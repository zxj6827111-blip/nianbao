import Link from 'next/link';

interface Props {
  params: { pairId: string };
}

export default function ReportPreviewPage({ params }: Props) {
  return (
    <main className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">对照报告 {params.pairId}</h1>
      <p>报告生成成功，可下载 PDF 或 Word。</p>
      <div className="space-x-4">
        <Link className="text-blue-600" href={`?format=pdf`}>导出 PDF</Link>
        <Link className="text-blue-600" href={`?format=docx`}>导出 Word</Link>
      </div>
    </main>
  );
}
