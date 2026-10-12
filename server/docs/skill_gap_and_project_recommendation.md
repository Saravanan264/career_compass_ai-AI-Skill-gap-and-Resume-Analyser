# CAREER COMPASS AI — SKILL GAP ANALYSIS & PROJECT RECOMMENDATION ARCHITECTURE

> **Disclaimer**: This system provides deterministic, explainable skill-gap analysis and project recommendations. It does **NOT** rely on external black-box LLM APIs.

---

## 1. Skill Gap Classification Taxonomy

Every candidate-job skill pair is categorized into 1 of 7 explicit match states:

1. **Matched Required Skill**: Candidate has exact canonical skill required by JD (`matchType: "exact"`, status = `"match"`).
2. **Missing Required Skill**: Skill required by JD but absent in candidate resume (`priority: "high"`, `gapSeverity: 100`, status = `"missing"`).
3. **Matched Preferred Skill**: Candidate has optional skill preferred by JD.
4. **Missing Preferred Skill**: Optional skill preferred by JD but missing (`priority: "medium"`, `gapSeverity: 50`, status = `"missing"`).
5. **Related Skill**: Candidate possesses a child or parent skill in the taxonomy (e.g. candidate has `PostgreSQL`, JD requires `SQL` $\rightarrow$ `matchType: "related"`).
6. **Semantic Match**: Phase 4 SentenceTransformers vector similarity identifies contextual alignment.
7. **Negated / Excluded Skill**: Phase 5 negated skills (`"Docker is not required"`) are strictly excluded from mandatory skill gap calculations.

---

## 2. Priority & Gap Severity Formula

- **Missing Required Skill**: `Priority = HIGH`, `Gap Severity = 100`
- **Missing Preferred Skill**: `Priority = MEDIUM`, `Gap Severity = 50`
- **Secondary Improvement Skill**: `Priority = LOW`, `Gap Severity = 25`

---

## 3. Project Recommendation Ranking Engine

### Formula:
$$\text{Project Score} = \text{Covered Required Gaps} \times 35 + \text{Covered Preferred Gaps} \times 20 + \text{Total Gap Coverage} \times 10 + \text{Multi-Skill Bonus (20 pts)}$$

### Key Deterministic Rules:
1. **Required Skill Primacy**: Projects covering missing required skills receive 1.75x weight compared to preferred skills.
2. **Multi-Skill Value**: Projects covering $\ge 2$ missing gaps receive a +20 point bonus.
3. **Irrelevant Filtering**: Projects covering 0 target role gaps are filtered out.
4. **Explainable Reasoning**: Every recommendation includes a natural, data-driven explanation string:
   > *"Recommended because it addresses 2 high-priority missing required gaps: FastAPI and Docker."*
