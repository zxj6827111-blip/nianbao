from __future__ import annotations

from fastapi import FastAPI

from .routes import ai, batch, compare, diff, ingest


def create_app() -> FastAPI:
    app = FastAPI(title="Nianbao API")
    app.include_router(ingest.router)
    app.include_router(compare.router)
    app.include_router(diff.router)
    app.include_router(batch.router)
    app.include_router(ai.router)
    return app


app = create_app()
