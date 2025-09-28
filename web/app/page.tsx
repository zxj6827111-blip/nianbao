import Link from 'next/link';

const links = [
  { href: '/ingest', label: '采集入库' },
  { href: '/compare/demo', label: '比对示例' },
  { href: '/documents', label: '文档库' },
  { href: '/batch', label: '批量处理' }
];

export default function HomePage() {
  return (
    <main className="p-6 space-y-4">
      <h1 className="text-2xl font-semibold">年报对照平台</h1>
      <p>欢迎使用年度报告自动比对系统。</p>
      <nav className="flex flex-col gap-2">
        {links.map(link => (
          <Link key={link.href} className="text-blue-600" href={link.href}>
            {link.label}
          </Link>
        ))}
      </nav>
    </main>
  );
}
