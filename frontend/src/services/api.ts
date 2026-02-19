import axios from "axios";

const API_BASE = "http://localhost:8000/api";

export interface AnalysisResult {
  verdict: string;
  evidence: string[];
  confidence: number;
  explanation: string;
}

export async function analyzeData(claim: string, file: File | null) {
  const formData = new FormData();
  formData.append("claim", claim);
  if (file) formData.append("file", file);

  const response = await axios.post<AnalysisResult>(
    `${API_BASE}/verify`,
    formData,
    { headers: { "Content-Type": "multipart/form-data" } }
  );

  return response.data;
}
