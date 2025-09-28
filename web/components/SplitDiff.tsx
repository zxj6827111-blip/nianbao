interface SplitDiffProps {
  diff: any;
}

export function SplitDiff({ diff }: SplitDiffProps) {
  return (
    <div className="grid grid-cols-2 gap-4">
      <section className="space-y-3">
        <h2 className="text-lg font-semibold">文本对照</h2>
        <div className="space-y-2">
          {diff.text_pairs?.map((pair: any, index: number) => (
            <article key={index} className={`border p-2 ${pair.matched ? 'bg-yellow-50' : 'bg-red-50'}`}>
              <p className="text-sm text-gray-600">上一年</p>
              <p>{pair.left}</p>
              <p className="text-sm text-gray-600">当年</p>
              <p>{pair.right}</p>
              <p className="text-xs text-gray-500">相似度：{pair.score.toFixed(2)}</p>
            </article>
          ))}
        </div>
      </section>
      <section className="space-y-3">
        <h2 className="text-lg font-semibold">表格差异</h2>
        {Object.entries(diff.tables || {}).map(([key, table]: any) => (
          <div key={key} className="border p-2">
            <h3 className="font-medium">{key}</h3>
            <table className="w-full text-sm">
              <thead>
                <tr>
                  <th className="text-left">指标</th>
                  <th>上一年</th>
                  <th>当年</th>
                  <th>变化</th>
                </tr>
              </thead>
              <tbody>
                {table.cells.map((cell: any) => (
                  <tr key={cell.path_key} className={cell.changed ? 'bg-red-50' : ''}>
                    <td>{cell.path_key}</td>
                    <td>{cell.left ?? '-'}</td>
                    <td>{cell.right ?? '-'}</td>
                    <td>{cell.changed ? '变化' : '相同'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </section>
    </div>
  );
}
