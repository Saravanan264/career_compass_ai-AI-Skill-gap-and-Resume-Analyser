# CAREER COMPASS AI — ADAPTIVE ROADMAP & LONGITUDINAL SKILL PROGRESS ARCHITECTURE

> **Explicit Architectural Statement**: *"The current adaptive roadmap uses deterministic rules based on resume analysis, job requirements, skill gaps, assessment performance and historical progress. It does not use predictive machine learning or LLM-generated learning plans."*

---

## 1. Skill Progress Model & Historical Tracking

For each relevant skill, the system tracks:
- `skill`: Canonical skill name (e.g. `"FastAPI"`).
- `requirement`: `"required"` | `"preferred"` | `"none"`.
- `resumeStatus`: `"matched"` | `"missing"`.
- `latestAssessmentScore`: `number | null` (from the most recent assessment attempt).
- `previousAssessmentScore`: `number | null` (from the preceding attempt, `null` if $< 2$ attempts).
- `improvement`: `latestAssessmentScore - previousAssessmentScore` (`null` if $< 2$ attempts).
- `attemptCount`: `number` of assessment attempts evaluating this skill.
- `status`:
  - `Weak`: Latest score $< 50\%$
  - `Developing`: Latest score $50-69\%$
  - `Strong`: Latest score $\ge 70\%$
  - `Not Assessed`: No assessment history for this skill
- `trend`:
  - `improving`: $\text{Improvement} > +5\%$
  - `declining`: $\text{Improvement} < -5\%$
  - `stable`: $-5\% \le \text{Improvement} \le +5\%$
  - `Not Enough Data`: $< 2$ attempts

---

## 2. Deterministic Improvement Calculation

$$\text{Improvement} = \text{Latest Skill Score} - \text{Previous Skill Score}$$

- **Single Attempt Rule**: When a skill has only 1 assessment attempt, `previousScore` is `null` and `improvement` is `null`. First attempt performance is never misrepresented as an improvement trend.

---

## 3. Adaptive Roadmap Logic & Stage Re-Prioritization

Roadmap stages dynamically adapt based on real-time candidate assessment performance:

- **Stage 1: Core Foundation & High-Priority Required Gaps (`High` Priority)**
  - Focuses on missing required skills where the latest assessment score is $< 70\%$ or `"Not Assessed"`.
  - Generates data-driven priority explanations (e.g., *"Prioritized because FastAPI & Docker are required skills missing from resume with assessment scores below threshold (<70%)."*).
- **Stage 2: Applied Projects & Preferred Skill Enhancement (`Medium` Priority)**
  - Focuses on missing preferred skills and integrates Phase 7 recommended practical projects into stage project milestones.
- **Stage 3: Reassessment Validation & Career Readiness (`Low` Priority)**
  - Encourages re-evaluation of developed/strong skills to verify retention and score progression.

---

## 4. Mastery & Completion Rule

- A skill is classified as **Strong** once its latest assessment score reaches $\ge 70\%$.
- Once a missing required skill achieves **Strong** status, it automatically leaves the Stage 1 high-priority gap list, transferring focus to remaining unresolved gaps without deleting historical tasks.
