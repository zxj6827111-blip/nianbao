'use client';

import { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000';

export default function Uploader() {
  const router = useRouter();
  const [title, setTitle] = useState('');
  const [url, setUrl] = useState('');
  const [busy, setBusy] = useState(false);
  const [log, setLog] = useState<string[]>([]);
  const fileRef = useRef<HTMLInputElement | null>(null);
  const [fileKey, setFileKey] = useState(0);

  function pushLog(s: string) {
    setLog((prev) => [...prev, s]);
  }

  async function ingestViaFile(file: File) {
    const fd = new FormData();
    fd.append('file', file);
    if (title) fd.append('title', title);
    const r = await fetch(`${API_BASE}/ingest`, { method: 'POST', body: fd });
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  }

  async function ingestViaUrl(u: string) {
    const body = { url: u, ...(title ? { title } : {}) };
    const r = await fetch(`${API_BASE}/ingest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  }

  async function maybeCompare(auto: any, rightDocId: number) {
    if (auto?.paired_with) {
      pushLog(
        `已自动匹配到上一年（doc_id=${auto.paired_with}，置信度=${auto.confidence ?? 'NA'}），开始比对…`
      );
      const r = await fetch(`${API_BASE}/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ left_doc_id: auto.paired_with, right_doc_id: rightDocId }),
      });
      if (!r.ok) throw new Error(await r.text());
      const data = await r.json();
      const pid = data.id ?? data.pair_id ?? data.comparison_id;
      if (pid) {
        router.push(`/compare/${pid}`);
      } else {
        pushLog('比对已完成，但未返回 pair_id。请手动在“库管理”里查看。');
      }
    } else {
      pushLog('未自动匹配到上一年，你可以在“库管理”里手动选择配对对象。');
    }
  }

  function resetInputs() {
    try {
      if (fileRef.current) fileRef.current.value = '';
    } catch {}
    setFileKey((k) => k + 1);
    // 如需清空标题或链接，可在此启用：
    // setTitle('');
    // setUrl('');
  }

  async function onUploadFile() {
    const f = fileRef.current?.files?.[0];
    if (!f) return;
    setBusy(true);
    setLog([]);
    try {
      pushLog(`上传文件：${f.name}`);
      const res = await ingestViaFile(f);
      pushLog(`入库成功，doc_id=${res.doc_id}`);
      await maybeCompare(res.auto, res.doc_id);
    } catch (e: any) {
      pushLog(`错误：${e.message || e.toString()}`);
    } finally {
      setBusy(false);
      resetInputs();
    }
  }

  async function onUploadUrl() {
    if (!url.trim()) return;
    setBusy(true);
    setLog([]);
    try {
      pushLog(`抓取链接：${url}`);
      const res = await ingestViaUrl(url.trim());
      pushLog(`入库成功，doc_id=${res.doc_id}`);
      await maybeCompare(res.auto, res.doc_id);
    } catch (e: any) {
      pushLog(`错误：${e.message || e.toString()}`);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto mt-8">
      <div className="rounded-2xl border p-6 shadow-sm bg-white">
        <h2 className="text-2xl font-semibold mb-4">上传/抓取 PDF</h2>

        <div className="grid gap-3">
          <input
            className="border rounded px-3 py-2"
            placeholder="标题（可选）"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <div className="flex items-center gap-3 flex-wrap">
            <input
              key={fileKey}
              ref={fileRef}
              type="file"
              accept="application/pdf"
              className="border rounded px-3 py-2"
              onClick={(e) => {
                (e.currentTarget as HTMLInputElement).value = '';
              }}
            />
            <button
              disabled={busy}
              onClick={onUploadFile}
              className="px-4 py-2 rounded bg-black text-white disabled:opacity-50"
            >
              选择 PDF 并上传
            </button>
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            <input
              className="border rounded px-3 py-2 flex-1 min-w-[260px]"
              placeholder="粘贴 PDF 链接（http/https）"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            <button
              disabled={busy || !url.trim()}
              onClick={onUploadUrl}
              className="px-4 py-2 rounded bg-indigo-600 text-white disabled:opacity-50"
            >
              通过链接上传
            </button>
          </div>

          <p className="text-gray-500 text-sm">
            提示：先上传上一年（如 2023），再上传当年（如 2024）。当年上传完成后系统会自动匹配上一年并发起比对。
          </p>

          <div className="mt-2">
            <h3 className="font-medium mb-1">调试日志</h3>
            <pre className="bg-gray-50 border rounded p-3 whitespace-pre-wrap min-h-[96px]">
              {log.join('\n')}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
