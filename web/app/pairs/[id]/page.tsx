'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000';

export default function PairDetailPage() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    async function fetchPair() {
      try {
        const r = await fetch(`${API_BASE}/pairs/${id}`);
        if (!r.ok) throw new Error(await r.text());
        const data = await r.json();
        setData(data);
      } catch (e: any) {
        setError(e.message || String(e));
      }
    }
    if (id) fetchPair();
  }, [id]);

  if (error) return <div className="text-red-500">错误：{error}</div>;
  if (!data) return <div>加载中...</div>;

  return (
    <div className="max-w-5xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">比对结果</h1>
      
      <div className="grid gap-6">
        <div className="flex gap-4 text-sm text-gray-500">
          <div>ID: {data.pair_id}</div>
          <div>创建时间: {new Date(data.created_at).toLocaleString()}</div>
          <div>状态: {data.status}</div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="p-4 border rounded">
            <h3 className="font-medium mb-2">左侧文档</h3>
            <div>{data.left_doc.filename}</div>
          </div>
          <div className="p-4 border rounded">
            <h3 className="font-medium mb-2">右侧文档</h3>
            <div>{data.right_doc.filename}</div>
          </div>
        </div>

        <div className="mt-4">
          <h3 className="font-medium mb-2">比对结果</h3>
          <pre className="bg-gray-50 p-4 rounded overflow-auto">
            {JSON.stringify(data.result, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}