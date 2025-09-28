from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class EmbedRequest(BaseModel):
    texts: list[str]


@router.post("/ai/embed")
def embed(request: EmbedRequest):
    embeddings = [[float(len(text))] for text in request.texts]
    return {"data": embeddings}


class SemanticDiffRequest(BaseModel):
    prompt: str
    context: str


@router.post("/ai/semantic_diff")
def semantic_diff(request: SemanticDiffRequest):
    return {"summary": f"对比完成：{len(request.context)}字"}
