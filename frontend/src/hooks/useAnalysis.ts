import { useState } from "react";
import { analyzeData, type AnalysisResult } from "../services/api.ts";

export function useAnalysis() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const submit = async (text: string, file: File | null) => {
    try {
      setLoading(true);
      setError(null);
      const data = await analyzeData(text, file);
      setResult(data);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze data");
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, result, submit };
}
