import { useState } from "react";
import { useAnalysis } from "../hooks/useAnalysis";

import TextInputCard from "../components/inputs/TextInputCard";
import VitalsUploadCard from "../components/inputs/VitalsUploadCard";
import RiskScoreCard from "../components/outputs/RiskScoreCard";
import ExplanationCard from "../components/outputs/ExplanationCard";

export default function Dashboard() {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const { loading, error, result, submit } = useAnalysis();

  return (
    <div style={{ padding: "20px" }}>
      <h1>Clinical Insight Analyzer</h1>

      <TextInputCard value={text} onChange={setText} />
      <VitalsUploadCard onFileSelect={setFile} />

      <button onClick={() => submit(text, file)} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <>
          <RiskScoreCard score={result.risk_score} />
          <ExplanationCard text={result.explanation} />
        </>
      )}
    </div>
  );
}
