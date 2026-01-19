"""
Request and response schemas.
"""

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    document_text: str = Field(..., description="UTF-8 document text")
    query: str = Field(..., description="Natural language query")


class AnalyzeResponse(BaseModel):
    summary: str
    chunks_used: int
    note: str
