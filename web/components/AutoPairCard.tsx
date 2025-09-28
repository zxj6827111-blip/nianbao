'use client';

interface AutoPairCardProps {
  data: {
    region_code?: string;
    org_name?: string;
    year?: number;
    confidence?: number;
  } | null;
  docId: number;
}

export function AutoPairCard({ data, docId }: AutoPairCardProps) {
  if (!data) {
    return null;
  }
  return (
    <section className="border rounded p-4 space-y-2">
      <h2 className="text-lg font-semibold">自动识别结果</h2>
      <ul>
        <li>地区：{data.region_code ?? '未知'}</li>
        <li>机关：{data.org_name ?? '未知'}</li>
        <li>年份：{data.year ?? '未知'}</li>
        <li>置信度：{(data.confidence ?? 0).toFixed(2)}</li>
      </ul>
      <a className="text-blue-600" href={`/compare/${docId}-${docId}`}>开始比对</a>
    </section>
  );
}
