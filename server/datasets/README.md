# CAREER COMPASS AI — DATASET & TAXONOMY FOUNDATION

## 1. Purpose
This directory contains the dataset foundation and schema definitions for future Natural Language Processing (NLP) and Machine Learning (ML) model training and fine-tuning within the Career Compass AI system.

> **Note**: No machine learning models are trained or deployed in this phase. The current Career Compass AI engine operates using a deterministic, rule-based heuristic parser with an expanded skill taxonomy. This dataset directory establishes standardized schemas for future empirical datasets.

---

## 2. Dataset Categories & Directory Structure

```
server/datasets/
├── README.md                           # Comprehensive dataset documentation & guidelines
├── skills/
│   └── sample_skill_schema.json        # Schema & taxonomy entry format for technical skills
├── resumes/
│   └── sample_resume_schema.json       # Schema for parsed resume documents
├── job_descriptions/
│   └── sample_jd_schema.json           # Schema for analyzed job description documents
└── resume_jd_pairs/
    └── sample_pair_schema.json         # Schema for resume-to-JD match ground truth pairs
```

---

## 3. Dataset Schemas Overview

### A. Skill Taxonomy Dataset (`skills/`)
Defines technical skills, hierarchical relationships, parent skills, canonical aliases, and skill types (technical, soft, process).

### B. Resume Corpus Dataset (`resumes/`)
Defines structured resume representations including extracted sections, detected skills, experience years, education degrees, and impact metrics.

### C. Job Description Corpus Dataset (`job_descriptions/`)
Defines structured job posting representations including required skills, preferred skills, experience bounds, and domain classifications.

### D. Resume–JD Match Dataset (`resume_jd_pairs/`)
Defines ground-truth relevance pairs for fine-tuning semantic matching models, ATS compatibility scores, and skill overlap labels.

---

## 4. Training / Validation / Test Split Strategy

When empirical datasets are introduced in future phases, data partitioning MUST strictly follow standard machine learning practices:
- **Train Set**: 70% of annotated records (used for model parameter optimization / fine-tuning).
- **Validation Set**: 15% of annotated records (used for hyperparameter tuning & early stopping).
- **Test Set**: 15% of annotated records (held-out set for final evaluation metrics: Precision, Recall, F1-Score).

---

## 5. Privacy, Ethics & Data Governance

1. **Personally Identifiable Information (PII) Stripping**:
   - All resume samples MUST be completely anonymized prior to inclusion.
   - Names, email addresses, phone numbers, physical addresses, candidate URLs, and company names MUST be scrubbed or replaced with generic placeholders (e.g. `[CANDIDATE_NAME]`, `[EMAIL]`).
2. **User Data Confidentiality**:
   - Live production user resumes uploaded to Career Compass AI MUST NOT be written to training datasets without explicit user opt-in consent.
3. **Licensing**:
   - Any external datasets incorporated in future phases MUST hold permissive open-source licenses (e.g. CC-BY 4.0, MIT, Apache 2.0).

---

## 6. Annotation Guidelines

- **Skill Entities**: Annotated using BIO (Begin, Inside, Outside) named entity tagging for NER models.
- **Match Labels**: Ranked on a 4-point scale: `0` (Unsuited), `1` (Weak Fit), `2` (Moderate Fit), `3` (Strong Fit).

---

## 7. Future NLP / ML Upgrade Pipeline

```
Raw Text Input → Tokenization → Named Entity Recognition (NER) → Dense Vector Embedding → Cosine Similarity / ATS Score
```
- Current System: Industry-inspired ATS compatibility analysis engine via rule-based normalization.
- Future Upgrade: Hybrid Rule-Based + Vector Embedding Semantic Match Engine.
