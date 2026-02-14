import axios from "axios";

const API_BASE = "http://localhost:8000";

// Exported interface for TypeScript
export interface AnalysisResult {
  alignment: string;
  risk_score: number;
  severity_score: number;
  contradiction_score: number;
  explanation: string;
}

// API function to call backend
export async function analyzeData(text: string, file: File | null) {
  const formData = new FormData();
  formData.append("text", text);
  if (file) formData.append("file", file);

  const response = await axios.post<AnalysisResult>(
    `${API_BASE}/analyze`,
    formData,
    { headers: { "Content-Type": "multipart/form-data" } }
  );

  return response.data;
}



// This is a mocked version of the API function for testing without a backend , Uncomment to use.

/*
export async function analyzeData(text: string, file: File | null): Promise<AnalysisResult> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        alignment: "Neutral",
        risk_score: Math.floor(Math.random() * 100),
        severity_score: Math.floor(Math.random() * 10),
        contradiction_score: Math.floor(Math.random() * 5),
        explanation: `This is a mocked analysis of your input: "${text.slice(0, 50)}..."`,
      });
    }, 1000);
  });
}
*/