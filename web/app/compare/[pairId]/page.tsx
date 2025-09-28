import { SummaryCards } from '@/components/SummaryCards';
import { SplitDiff } from '@/components/SplitDiff';
import { fetchDiff } from '@/lib/api';

interface Props {
  params: { pairId: string };
}

export default async function ComparePage({ params }: Props) {
  const [leftId, rightId] = params.pairId.split('-').map(Number);
  const diff = await fetchDiff(leftId, rightId);
  return (
    <main className="p-6 space-y-4">
      <SummaryCards summary={diff.summary} />
      <SplitDiff diff={diff} />
    </main>
  );
}
