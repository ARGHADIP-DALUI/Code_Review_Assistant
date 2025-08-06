export default function ResultView({ reviewResult }) {
  const {
    suggestions,
    warnings,
    optimizations,
    bugs,
    score,
    remark,
    report_url
  } = reviewResult;

  const renderSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case "high":
        return "🔥";
      case "medium":
        return "⚠️";
      case "low":
        return "ℹ️";
      default:
        return "🐞";
    }
  };

  return (
    <div className="mt-6 p-4 bg-white rounded shadow space-y-4">
      <h2 className="text-xl font-semibold text-green-700">🧾 Review Summary</h2>

      <div className="flex items-center justify-between">
        <p className="text-lg font-semibold text-blue-600">📊 Remark: {remark}</p>
        <p className="text-lg font-bold text-purple-600">✅ Score: {score}/100</p>
      </div>

      {report_url && (
        <a
          href={report_url}
          className="text-blue-500 underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          📄 Download PDF Report
        </a>
      )}

      {bugs?.length > 0 && (
        <div>
          <hr className="my-2" />
          <strong>🐞 Detected Bugs:</strong>
          <ul className="list-disc ml-5 text-red-700 space-y-2">
            {bugs.map((bug, i) => (
              <li key={`bug-${i}`}>
                {renderSeverityIcon(bug.severity)} <strong>{bug.message}</strong>
                {bug.tip && <p className="text-sm text-gray-600 ml-4">💡 Tip: {bug.tip}</p>}
              </li>
            ))}
          </ul>
        </div>
      )}

      {suggestions?.length > 0 && (
        <div>
          <hr className="my-2" />
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
          <hr className="my-2" />
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
          <hr className="my-2" />
          <strong>💡 Optimizations:</strong>
          <ul className="list-disc ml-5">
            {optimizations.map((o, i) => (
              <li key={`optimization-${i}`}>{o}</li>
            ))}
          </ul>
        </div>
      )}

      {suggestions?.length === 0 &&
        warnings?.length === 0 &&
        optimizations?.length === 0 &&
        bugs?.length === 0 && (
          <p className="text-gray-500 italic">
            No suggestions, warnings, optimizations, or bugs found.
          </p>
      )}
    </div>
  );
}



