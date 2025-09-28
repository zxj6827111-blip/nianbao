from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.compare import CompareService

router = APIRouter()
service = CompareService()


class CompareRequest(BaseModel):
    left_doc_id: int
    right_doc_id: int


@router.post("/compare")
def compare(request: CompareRequest):
    try:
        result = service.compare(request.left_doc_id, request.right_doc_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return result
