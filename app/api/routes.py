"""
HTTP routes only. No core logic here.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse

from app.api.schemas import AnalyzeRequest, AnalyzeResponse
from app.core.document import validate_document, chunk_document
from app.core.retrieval import select_relevant_chunks
from app.core.prompt import build_summary_prompt
from app.core.budgets import MAX_OUTPUT_TOKENS
from app.inference.local import LocalSummarizationModel
from app.inference.streaming import stream_text_chunks
from app.reliability.errors import AppError

router = APIRouter()

# Model loaded once per process
_model = LocalSummarizationModel()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    try:
        document = validate_document(req.document_text)
        chunks = chunk_document(document)
        relevant = select_relevant_chunks(chunks, req.query)

        prompt = build_summary_prompt(relevant, req.query)

        summary = _model.generate(
            prompt=prompt,
            max_tokens=MAX_OUTPUT_TOKENS,
            timeout_s=2.0,
        )

        return AnalyzeResponse(
            summary=summary,
            chunks_used=len(relevant),
            note="Summary generated using local offline model.",
        )

    except AppError as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": e.code,
                    "message": e.user_message,
                }
            },
        )


@router.post("/analyze/stream")
def analyze_stream(req: AnalyzeRequest):
    try:
        document = validate_document(req.document_text)
        chunks = chunk_document(document)
        relevant = select_relevant_chunks(chunks, req.query)

        prompt = build_summary_prompt(relevant, req.query)

        stream = _model.generate_stream(
            prompt=prompt,
            max_tokens=MAX_OUTPUT_TOKENS,
            timeout_s=2.5,
        )

        return StreamingResponse(
            stream_text_chunks(stream),
            media_type="text/event-stream",
        )

    except AppError as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": e.code,
                    "message": e.user_message,
                }
            },
        )
