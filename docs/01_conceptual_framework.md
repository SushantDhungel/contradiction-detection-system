# Contradiction Detection System

## Conceptual Framework & Methodology

---

## Executive Summary

The **Contradiction Detection System** is an AI-powered tool that verifies claims and statements against source documents. Users upload a document (PDF, text, or image) and input a claim to check. The system analyzes the source, extracts relevant information, and determines whether the claim is supported, contradicted, or cannot be verified based on the available evidence.

---

## 1. Core Concept: Contradiction Detection

### 1.1 Definition

**Contradiction Detection** is the process of:

1. **Parsing** a source document to extract factual information
2. **Analyzing** a user-provided claim or statement
3. **Comparing** the claim against the extracted information
4. **Returning** a verdict with supporting evidence

```mermaid
graph LR
    A[Source Document] -->|Parse & Extract| B[Factual Information]
    C[User Claim] -->|Analyze| D[Claim Components]

    B --> E{Compare}
    D --> E

    E -->|Match| F[✅ TRUE]
    E -->|Conflict| G[❌ FALSE]
    E -->|Partial| H[⚠️ PARTIALLY TRUE]
    E -->|Insufficient Data| I[❓ CANNOT DETERMINE]

    style F fill:#4caf50,color:#fff
    style G fill:#f44336,color:#fff
    style H fill:#ff9800,color:#fff
    style I fill:#9e9e9e,color:#fff
```

### 1.2 Why This Matters

```mermaid
mindmap
  root((Contradiction Detection))
    Business Applications
      Verify sales reports
      Audit financial claims
      Check marketing statements
      Validate press releases
    Academic & Research
      Fact-check papers
      Verify citations
      Cross-reference sources
      Literature review
    Legal & Compliance
      Contract verification
      Regulatory compliance
      Evidence analysis
      Due diligence
    Media & Journalism
      Fact-checking
      Source verification
      Quote validation
      News accuracy
```

### 1.3 Types of Contradictions

```mermaid
graph TD
    A[Contradiction Types] --> B[Factual Contradiction]
    A --> C[Numerical Contradiction]
    A --> D[Temporal Contradiction]
    A --> E[Logical Contradiction]
    A --> F[Contextual Contradiction]

    B --> B1["Claim: 'CEO is John Smith'<br/>Source: 'CEO is Jane Doe'"]
    C --> C1["Claim: 'Revenue was $5M'<br/>Source: 'Revenue was $3.2M'"]
    D --> D1["Claim: 'Launched in 2023'<br/>Source: 'Launched in 2024'"]
    E --> E1["Claim: 'All products are organic'<br/>Source: 'Some contain additives'"]
    F --> F1["Claim: 'Best quarter ever'<br/>Source: 'Q2 2022 was higher'"]

    style B fill:#e3f2fd
    style C fill:#e3f2fd
    style D fill:#e3f2fd
    style E fill:#e3f2fd
    style F fill:#e3f2fd
```

| Type           | Description                  | Example                                     |
| -------------- | ---------------------------- | ------------------------------------------- |
| **Factual**    | Direct factual mismatch      | Names, events, locations                    |
| **Numerical**  | Numbers don't match          | Revenue, percentages, counts                |
| **Temporal**   | Dates/times conflict         | Launch dates, deadlines                     |
| **Logical**    | Logical inconsistency        | "All X are Y" vs "Some X are not Y"         |
| **Contextual** | Misrepresentation of context | Cherry-picked stats, misleading comparisons |

---

## 2. System Workflow

### 2.1 High-Level Flow

```mermaid
flowchart TD
    Start([User Input]) --> Upload[Upload Source Document]
    Upload --> Parse{Document Type?}

    Parse -->|PDF| PDF[PDF Parser]
    Parse -->|Text| TXT[Text Parser]
    Parse -->|Image| IMG[OCR Engine]

    PDF --> Extract[Extract Text Content]
    TXT --> Extract
    IMG --> Extract

    Extract --> Chunk[Split into Chunks]
    Chunk --> Embed[Generate Embeddings]

    Start --> Claim[Enter Claim/Statement]
    Claim --> ClaimEmbed[Embed Claim]

    Embed --> Search[Semantic Search]
    ClaimEmbed --> Search

    Search --> Context[Retrieve Relevant Context]
    Context --> LLM[Send to Gemini API]
    Claim --> LLM

    LLM --> Analyze[Analyze Claim vs Context]
    Analyze --> Verdict[Generate Verdict]

    Verdict --> Output([Return Result])

    style Start fill:#e1f5ff
    style Output fill:#4caf50,color:#fff
    style LLM fill:#ff9800,color:#fff
```

### 2.2 Detailed Processing Pipeline

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant DataLayer
    participant NLPLayer
    participant Gemini

    User->>Frontend: Upload document + Enter claim
    Frontend->>API: POST /verify {document, claim}

    API->>DataLayer: Process document
    DataLayer->>DataLayer: Parse PDF/Text/Image
    DataLayer->>DataLayer: Extract text
    DataLayer->>DataLayer: Chunk text
    DataLayer-->>API: Return chunks[]

    API->>NLPLayer: Find relevant context
    NLPLayer->>NLPLayer: Embed claim
    NLPLayer->>NLPLayer: Semantic search in chunks
    NLPLayer-->>API: Return relevant_context[]

    API->>NLPLayer: Verify claim
    NLPLayer->>Gemini: Send prompt (claim + context)
    Gemini-->>NLPLayer: Return analysis
    NLPLayer->>NLPLayer: Parse response
    NLPLayer-->>API: Return verdict + explanation

    API-->>Frontend: JSON response
    Frontend-->>User: Display result
```

---

## 3. Core Components

### 3.1 Data Layer

The Data Layer handles all document processing:

```mermaid
flowchart LR
    subgraph Input["Input Types"]
        PDF[PDF Files]
        TXT[Text Files]
        IMG[Images]
    end

    subgraph Processing["Processing Pipeline"]
        P1[File Validation]
        P2[Content Extraction]
        P3[Text Cleaning]
        P4[Chunking]
    end

    subgraph Output["Output"]
        O1[Clean Text Chunks]
        O2[Metadata]
    end

    Input --> P1 --> P2 --> P3 --> P4 --> Output

    style Input fill:#e1f5ff
    style Processing fill:#fff4e1
    style Output fill:#e1ffe1
```

**Responsibilities:**

- Parse PDF documents (PyPDF2, pdfplumber)
- Extract text from images (Tesseract OCR)
- Clean and normalize text
- Split text into manageable chunks
- Preserve metadata (page numbers, sections)

### 3.2 NLP Layer

The NLP Layer performs the core intelligence:

```mermaid
flowchart TD
    subgraph Inputs["Inputs"]
        I1[Text Chunks from Data Layer]
        I2[User Claim]
    end

    subgraph Processing["NLP Processing"]
        P1[Embed Text Chunks]
        P2[Embed Claim]
        P3[Semantic Search]
        P4[Context Retrieval]
        P5[Prompt Construction]
        P6[LLM Call - Gemini API]
        P7[Response Parsing]
    end

    subgraph Output["Output"]
        O1[Verdict: TRUE/FALSE/etc]
        O2[Explanation]
        O3[Evidence Excerpts]
        O4[Confidence Score]
    end

    Inputs --> Processing --> Output

    style Processing fill:#fff4e1
    style Output fill:#4caf50,color:#fff
```

**Responsibilities:**

- Generate embeddings for semantic search
- Find relevant context for the claim
- Construct effective prompts for the LLM
- Call Google Gemini API
- Parse and structure the response
- Handle edge cases and errors

### 3.3 API/Backend Layer

```mermaid
flowchart LR
    subgraph Endpoints["API Endpoints"]
        E1[POST /upload]
        E2[POST /verify]
        E3[GET /status]
        E4[GET /history]
    end

    subgraph Services["Services"]
        S1[Document Service]
        S2[Verification Service]
        S3[Storage Service]
    end

    subgraph External["External"]
        X1[Gemini API]
        X2[File Storage]
    end

    Endpoints --> Services --> External

    style Endpoints fill:#e1f5ff
    style Services fill:#fff4e1
    style External fill:#ffe1f5
```

### 3.4 Frontend Layer

```mermaid
flowchart TD
    subgraph UI["User Interface"]
        U1[Document Upload]
        U2[Claim Input Field]
        U3[Submit Button]
        U4[Results Display]
        U5[History View]
    end

    subgraph States["UI States"]
        S1[Idle]
        S2[Uploading]
        S3[Processing]
        S4[Displaying Results]
        S5[Error]
    end

    U1 --> S2
    S2 --> U2
    U2 --> U3
    U3 --> S3
    S3 --> S4
    S4 --> U4

    style UI fill:#e1f5ff
    style S4 fill:#4caf50,color:#fff
```

---

## 4. Verification Logic

### 4.1 Verdict Categories

```mermaid
graph TB
    Verdicts[Possible Verdicts] --> TRUE
    Verdicts --> FALSE
    Verdicts --> PARTIAL[PARTIALLY TRUE]
    Verdicts --> CANNOT[CANNOT DETERMINE]

    TRUE --> T1["The claim is fully supported<br/>by the source document"]
    FALSE --> F1["The claim directly contradicts<br/>information in the source"]
    PARTIAL --> P1["Some aspects are true,<br/>others are false or exaggerated"]
    CANNOT --> C1["Insufficient information in<br/>the source to verify"]

    style TRUE fill:#4caf50,color:#fff
    style FALSE fill:#f44336,color:#fff
    style PARTIAL fill:#ff9800,color:#fff
    style CANNOT fill:#9e9e9e,color:#fff
```

### 4.2 Verification Decision Tree

```mermaid
flowchart TD
    Start[Claim Received] --> Q1{Relevant info<br/>found in source?}

    Q1 -->|No| CANNOT[❓ CANNOT DETERMINE]
    Q1 -->|Yes| Q2{Does claim match<br/>source info?}

    Q2 -->|Exact match| TRUE[✅ TRUE]
    Q2 -->|Complete mismatch| FALSE[❌ FALSE]
    Q2 -->|Partial match| Q3{Which parts<br/>are wrong?}

    Q3 -->|Minor details| PARTIAL_T[⚠️ PARTIALLY TRUE<br/>Minor inaccuracies]
    Q3 -->|Key facts| PARTIAL_F[⚠️ PARTIALLY TRUE<br/>Significant errors]

    TRUE --> Explain[Generate Explanation]
    FALSE --> Explain
    PARTIAL_T --> Explain
    PARTIAL_F --> Explain
    CANNOT --> Explain

    Explain --> Evidence[Cite Evidence]
    Evidence --> Confidence[Calculate Confidence]
    Confidence --> Result[Return Result]

    style TRUE fill:#4caf50,color:#fff
    style FALSE fill:#f44336,color:#fff
    style PARTIAL_T fill:#ff9800
    style PARTIAL_F fill:#ff9800
    style CANNOT fill:#9e9e9e,color:#fff
```

### 4.3 Confidence Scoring

```mermaid
graph LR
    subgraph Factors["Confidence Factors"]
        F1[Context Relevance]
        F2[Evidence Clarity]
        F3[Claim Specificity]
        F4[Source Quality]
    end

    subgraph Scoring["Confidence Levels"]
        S1[HIGH: 80-100%<br/>Clear evidence, direct match]
        S2[MEDIUM: 50-79%<br/>Indirect evidence, inference needed]
        S3[LOW: 0-49%<br/>Weak evidence, uncertain]
    end

    Factors --> Scoring

    style S1 fill:#4caf50,color:#fff
    style S2 fill:#ff9800
    style S3 fill:#f44336,color:#fff
```

---

## 5. Use Cases

### 5.1 Business: Sales Report Verification

```mermaid
sequenceDiagram
    participant Manager
    participant System
    participant Report as Sales Report PDF

    Manager->>System: Upload Q3 sales report
    Manager->>System: Claim: "Q3 revenue grew 25% YoY"

    System->>Report: Extract sales figures
    Report-->>System: Q3 2025: $4.2M, Q3 2024: $3.5M

    System->>System: Calculate: (4.2-3.5)/3.5 = 20%
    System->>System: Verdict: PARTIALLY TRUE

    System-->>Manager: "PARTIALLY TRUE - Revenue grew 20%, not 25%"

    Note over Manager,Report: Prevents overstated claims in presentations
```

### 5.2 Academic: Research Claim Verification

```mermaid
flowchart LR
    Paper[Research Paper] --> System
    Claim["Claim: 'Study found 90%<br/>effectiveness rate'"] --> System

    System --> Analysis{Analyze}

    Analysis --> Result["FALSE: Paper reports<br/>78% effectiveness (p. 12)"]

    style Result fill:#f44336,color:#fff
```

### 5.3 Legal: Contract Compliance

```mermaid
flowchart TD
    Contract[Contract PDF] --> System
    Statement["Vendor claims: 'We delivered<br/>all items by deadline'"] --> System

    System --> Check{Check Contract}

    Check --> Finding["Contract shows:<br/>- Deadline: March 15<br/>- Delivery: March 22"]

    Finding --> Verdict["FALSE: Delivery was<br/>7 days late"]

    style Verdict fill:#f44336,color:#fff
```

---

## 6. Technical Approach

### 6.1 Why Use an LLM (Gemini API)?

```mermaid
graph TB
    subgraph Traditional["Traditional Approach"]
        T1[Rule-based matching]
        T2[Keyword search]
        T3[Exact string match]
    end

    subgraph LLM["LLM Approach"]
        L1[Semantic understanding]
        L2[Context awareness]
        L3[Nuanced reasoning]
        L4[Natural language output]
    end

    subgraph Advantages["LLM Advantages"]
        A1["Understands paraphrasing<br/>'revenue' = 'sales' = 'income'"]
        A2["Handles implicit info<br/>Can infer from context"]
        A3["Explains reasoning<br/>Not just yes/no"]
        A4["Handles ambiguity<br/>Graceful uncertainty"]
    end

    Traditional --> Limited[Limited to exact matches]
    LLM --> Advantages

    style Traditional fill:#ffe1e1
    style LLM fill:#e1ffe1
    style Advantages fill:#4caf50,color:#fff
```

### 6.2 Chunking Strategy

```mermaid
flowchart TD
    Doc[Full Document<br/>10,000 words] --> Split[Split into Chunks]

    Split --> C1[Chunk 1<br/>~500 words]
    Split --> C2[Chunk 2<br/>~500 words]
    Split --> C3[Chunk 3<br/>~500 words]
    Split --> CN[Chunk N<br/>...]

    Claim[User Claim] --> Search[Semantic Search]
    C1 --> Search
    C2 --> Search
    C3 --> Search
    CN --> Search

    Search --> Top[Top 3-5 Relevant Chunks]
    Top --> LLM[Send to Gemini]
    Claim --> LLM

    LLM --> Response[Verification Result]

    style Split fill:#fff4e1
    style Search fill:#e1f5ff
    style LLM fill:#ff9800,color:#fff
```

**Why Chunk?**

- LLMs have token limits (~32K for Gemini)
- Large documents exceed these limits
- Chunking + semantic search finds relevant parts
- Only relevant context is sent to LLM = better results + lower cost

### 6.3 Prompt Engineering

The prompt sent to Gemini follows this structure:

```
┌─────────────────────────────────────────────────────────┐
│ SYSTEM INSTRUCTION                                      │
│ "You are a fact-checking assistant. Your job is to     │
│ verify claims against provided source text..."          │
├─────────────────────────────────────────────────────────┤
│ CONTEXT (from source document)                          │
│ "According to the Q3 report: Revenue was $4.2M..."     │
├─────────────────────────────────────────────────────────┤
│ CLAIM TO VERIFY                                         │
│ "Q3 revenue grew 25% compared to last year"            │
├─────────────────────────────────────────────────────────┤
│ OUTPUT FORMAT INSTRUCTION                               │
│ "Respond with: VERDICT, EXPLANATION, EVIDENCE"         │
└─────────────────────────────────────────────────────────┘
```

---

## 7. Success Metrics

### 7.1 System Performance

```mermaid
mindmap
  root((Success Metrics))
    Accuracy
      Correct verdicts rate
      False positive rate
      False negative rate
    Performance
      Response time < 5s
      Document processing time
      API latency
    User Experience
      Clear explanations
      Relevant evidence cited
      Actionable feedback
    Reliability
      Uptime > 99%
      Error handling
      Graceful degradation
```

### 7.2 Key Performance Indicators

| Metric                  | Target           | Description                   |
| ----------------------- | ---------------- | ----------------------------- |
| **Accuracy**            | >85%             | Correct verdict on test cases |
| **Response Time**       | <5s              | End-to-end verification       |
| **Context Relevance**   | >90%             | Retrieved chunks are relevant |
| **Explanation Quality** | User rating >4/5 | Clarity of explanations       |

---

## 8. Limitations & Edge Cases

### 8.1 Known Limitations

```mermaid
graph TB
    subgraph Limitations["System Limitations"]
        L1[Cannot verify opinions<br/>Only factual claims]
        L2[Relies on source quality<br/>Bad source = bad results]
        L3[Token limits<br/>Very long documents need chunking]
        L4[No external knowledge<br/>Only uses provided source]
        L5[Language support<br/>Best with English]
    end

    subgraph Mitigations["Mitigations"]
        M1[Detect and flag opinion claims]
        M2[Source quality scoring]
        M3[Smart chunking with overlap]
        M4[Clear scope communication]
        M5[Multi-language support roadmap]
    end

    L1 --> M1
    L2 --> M2
    L3 --> M3
    L4 --> M4
    L5 --> M5

    style Limitations fill:#ffe1e1
    style Mitigations fill:#e1ffe1
```

### 8.2 Edge Cases

| Edge Case                             | Handling                                            |
| ------------------------------------- | --------------------------------------------------- |
| Claim references info not in document | Return "CANNOT DETERMINE" with explanation          |
| Document is image-only                | Use OCR (may have accuracy issues)                  |
| Claim is vague/ambiguous              | Ask for clarification or flag uncertainty           |
| Multiple conflicting sources          | Note the conflict, don't make assumptions           |
| Numbers require calculation           | LLM can do basic math; complex calculations flagged |

---

## 9. Next Steps

```mermaid
gantt
    title Implementation Phases
    dateFormat  YYYY-MM

    section Phase 1: Foundation
    Set up project structure     :2026-02, 2w
    Implement Data Layer basics  :2026-02, 3w
    Implement NLP Layer basics   :2026-02, 3w

    section Phase 2: Core Features
    PDF parsing                  :2026-03, 2w
    Gemini API integration       :2026-03, 2w
    Basic verification flow      :2026-03, 2w

    section Phase 3: Integration
    API endpoints                :2026-04, 2w
    Frontend UI                  :2026-04, 3w
    End-to-end testing          :2026-04, 2w

    section Phase 4: Enhancement
    Image/OCR support           :2026-05, 2w
    Confidence scoring          :2026-05, 2w
    Performance optimization    :2026-05, 2w
```

---

## Appendix: Glossary

| Term                | Definition                                              |
| ------------------- | ------------------------------------------------------- |
| **Claim**           | A statement to be verified against a source             |
| **Source Document** | The PDF, text, or image containing factual information  |
| **Chunk**           | A segment of text from the source document              |
| **Embedding**       | A vector representation of text for semantic search     |
| **Semantic Search** | Finding relevant text based on meaning, not keywords    |
| **Verdict**         | The system's determination (TRUE/FALSE/etc.)            |
| **Context**         | Relevant excerpts from the source used for verification |
| **LLM**             | Large Language Model (e.g., Gemini, GPT)                |
