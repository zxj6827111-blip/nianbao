export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000';

export async function ingestDocument(payload: { text: string; title: string }) {
  const formData = new FormData();
  formData.append('text', payload.text);
  formData.append('title', payload.title);
  const res = await fetch(`${API_BASE}/ingest`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    throw new Error('入库失败');
  }
  return res.json();
}

export async function fetchDiff(leftId: number, rightId: number) {
  const res = await fetch(`${API_BASE}/diff/${leftId}/${rightId}`);
  if (!res.ok) {
    throw new Error('获取比对结果失败');
  }
  return res.json();
}
