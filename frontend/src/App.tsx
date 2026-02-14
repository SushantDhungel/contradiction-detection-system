import React, { useState } from "react";
import { useAnalysis } from "./hooks/useAnalysis";

export default function App() {
  const { loading, error, result, submit } = useAnalysis();
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    submit(text, file);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Text Analysis</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text here..."
          rows={5}
          cols={50}
        />
        <br />
        <input type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: "1rem" }}>
          <h2>Results</h2>
          <p><strong>Alignment:</strong> {result.alignment}</p>
          <p><strong>Risk Score:</strong> {result.risk_score}</p>
          <p><strong>Severity Score:</strong> {result.severity_score}</p>
          <p><strong>Contradiction Score:</strong> {result.contradiction_score}</p>
          <p><strong>Explanation:</strong> {result.explanation}</p>
        </div>
      )}
    </div>
  );
}
