import Uploader from "@/components/Uploader";

export default function Home() {
  return (
    <main className="p-8">
      <h1 className="text-4xl font-bold mb-2">年报对照平台</h1>
      <p className="text-gray-600 mb-6">欢迎使用年度报告自动比对系统。</p>
      <Uploader />
    </main>
  );
}
