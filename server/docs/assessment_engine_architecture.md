# CAREER COMPASS AI — ROLE-AWARE ASSESSMENT ENGINE ARCHITECTURE

> **Explicit Architectural Statement**: *"The current assessment engine uses a deterministic question pool and does not dynamically generate questions using an LLM."*

---

## 1. Role-Aware & Priority Question Selection Strategy

The mock assessment engine selects questions based on a 4-tier priority hierarchy:

1. **Missing Required Skills** (50–60% of question quota): Questions associated with skills required by the target role that are missing from the candidate's resume.
2. **Missing Preferred Skills** (20–30% of quota): Questions associated with preferred role skills missing from the candidate's resume.
3. **Existing Strengths & Target Role Skills** (10–20% of quota): Questions validating skills already identified in the candidate's resume to ensure solid foundational mastery.
4. **Negated Skills Exclusion**: Skills classified as negated in Phase 5 (`"Docker is not required"`) are strictly excluded from generating assessment requirements.

---

## 2. Difficulty Adjustment Strategy

- **High Previous Attempt Score ($\ge 75\%$)**: Prioritizes `Medium` and `Hard` questions to challenge the candidate.
- **Low Previous Attempt Score ($< 50\%$)**: Prioritizes `Easy` and `Medium` questions for foundational evaluation.
- **Initial / No Previous Attempt**: Uses a balanced distribution (`Easy` / `Medium` / `Hard`).

---

## 3. Assessment Evaluation & Metric Separation

- **Assessment Score**:
  $$\text{Assessment Score} = \frac{\text{Total Correct Answers}}{\text{Total Questions}} \times 100$$
- **Metric Isolation**: The Mock Assessment Score remains **completely separate** from the ATS Score.
- **Skill-Wise Performance**: Exposes individual skill percentages (`score`), attempted count (`total`), correct count (`correct`), required flag (`isRequired`), and performance state (`strong` $\ge 75\%$, `moderate` $50-74\%$, `weak` $< 50\%$).
- **Explainable Feedback**: Generates natural data-driven result explanations (e.g. *"Overall score: 75%. Strong performance in: Python, SQL. Improvement needed in: FastAPI, Docker."*).
