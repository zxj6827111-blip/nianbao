import Link from 'next/link';

const documents = [
  {
    region: '淮安市',
    org: '淮安市人民政府',
    year: 2024,
    docId: 1
  }
];

export default function DocumentsPage() {
  return (
    <main className="p-6 space-y-4">
      <h1 className="text-xl font-semibold">文档库</h1>
      <ul className="space-y-2">
        {documents.map(doc => (
          <li key={`${doc.docId}-${doc.year}`} className="border p-3">
            <p>{doc.region} · {doc.org} · {doc.year}</p>
            <Link className="text-blue-600" href={`/compare/${doc.docId}-1`}>
              查看比对
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
