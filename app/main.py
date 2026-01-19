"""
Application entrypoint.

Responsibilities:
- Initialize FastAPI app
- Register routes
- Configure middleware
- Configure logging
- Start HTTP server

This module contains no business logic.
"""

import time
import uuid
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.api.routes import router as api_router
from app.config import CONFIG
from app.logging import setup_logging


def create_app() -> FastAPI:
    """
    Factory for the FastAPI application.

    Returns:
        Configured FastAPI app.
    """

    # --- Logging (initialize once) ---
    setup_logging()
    logger = logging.getLogger("app")

    app = FastAPI(
        title="Document Analysis Prototype",
        description="Offline-first AI system for document analysis and summarization.",
        version="1.0.0",
    )

    # --- Middleware: request ID, logging, timing ---
    @app.middleware("http")
    async def add_request_metadata(request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        adapter = logging.LoggerAdapter(
            logger,
            {"request_id": request_id},
        )

        adapter.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
            },
        )

        try:
            response = await call_next(request)
        except Exception:
            adapter.exception("Unhandled exception during request")

            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": "An unexpected error occurred.",
                        "request_id": request_id,
                    }
                },
            )

        latency_ms = int((time.time() - start_time) * 1000)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Latency-ms"] = str(latency_ms)

        adapter.info(
            "Request completed",
            extra={
                "status_code": response.status_code,
                "latency_ms": latency_ms,
            },
        )

        return response

    # --- API routes ---
    app.include_router(api_router)

    # --- Health check ---
    @app.get("/health")
    def health():
        return {"status": "ok"}

    # --- Static UI ---
    app.mount(
        "/",
        StaticFiles(directory="app/ui/static", html=True),
        name="ui",
    )

    return app


# --- ASGI app ---
app = create_app()


# --- Local execution ---
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=CONFIG.HOST,
        port=CONFIG.PORT,
        reload=False,
        log_level="info",
    )
