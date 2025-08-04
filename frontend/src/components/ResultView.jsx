export default function ResultView({ reviewResult }) {
  const { suggestions, warnings, optimizations, score, remark } = reviewResult;

  return (
    <div className="mt-6 p-4 bg-white rounded shadow space-y-2">
      <h2 className="text-xl font-semibold text-green-700">🧾 Review Summary</h2>
      <p><strong>📊 Remark:</strong> {remark}</p>
      <p><strong>✅ Score:</strong> {score}/100</p>

      {suggestions?.length > 0 && (
        <div>
          <strong>✅ Suggestions:</strong>
          <ul className="list-disc ml-5">
            {suggestions.map((s, i) => (
              <li key={`suggestion-${i}`}>{s}</li>
            ))}
          </ul>
        </div>
      )}

      {warnings?.length > 0 && (
        <div>
          <strong>⚠️ Warnings:</strong>
          <ul className="list-disc ml-5">
            {warnings.map((w, i) => (
              <li key={`warning-${i}`}>{w}</li>
            ))}
          </ul>
        </div>
      )}

      {optimizations?.length > 0 && (
        <div>
          <strong>💡 Optimizations:</strong>
          <ul className="list-disc ml-5">
            {optimizations.map((o, i) => (
              <li key={`optimization-${i}`}>{o}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
