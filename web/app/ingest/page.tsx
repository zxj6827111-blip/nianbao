'use client';

import { useState } from 'react';
import { AutoPairCard } from '@/components/AutoPairCard';
import { ingestDocument } from '@/lib/api';

export default function IngestPage() {
  const [text, setText] = useState('');
  const [title, setTitle] = useState('');
  const [result, setResult] = useState<any>();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      const res = await ingestDocument({ text, title });
      setResult(res);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">采集入库</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input
          className="border p-2 w-full"
          placeholder="标题"
          value={title}
          onChange={event => setTitle(event.target.value)}
        />
        <textarea
          className="border p-2 w-full h-48"
          placeholder="粘贴文本或上传文件"
          value={text}
          onChange={event => setText(event.target.value)}
        />
        <button className="bg-blue-600 text-white px-4 py-2" disabled={loading} type="submit">
          {loading ? '处理中…' : '入库'}
        </button>
      </form>
      {result && <AutoPairCard data={result.auto} docId={result.doc_id} />}
    </main>
  );
}
