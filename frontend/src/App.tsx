import React, { useState } from "react";
import { useAnalysis } from "./hooks/useAnalysis";
import { Zap, AlertCircle, CheckCircle, FileUp, X } from "lucide-react";
import "./App.css";

export default function App() {
  const { loading, error, result, submit } = useAnalysis();
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const allowedType = "application/pdf";

  const handleFile = (selectedFile: File | null) => {
    if (!selectedFile) return;

    if (selectedFile.type !== allowedType) {
      alert("Unsupported file type. Please upload a PDF file only.");
      return;
    }

    setFile(selectedFile);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    submit(text, file);
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="header-content">
          <div className="header-title">
            <div className="header-icon">
              <Zap size={24} />
            </div>
            <div>
              <h1>Contradiction Detection System</h1>
              <p>Advanced AI-Driven Contradiction Detection and Inconsistency Analysis</p>
            </div>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          <section className="form-section">
            <div className="form-container">
              <div className="form-header">
                <h2>Analyze Your Text for Contradictions</h2>
                <p>Input your text or upload a PDF file for contradiction detection</p>
              </div>

              <form onSubmit={handleSubmit} className="analysis-form">
                <div className="form-group">
                  <label htmlFor="text-input">Enter Statements for Analysis</label>
                  <textarea
                    id="text-input"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste your text here for analysis..."
                    className="textarea-input"
                    rows={6}
                  />
                  <div className="char-count">{text.length} characters</div>
                </div>

                <div className="form-group">
                  <label htmlFor="file-input">Upload PDF File</label>
                  <div
                    className={`file-upload-wrapper ${
                      file ? "has-file" : ""
                    } ${isDragging ? "dragging" : ""}`}
                    onClick={() =>
                      document.getElementById("file-input")?.click()
                    }
                    onDragOver={(e) => {
                      e.preventDefault();
                      setIsDragging(true);
                    }}
                    onDragLeave={(e) => {
                      e.preventDefault();
                      setIsDragging(false);
                    }}
                    onDrop={(e) => {
                      e.preventDefault();
                      setIsDragging(false);
                      const droppedFile = e.dataTransfer.files[0];
                      handleFile(droppedFile);
                    }}
                  >
                    <input
                      id="file-input"
                      type="file"
                      accept=".pdf,application/pdf"
                      onChange={(e) =>
                        handleFile(e.target.files?.[0] ?? null)
                      }
                      style={{ display: "none" }}
                    />

                    <div className="file-upload-display">
                      <FileUp size={24} />
                      <span>
                        {file
                          ? file.name
                          : isDragging
                          ? "Release to upload your PDF"
                          : "Click or drag a PDF file here"}
                      </span>
                    </div>
                  </div>

                  {file && (
                    <div style={{ marginTop: "10px" }}>
                      <button
                        type="button"
                        className="remove-file"
                        onClick={() => setFile(null)}
                      >
                        <X size={16} /> Remove PDF
                      </button>
                    </div>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={loading || (!text && !file)}
                  className={`submit-button ${loading ? "loading" : ""}`}
                >
                  {loading ? (
                    <>
                      <span className="spinner"></span>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Zap size={16} />
                      Analyze Now
                    </>
                  )}
                </button>
              </form>
            </div>
          </section>

          {error && (
            <div className="error-alert">
              <AlertCircle size={20} />
              <div className="alert-content">
                <h3>Analysis Error</h3>
                <p>{error}</p>
              </div>
            </div>
          )}

          {result && (
            <section className="results-section">
              <div className="results-header">
                <CheckCircle size={24} className="success-icon" />
                <h2>Analysis Results</h2>
              </div>

              <div className="verdict-confidence-row">

                <div className="metric-card">
                  <div className="metric-label">Verdict</div>
                  <div className="metric-value">
                    {result.verdict}
                  </div>
                </div>

                <div className="metric-card">
                  <div className="metric-label">Confidence</div>
                  <div className="metric-value">
                    {(result.confidence * 100).toFixed(1)}%
                  </div>
                  <div className="metric-bar">
                    <div
                      className="metric-fill"
                      style={{
                        width: `${result.confidence * 100}%`,
                      }}
                    ></div>
                  </div>
                </div>

              </div>

              <div className="explanation-card">
                <h3>Evidence</h3>
                <ul>
                  {result.evidence.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              <div className="explanation-card">
                <h3>Detailed Explanation</h3>
                <p>{result.explanation}</p>
              </div>
            </section>
          )}
        </div>
      </main>
    </div>
  );
}