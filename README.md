# Contradiction Detection System

An AI-powered system that verifies claims and statements against source documents (PDF, text, or images) to detect contradictions, inconsistencies, and factual accuracy.

## 🎯 What It Does

Users provide:

1. **Source Document** — A PDF, text file, or image containing factual information
2. **Claim/Statement** — A statement to verify against the source

The system analyzes the claim and returns:

- **Verdict**: TRUE / FALSE / PARTIALLY TRUE / CANNOT DETERMINE
- **Explanation**: Why the claim is supported or contradicted
- **Evidence**: Relevant excerpts from the source document

### Example Use Case

> **Source**: Company quarterly sales report (PDF)  
> **Claim**: "Our Q3 revenue increased by 25% compared to Q2"  
> **Result**: FALSE — According to the report, Q3 revenue was $2.1M vs Q2's $1.9M, which is an 10.5% increase, not 25%.

---

## 🏗️ Architecture

The system is divided into **4 layers**:

```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
│   Upload UI • Claim Input • Results Display             │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                    API / BACKEND                        │
│   FastAPI • Request Routing • Response Formatting       │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
┌───────────────────┐             ┌───────────────────┐
│    DATA LAYER     │             │    NLP LAYER      │
│ PDF/Text/Image    │────────────▶│ Gemini API        │
│ Parsing & Chunking│             │ Contradiction     │
│                   │             │ Detection Logic   │
└───────────────────┘             └───────────────────┘
```

| Layer           | Responsibility                              | Key Tech                  |
| --------------- | ------------------------------------------- | ------------------------- |
| **Frontend**    | User interface for uploads and results      | React/Next.js             |
| **Data Layer**  | Document parsing, text extraction, chunking | PyPDF2, Tesseract         |
| **NLP Layer**   | Semantic analysis, claim verification       | Google Gemini API, Python |
| **API/Backend** | REST endpoints, orchestration               | FastAPI                   |

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **LLM**: Google Gemini API (free tier)
- **Backend**: FastAPI
- **Frontend**: React / Next.js
- **Document Processing**: PyPDF2, pdf2image, pytesseract
- **Vector Search** (optional): Sentence Transformers, FAISS

---

## 📁 Project Structure

```
contradiction-detection-system/
├── README.md
├── docs/
│   ├── 01_conceptual_framework.md    # What & Why
│   ├── 02_technical_architecture.md  # How (system design)
│   └── 04_nlp_layer_implementation.md # NLP Layer guide (step-by-step)
├── frontend/                          # React app (TBD)
├── backend/                           # FastAPI server (TBD)
│   ├── api/                          # API routes
│   ├── data_layer/                   # Document processing
│   └── nlp_layer/                    # Contradiction detection
└── tests/                            # Test cases
```

---

## 👥 Team Division

| Part          | Owner   | Description                              |
| ------------- | ------- | ---------------------------------------- |
| Frontend      | Sushant | Upload interface, results display        |
| Data Layer    | Binisha  | PDF/text/image parsing and preprocessing |
| NLP Layer     | Anam    | Claim verification using Gemini API      |
| API/Backend   | Krishom | FastAPI endpoints and orchestration      |

---

## 📚 Documentation

- [Conceptual Framework](docs/01_conceptual_framework.md) — Problem definition, contradiction types, use cases
- [Technical Architecture](docs/02_technical_architecture.md) — System design, data flow, API specs
- [NLP Layer Implementation Guide](docs/04_nlp_layer_implementation.md) — Step-by-step learning guide for NLP layer

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/your-org/contradiction-detection-system.git

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up Gemini API key
export GEMINI_API_KEY="your-api-key"  # On Windows: set GEMINI_API_KEY=your-api-key

# Run the backend
uvicorn backend.main:app --reload
```

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.
