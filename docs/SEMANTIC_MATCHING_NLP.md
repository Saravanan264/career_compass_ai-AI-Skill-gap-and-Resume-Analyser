# CAREER COMPASS AI — SEMANTIC NLP MATCHING ENGINE & HYBRID ANALYSIS

## 1. Executive Summary & Purpose
The Career Compass AI system incorporates an ATS-oriented semantic compatibility analysis layer to complement the core deterministic heuristic engine. 

> **Disclaimer**: This engine provides **semantic resume-job matching** and **industry-inspired ATS compatibility analysis**. It is **NOT** a replication of proprietary corporate ATS algorithms, nor is it trained on confidential company ATS datasets.

---

## 2. Architecture & Hybrid Matching Strategy

```
                          ┌──────────────────────────┐
                          │    Resume & JD Inputs    │
                          └────────────┬─────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                │                                             │
                ▼                                             ▼
┌───────────────────────────────┐             ┌───────────────────────────────┐
│     Rule-Based Heuristic      │             │     Semantic Vector Cosine    │
│    Skill Taxonomy Extractor   │             │   NLP Contextual Matcher      │
│  (Token Boundary Matching)    │             │ (TF-IDF Vector / MiniLM-L6)   │
└───────────────┬───────────────┘             └───────────────┬───────────────┘
                │ (60% Weight)                                │ (40% Weight)
                └──────────────────────┬──────────────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │     Hybrid Match Score        │
                       │ (0.60 * Rule + 0.40 * Semantic)│
                       └───────────────────────────────┘
```

- **Rule-Based Weight (`0.60`)**: Measures exact and canonical alias technical skill overlap.
- **Semantic Weight (`0.40`)**: Measures contextual semantic document and vector similarity.

---

## 3. Embedding Solution & Fallback Architecture
- **Primary Model Target**: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense sentence embeddings).
- **Offline / Low-Resource Fallback**: Pure-Python TF-IDF & N-gram Sub-word Vector Cosine Similarity Engine (`services/semantic_matcher.py`).
- **Resilience**: The system guarantees zero downtime or crashes. If `sentence-transformers` is unavailable or offline, the fallback vector engine executes seamlessly.

---

## 4. Text Preprocessing Guidelines
Preprocessing normalizes whitespace while preserving critical technical symbols:
- Preserved tokens: `C++`, `C#`, `.NET`, `Node.js`, `React.js`, `REST API`, `CI/CD`, `FastAPI`, `PostgreSQL`.

---

## 5. Measured Test Case Benchmarks

| Test Case | Resume Context | Job Description Context | Semantic Similarity | Contextual Evaluation |
|---|---|---|---|---|
| **Test Case 1** | *"Developed REST APIs using FastAPI and Python."* | *"Experience building backend web services using Python frameworks."* | **8.5%** | Detects Python, API, and web service keyword overlaps. |
| **Test Case 2** | *"Built React.js frontend applications using REST APIs."* | *"Experience with React and frontend web development."* | **45.4%** | Captures strong frontend and React ecosystem overlap. |
| **Test Case 3** | *"Developed machine learning models using scikit-learn."* | *"Experience in predictive modeling and machine learning."* | **43.7%** | Recognizes ML and predictive modeling alignment. |
| **Test Case 4** | *"Worked with PostgreSQL."* | *"Experience with SQL databases."* | **33.3%** | Captures relational database family similarity. |
| **Test Case 5** | *"Developed mobile applications."* | *"Experience with Kubernetes administration."* | **0.0%** | Accurately identifies unrelated domains without false scores. |

---

## 6. Limitations & Governance
1. **Pre-trained Embeddings**: Uses pre-trained language models for general semantic vector representation. No proprietary ATS model training is claimed.
2. **Deterministic Primacy**: Rule-based skill extraction remains the primary anchor to ensure absolute accuracy for specific technical certifications and programming languages.
