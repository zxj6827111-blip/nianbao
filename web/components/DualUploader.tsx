'use client';

import { useRef, useState } from 'react';
import { useRouter } from 'next/navigation';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000';

type Stat = 'idle'|'uploading'|'done'|'error';
type UploadState = {
  year: number;
  fileKey: number;
  filename?: string;
  progress: number;
  status: Stat;
  docId?: number;
  msg?: string;
};

function ProgressBar({ value }: { value: number }) {
  return (
    <div className="h-2 bg-gray-200 rounded w-full">
      <div
        className="h-2 bg-indigo-600 rounded"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  );
}

export default function DualUploader() {
  const now = new Date().getFullYear();
  const router = useRouter();

  const prevRef = useRef<HTMLInputElement | null>(null);
  const currRef = useRef<HTMLInputElement | null>(null);

  const [busy, setBusy] = useState(false);
  const [prev, setPrev] = useState<UploadState>({
    year: now - 1,
    fileKey: 0,
    progress: 0,
    status: 'idle',
  });
  const [curr, setCurr] = useState<UploadState>({
    year: now,
    fileKey: 0,
    progress: 0,
    status: 'idle',
  });

  const canCompare =
    prev.status === 'done' &&
    curr.status === 'done' &&
    !!prev.docId &&
    !!curr.docId &&
    !busy;

  function resetInput(which: 'prev' | 'curr') {
    if (which === 'prev' && prevRef.current) {
      try {
        prevRef.current.value = '';
      } catch {}
    }
    if (which === 'curr' && currRef.current) {
      try {
        currRef.current.value = '';
      } catch {}
    }
    if (which === 'prev') {
      setPrev((s) => ({ ...s, fileKey: s.fileKey + 1 }));
    } else {
      setCurr((s) => ({ ...s, fileKey: s.fileKey + 1 }));
    }
  }

  async function uploadFile(which: 'prev' | 'curr') {
    const node = which === 'prev' ? prevRef.current : currRef.current;
    const state = which === 'prev' ? prev : curr;
    const setState = which === 'prev' ? setPrev : setCurr;
    const f = node?.files?.[0];
    if (!f) return;

    setBusy(true);
    setState((s) => ({
      ...s,
      status: 'uploading',
      progress: 0,
      filename: f.name,
      msg: undefined,
      docId: undefined,
    }));

    const fd = new FormData();
    fd.append('file', f);
    fd.append('year', String(state.year));

    const xhr = new XMLHttpRequest();
    xhr.open('POST', `${API_BASE}/ingest`, true);

    xhr.upload.onprogress = (evt) => {
      if (evt.lengthComputable) {
        const p = Math.round((evt.loaded / evt.total) * 100);
        setState((s) => ({ ...s, progress: p }));
      }
    };

    xhr.onerror = () => {
      setState((s) => ({ ...s, status: 'error', msg: '网络错误', docId: undefined }));
      setBusy(false);
      resetInput(which);
    };

    xhr.onload = () => {
      try {
        if (xhr.status >= 200 && xhr.status < 300) {
          const res = JSON.parse(xhr.responseText || '{}');
          setState((s) => ({
            ...s,
            status: 'done',
            progress: 100,
            docId: res.doc_id,
            msg: `doc_id=${res.doc_id}`,
          }));
        } else {
          setState((s) => ({
            ...s,
            status: 'error',
            msg: `${xhr.status} ${xhr.statusText}`,
            docId: undefined,
          }));
        }
      } catch (e: any) {
        setState((s) => ({
          ...s,
          status: 'error',
          msg: e?.message || '解析响应失败',
          docId: undefined,
        }));
      } finally {
        setBusy(false);
        resetInput(which);
      }
    };

    xhr.send(fd);
  }

  async function startCompare() {
    if (!canCompare) return;
    setBusy(true);
    try {
      const r = await fetch(`${API_BASE}/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ left_doc_id: prev.docId, right_doc_id: curr.docId }),
      });
      if (!r.ok) throw new Error(await r.text());
      const data = await r.json();
      const pid = data.id ?? data.pair_id ?? data.comparison_id;
      if (pid) {
        router.push(`/compare/${pid}`);
      } else {
        alert('比对完成，但未返回 pair_id，请到库管理或最近任务查看。');
      }
    } catch (e: any) {
      alert(`比对失败：${e?.message || e}`);
    } finally {
      setBusy(false);
    }
  }

  function resetAll() {
    if (prevRef.current) {
      try {
        prevRef.current.value = '';
      } catch {}
    }
    if (currRef.current) {
      try {
        currRef.current.value = '';
      } catch {}
    }
    setPrev((s) => ({
      year: now - 1,
      fileKey: s.fileKey + 1,
      progress: 0,
      status: 'idle',
      filename: undefined,
      docId: undefined,
      msg: undefined,
    }));
    setCurr((s) => ({
      year: now,
      fileKey: s.fileKey + 1,
      progress: 0,
      status: 'idle',
      filename: undefined,
      docId: undefined,
      msg: undefined,
    }));
    setBusy(false);
  }

  return (
    <div className="max-w-5xl mx-auto mt-6 space-y-6">
      <div className="grid md:grid-cols-2 gap-6">
        <div className="rounded-2xl border p-5 bg-white shadow-sm">
          <h3 className="text-lg font-semibold mb-3">上传上一年度</h3>
          <div className="flex items-center gap-3 mb-3">
            <label className="text-sm text-gray-600">年份</label>
            <input
              type="number"
              min={2000}
              max={9999}
              value={prev.year}
              onChange={(e) =>
                setPrev((s) => ({ ...s, year: Number(e.target.value || now - 1) }))
              }
              className="w-28 border rounded px-2 py-1"
            />
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            <input
              key={prev.fileKey}
              ref={prevRef}
              type="file"
              accept="application/pdf"
              className="border rounded px-3 py-2"
              onClick={(e) => {
                (e.currentTarget as HTMLInputElement).value = '';
              }}
            />
            <button
              onClick={() => uploadFile('prev')}
              disabled={busy}
              className="px-4 py-2 rounded bg-black text-white disabled:opacity-50"
            >
              上传上一年 PDF
            </button>
          </div>
          <div className="mt-3 space-y-1">
            <ProgressBar value={prev.progress} />
            <div className="text-sm text-gray-600">
              {prev.status === 'idle' && '等待上传…'}
              {prev.status === 'uploading' && `上传中：${prev.filename} (${prev.progress}%)`}
              {prev.status === 'done' && `上传完成：${prev.filename}（doc_id=${prev.docId}）`}
              {prev.status === 'error' && `上传失败：${prev.msg || ''}`}
            </div>
          </div>
        </div>

        <div className="rounded-2xl border p-5 bg-white shadow-sm">
          <h3 className="text-lg font-semibold mb-3">上传本年度</h3>
          <div className="flex items-center gap-3 mb-3">
            <label className="text-sm text-gray-600">年份</label>
            <input
              type="number"
              min={2000}
              max={9999}
              value={curr.year}
              onChange={(e) =>
                setCurr((s) => ({ ...s, year: Number(e.target.value || now) }))
              }
              className="w-28 border rounded px-2 py-1"
            />
          </div>
          <div className="flex items-center gap-3 flex-wrap">
            <input
              key={curr.fileKey}
              ref={currRef}
              type="file"
              accept="application/pdf"
              className="border rounded px-3 py-2"
              onClick={(e) => {
                (e.currentTarget as HTMLInputElement).value = '';
              }}
            />
            <button
              onClick={() => uploadFile('curr')}
              disabled={busy}
              className="px-4 py-2 rounded bg-black text-white disabled:opacity-50"
            >
              上传本年 PDF
            </button>
          </div>
          <div className="mt-3 space-y-1">
            <ProgressBar value={curr.progress} />
            <div className="text-sm text-gray-600">
              {curr.status === 'idle' && '等待上传…'}
              {curr.status === 'uploading' && `上传中：${curr.filename} (${curr.progress}%)`}
              {curr.status === 'done' && `上传完成：${curr.filename}（doc_id=${curr.docId}）`}
              {curr.status === 'error' && `上传失败：${curr.msg || ''}`}
            </div>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={startCompare}
          disabled={!canCompare}
          className="px-4 py-2 rounded bg-indigo-600 text-white disabled:opacity-50"
        >
          开始比对
        </button>
        <button onClick={resetAll} className="px-4 py-2 rounded border">
          重置
        </button>
        <span className="text-sm text-gray-600">
          需先完成两份上传后才可点击“开始比对”。默认以“上一年”为 left，“本年”为 right。
        </span>
      </div>
    </div>
  );
}
