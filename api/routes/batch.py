from __future__ import annotations

import csv
import io
from typing import List

from fastapi import APIRouter, File, UploadFile

from ..services.documents import DocumentService

router = APIRouter()
service = DocumentService()


@router.post("/batch")
async def batch_import(file: UploadFile = File(...)):
    content = await file.read()
    buffer = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(buffer)
    results: List[dict] = []
    for row in reader:
        text = row.get("text") or ""
        title = row.get("title") or ""
        url = row.get("url") or ""
        if not text:
            continue
        result = service.ingest_text(text=text, title=title, url=url)
        results.append({"row": row, "result": result})
    return {"items": results}
