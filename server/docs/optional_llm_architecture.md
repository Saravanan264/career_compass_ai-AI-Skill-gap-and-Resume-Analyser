# CAREER COMPASS AI — OPTIONAL LLM ARCHITECTURE

> **Core Architectural Principle**: *"The LLM is an optional natural-language enhancement layer. Core Career Compass AI decisions remain deterministic and explainable."*

---

## 1. Why the LLM is Optional
The core Career Compass AI application relies strictly on deterministic heuristics, rule-based algorithms, and pre-trained sentence transformer embeddings (`all-MiniLM-L6-v2`) for ATS scoring, resume-job matching, skill gap classification, mock assessment generation, and longitudinal roadmap adaptation.

The optional LLM layer exists solely to provide human-readable textual explanations and personalized summaries for candidates without deciding scores or priorities.

---

## 2. Provider Abstraction
The backend service abstraction (`server/services/llm_service.py`) encapsulates all external LLM interactions. It supports HTTP-based completion formats (e.g. OpenAI / compatible endpoints) and isolates API call details from the rest of the application.

---

## 3. Environment Configuration
The LLM layer is controlled entirely via environment variables in `server/.env`:

```env
LLM_ENABLED=false
LLM_PROVIDER=openai
LLM_API_KEY=
LLM_MODEL=gpt-4o-mini
```

When `LLM_ENABLED=false` or `LLM_API_KEY` is empty/missing, the system operates seamlessly in 100% deterministic mode without throwing errors.

---

## 4. Supported Use Cases & Deterministic Fallback

| Feature | LLM Task | Deterministic Fallback Output |
| :--- | :--- | :--- |
| **Resume ATS Feedback** | Natural-language resume advice | Structured bullet points based on missing keywords and formatting scores |
| **Skill Gap Explanation** | Contextual explanation of why a skill matters | Rule-based description citing target JD requirement status |
| **Roadmap Rationale** | Natural-language explanation of stage ordering | Rule-based rationale citing required vs. preferred priority |

---

## 5. Security & Privacy
- **Zero API Key Leakage**: API keys are accessed strictly on the backend and never exposed to the client, logged, or returned in API payloads.
- **Privacy Preservation**: No passwords, tokens, hashes, or unnecessary personally identifiable information (PII) are transmitted to external services.
- **Input Sanitization**: Requests send only essential non-sensitive context (e.g., target role, skill names, score metrics).

---

## 6. Academic Classification & Terminology
- **Rule-based Processing**: ATS scoring, skill taxonomy matching, skill gap priority ranking, mock assessment question selection.
- **Pre-trained Embeddings**: SentenceTransformer semantic vector matching (`all-MiniLM-L6-v2`).
- **Optional LLM Layer**: Natural-language text generation and feedback enhancement.
