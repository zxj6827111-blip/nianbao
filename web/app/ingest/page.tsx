import DualUploader from "@/components/DualUploader";

export default function IngestPage() {
  return (
    <main className="p-8">
      <h1 className="text-3xl font-semibold mb-4">采集入库</h1>
      <DualUploader />
    </main>
  );
}
