# api/main.py
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import itertools
import os

app = FastAPI(title="年报比对系统")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局存储
DOC_STORE: Dict[int, Dict] = {}  # {doc_id: {"path": str, "filename": str}}
PAIR_STORE: Dict[int, Dict] = {}  # {pair_id: {"created_at": datetime, "status": str, "left_doc": dict, "right_doc": dict, "result": dict}}
DOC_COUNTER = itertools.count(1)
PAIR_COUNTER = itertools.count(1)

# 文件存储路径
SAVE_DIR = "/tmp/nb_docs"
os.makedirs(SAVE_DIR, exist_ok=True)


# 请求/响应模型
class CompareRequest(BaseModel):
    left_doc_id: int
    right_doc_id: int

class PairResponse(BaseModel):
    pair_id: int
    created_at: datetime
    status: str
    left_doc: Dict
    right_doc: Dict
    result: Optional[Dict] = None

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    doc_id = next(DOC_COUNTER)
    save_path = os.path.join(SAVE_DIR, f"{doc_id}__{file.filename}")
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    DOC_STORE[doc_id] = {
        "path": save_path,
        "filename": file.filename,
        "created_at": datetime.now()
    }
    print(f"[ingest] saved doc_id={doc_id}, file={file.filename}")
    return {"doc_id": doc_id, "filename": file.filename}

@app.post("/compare", response_model=Dict)
async def compare(req: CompareRequest):
    left = DOC_STORE.get(req.left_doc_id)
    right = DOC_STORE.get(req.right_doc_id)
    if not left or not right:
        raise HTTPException(status_code=404, detail="Documents not found")
    
    pair_id = next(PAIR_COUNTER)
    pair = {
        "pair_id": pair_id,
        "created_at": datetime.now(),
        "status": "completed",
        "left_doc": {
            "doc_id": req.left_doc_id,
            **left
        },
        "right_doc": {
            "doc_id": req.right_doc_id,
            **right
        },
        "result": {
            "diffs": []  # 占位比对结果
        }
    }
    PAIR_STORE[pair_id] = pair
    print(f"[compare] created pair_id={pair_id}")
    return {"pair_id": pair_id}

@app.get("/pairs/{pair_id}", response_model=Dict)
async def get_pair(pair_id: int):
    pair = PAIR_STORE.get(pair_id)
    if not pair:
        raise HTTPException(status_code=404, detail="Pair not found")
    return pair

@app.get("/pairs/recent", response_model=List[Dict])
async def list_recent_pairs(limit: int = 20):
    pairs = sorted(
        PAIR_STORE.values(),
        key=lambda x: x["created_at"],
        reverse=True
    )[:limit]
    return pairs
