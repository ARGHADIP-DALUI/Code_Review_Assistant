import { useState } from "react";
import Editor from "@monaco-editor/react";
import ResultView from "./ResultView"; // ✅ Import ResultView

export default function CodeEditor() {
  const [language, setLanguage] = useState("python");
  const [reviewType, setReviewType] = useState("basic");
  const [code, setCode] = useState("");
  const [reviewResult, setReviewResult] = useState(null); // ✅ Store review result

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/review", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ language, code, review_type: reviewType }),
      });

      if (!response.ok) {
        throw new Error("Server Error");
      }

      const data = await response.json();
      setReviewResult(data); // ✅ Store review result
    } catch (error) {
      console.error("❌ Review Error:", error);
      alert("🚨 Failed to submit code for review. Is your FastAPI backend running?");
    }
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-3xl font-bold">Code Review Assistant 🧠</h1>

      <div className="flex gap-4">
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="border p-2 rounded"
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
        </select>

        <select
          value={reviewType}
          onChange={(e) => setReviewType(e.target.value)}
          className="border p-2 rounded"
        >
          <option value="basic">Basic</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>

      <Editor
        height="400px"
        language={language}
        value={code}
        onChange={(value) => setCode(value)}
        theme="vs-dark"
      />

      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        🚀 Submit for Review
      </button>

      {/* ✅ UI for Review Output */}
      {reviewResult && <ResultView reviewResult={reviewResult} />} {/* Pass reviewResult to ResultView */}
    </div>
  );
}

