from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..services.compare import CompareService

router = APIRouter()
service = CompareService()


@router.get("/diff/{left_doc_id}/{right_doc_id}")
def get_diff(left_doc_id: int, right_doc_id: int):
    try:
        result = service.compare(left_doc_id, right_doc_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return result
