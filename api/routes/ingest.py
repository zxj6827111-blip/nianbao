# api/routes/ingest.py
from __future__ import annotations

import io
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

router = APIRouter()


def _decode_text(binary: bytes) -> str:
    """尽量把二进制解成文本（非 PDF 时用）"""
    try:
        return binary.decode("utf-8")
    except UnicodeDecodeError:
        try:
            import chardet  # 可选依赖；没有也会退回 ignore
            enc = (chardet.detect(binary) or {}).get("encoding") or "utf-8"
            return binary.decode(enc, errors="ignore")
        except Exception:
            return binary.decode("utf-8", errors="ignore")


def _extract_pdf_text(binary: bytes) -> str:
    """从 PDF 二进制中提取文本"""
    # 先尝试 pdfminer.six
    try:
        from pdfminer.high_level import extract_text
        return extract_text(io.BytesIO(binary)) or ""
    except Exception:
        # 再退回 pypdf
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(binary))
            return "\n".join((page.extract_text() or "") for page in reader.pages)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"PDF 解析失败: {e}")


@router.post("/ingest")
async def ingest(
    file: Optional[UploadFile] = File(default=None),
    title: Optional[str] = Form(default=None),
    year: Optional[int] = Form(default=None),
    url: Optional[str] = Form(default=None),
):
    """
    仅演示读取与文本提取：
    - 上传 PDF：二进制 → 提取文本
    - 上传 txt：按文本解码
    - （如需支持 url，这里可补：下载后走同样分支）
    """
    if not file and not url:
        raise HTTPException(status_code=400, detail="请上传文件或提供链接")

    if file:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="空文件")
        is_pdf = (
            (getattr(file, "content_type", "") or "").lower() in ("application/pdf", "application/x-pdf")
            or content.startswith(b"%PDF-")
        )
        text_content = _extract_pdf_text(content) if is_pdf else _decode_text(content)
    else:
        # 如果你现在暂时不做 URL 下载，这里先返回错误或留 TODO
        raise HTTPException(status_code=400, detail="暂不支持链接抓取，请先用文件上传")

    # TODO: 把 text_content/title/year 交给你的持久化服务，返回 doc_id
    # 例如：doc_id = documents.save(title, year, text_content, raw=content)
    # 这里先返回一个模拟字段，确保前端流程能走通
    return {"doc_id": 1, "auto": None, "year": year, "title": title}
