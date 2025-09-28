from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..services.documents import DocumentService

router = APIRouter()
service = DocumentService()


@router.post("/ingest")
async def ingest(
    file: UploadFile | None = None,
    url: str | None = Form(default=None),
    title: str | None = Form(default=None),
    text: str | None = Form(default=None),
):
    if file:
        content = await file.read()
        text_content = content.decode("utf-8")
    elif text:
        text_content = text
    else:
        raise HTTPException(status_code=400, detail="file or text required")
    result = service.ingest_text(text=text_content, title=title or (file.filename if file else ""), url=url or "")
    return result
