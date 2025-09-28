'use client';

import { useState } from 'react';

export default function BatchPage() {
  const [rows, setRows] = useState<string>('');
  const [result, setResult] = useState<string>('');

  const onSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    setResult(rows.split('\n').filter(Boolean).map((line, index) => `任务${index + 1}: 待处理`).join('\n'));
  };

  return (
    <main className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">批量导入</h1>
      <form className="space-y-3" onSubmit={onSubmit}>
        <textarea
          className="border p-2 w-full h-40"
          placeholder="粘贴CSV内容"
          value={rows}
          onChange={event => setRows(event.target.value)}
        />
        <button className="bg-blue-600 text-white px-4 py-2" type="submit">解析</button>
      </form>
      {result && (
        <pre className="bg-gray-100 p-3 whitespace-pre-wrap">{result}</pre>
      )}
    </main>
  );
}
