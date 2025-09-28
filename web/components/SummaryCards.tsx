interface SummaryCardsProps {
  summary: {
    text_reuse?: number;
    table_reuse?: number;
    balance_ok?: boolean;
    balance_delta?: number;
  };
}

export function SummaryCards({ summary }: SummaryCardsProps) {
  return (
    <section className="grid grid-cols-2 gap-4">
      <div className="border rounded p-4">
        <h2 className="text-lg font-semibold">复用率</h2>
        <p>文本：{formatPercent(summary.text_reuse)}</p>
        <p>表格：{formatPercent(summary.table_reuse)}</p>
      </div>
      <div className="border rounded p-4">
        <h2 className="text-lg font-semibold">勾稽校验</h2>
        <p>{summary.balance_ok ? '通过' : `未通过（差额 ${summary.balance_delta}）`}</p>
      </div>
    </section>
  );
}

function formatPercent(value?: number) {
  if (value === undefined) {
    return 'N/A';
  }
  return `${(value * 100).toFixed(1)}%`;
}
