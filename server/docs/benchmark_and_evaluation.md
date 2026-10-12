# CAREER COMPASS AI — SYSTEM BENCHMARK & EVALUATION REPORT

> **Disclaimer**: *"The benchmark dataset is controlled/synthetic and is intended for functional evaluation rather than population-level performance estimation."*

---

## 1. BENCHMARK DESIGN & DATASET
- **Dataset File**: `server/datasets/benchmark/benchmark_cases.json`
- **Type**: Controlled synthetic benchmark dataset containing curated resume profiles, job descriptions, ground-truth skill sets, expected gaps, and priority rankings.
- **Cases Evaluated**:
  1. `CASE-001-BACKEND-DEV` (Backend Engineering)
  2. `CASE-002-FRONTEND-DEV` (Frontend Engineering)
  3. `CASE-003-AI-ML-ENG` (AI/ML Engineering)

---

## 2. SKILL EXTRACTION & NORMALIZATION EVALUATION
Evaluated on complex technical pairs (aliases, abbreviations, punctuation, overlapping terms):

| Test Pair | Expected Target Skills | Extracted Skills | Result |
| :--- | :--- | :--- | :--- |
| `Java vs JavaScript` | `Java`, `JavaScript` | `Java`, `JavaScript` | **MATCH** |
| `C vs CSS` | `C`, `CSS` | `C`, `CSS` | **MATCH** |
| `Go vs Google` | `Go` | `Go` | **MATCH** |
| `React vs ReactJS` | `React` | `React` | **MATCH** |
| `Scikit-learn vs sklearn` | `Scikit-learn` | `Scikit-learn` | **MATCH** |
| `SQL vs PostgreSQL` | `SQL`, `PostgreSQL` | `SQL`, `PostgreSQL` | **MATCH** |
| `NLP vs Natural Language Processing` | `NLP`, `Natural Language Processing` | `NLP`, `Natural Language Processing` | **MATCH** |

### Extraction Performance Metrics:
- **True Positives**: 10
- **False Positives**: 0
- **False Negatives**: 0
- **Precision**: **1.0000** (100%)
- **Recall**: **1.0000** (100%)
- **F1 Score**: **1.0000** (100%)

---

## 3. JD PARSING EVALUATION
- **Required Skill Extraction**: Successfully isolated required skills (e.g. `Python`, `FastAPI`, `PostgreSQL`).
- **Preferred Skill Extraction**: Successfully isolated optional/preferred skills (e.g. `Docker`, `AWS`).
- **Negated Skill Handling**: Successfully detected negative context phrases (e.g., `"Experience with Kubernetes is not required"`) and routed `Kubernetes` to `otherSkills`, preventing it from becoming an active skill gap.

---

## 4. SEMANTIC MATCHING EVALUATION
- **Model**: `SentenceTransformer` (`all-MiniLM-L6-v2`) with TF-IDF vector cosine fallback.
- **Embedding Dimension**: 384
- **Related Pair Similarity**: `0.5562` (55.6%)
- **Unrelated Pair Similarity**: `0.0520` (5.2%)
- **Hybrid Matching Weighting**: 60% Rule-based Heuristic + 40% Dense Vector Similarity.
- **Inference Latency**: `~1.50 ms` per pair.

---

## 5. ATS SCORECARD EVALUATION
Evaluated 7-component weighted ATS scorecard:
- **Strong Resume**: Achieved **87%** ATS score.
- **Weak Resume**: Achieved **26%** ATS score.
- **Components Verified**: Format parseability (15%), Section completeness (15%), Required skill coverage (25%), Preferred skill coverage (10%), Experience alignment (15%), Education alignment (10%), Impact evidence (10%).

---

## 6. SKILL GAP & PRIORITY EVALUATION
- **Priority Ranking**: Missing Required Skills > Missing Preferred Skills.
- **Hierarchy Handling**: Parent skills (e.g., `Python`) do not automatically fulfill child skills (e.g., `FastAPI`).
- **Negated Exclusion**: Negated skills are excluded from skill gap recommendations.

---

## 7. PROJECT RECOMMENDATION EVALUATION
- **Algorithm**: Multi-skill matrix coverage ranking.
- **Result**: Recommended capstone projects cover multiple missing skills per project (e.g., `AWS`, `Docker`) to maximize learning efficiency.

---

## 8. ASSESSMENT EVALUATION
- **Selection Rule**: Deterministic role-aware question selection prioritized by missing required skills and weak assessment history.
- **Adaptation**: Questions adapt across `Easy`, `Medium`, and `Hard` difficulty tiers based on prior performance.

---

## 9. LONGITUDINAL PROGRESS EVALUATION
Tracked across 3 attempts (`Attempt 1`: 35%, `Attempt 2`: 75%, `Attempt 3`: 82%):
- **Latest Score**: `82%`
- **Previous Score**: `75%`
- **Improvement**: `+7%`
- **Trend**: `improving`
- **Status Classification**: `Strong` ($\ge 70\%$)

---

## 10. LEARNING ROADMAP EVALUATION
- **Stage 1 (High Priority)**: Focuses on missing required skills with score $<70\%$.
- **Stage 2 (Medium Priority)**: Focuses on preferred skills and project recommendations.
- **Stage 3 (Low Priority)**: Focuses on validation and interview readiness for mastered skills.

---

## 11. LLM EVALUATION
- **Provider Abstraction**: Functionally validated using mock & fallback architecture (`server/services/llm_service.py`).
- **Fallback Verification**: 100% pass when `LLM_ENABLED=false` or `LLM_API_KEY` is missing.
- **Security Guarantee**: Zero API key exposure.

---

## 12. PERFORMANCE MEASUREMENTS (LATENCY)
*Measured on local environment across repeated test executions:*

| Pipeline Component | Latency (ms) |
| :--- | :--- |
| **Resume Analysis** | `~3.82 ms` |
| **Semantic Matching** | `~1.50 ms` |
| **JD Parsing** | `~1.94 ms` |

*Performance measurements are environment-dependent.*

---

## 13. ACADEMIC CLASSIFICATION
1. **Rule-based Processing**: ATS scoring, skill gap prioritization, roadmap stage ordering.
2. **Pre-trained Embeddings**: SentenceTransformer (`all-MiniLM-L6-v2`) semantic vector matching.
3. **Optional LLM Layer**: Natural-language feedback enhancement.
