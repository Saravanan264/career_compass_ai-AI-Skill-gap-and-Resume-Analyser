# CAREER COMPASS AI — ADVANCED SKILL TAXONOMY & JD NLP ANALYSIS

## 1. Executive Summary
Phase 5 enhances the Career Compass AI platform with advanced skill taxonomy normalization, explicit relationship modeling, and deterministic Job Description NLP extraction (negation detection, structured experience ranges, education extraction, and dynamic skill categorization).

---

## 2. Taxonomy Definitions & Canonical Rules

### Key Definitions:
1. **Canonical Skill**: The authoritative standard name for a technical concept (e.g. `React`, `Node.js`, `PostgreSQL`, `Scikit-learn`).
2. **Alias**: Alternate spellings, acronyms, or historical naming conventions mapped to a single canonical skill (e.g. `React.js` / `ReactJS` $\rightarrow$ `React`).
3. **Skill Category**: Standardized technical domain grouping (`Programming Languages`, `Frontend Frameworks`, `Backend Frameworks`, `Databases`, `Cloud Technologies`, `DevOps`, `Machine Learning`, `NLP`, `Generative AI`, `Tools`, `Soft Skills`).
4. **Skill Type**: Structural classification (`technical`, `soft`, `process`).
5. **Parent Skill**: Higher-level foundational technology or domain.
   - Example: `PostgreSQL` $\rightarrow$ Parent: `SQL`.
   - Example: `TypeScript` $\rightarrow$ Parent: `JavaScript`.
   - Example: `Scikit-learn` $\rightarrow$ Parent: `Python`.
   - Example: `LLM` $\rightarrow$ Parent: `Generative AI`.

---

## 3. Match Relationship Classifications

- **Exact Canonical Match**: The resume skill and JD required skill map to the identical canonical skill (e.g., `React.js` vs `ReactJS` $\rightarrow$ Match = `TRUE`).
- **Related / Parent Category Match**: The resume candidate possesses a specific technology under a required parent category (e.g., Candidate has `PostgreSQL` when JD specifies general `SQL`).
- **Semantic Vector Match**: High contextual document similarity detected by Phase 4 SentenceTransformer / TF-IDF engine even when keyword strings differ.

---

## 4. Job Description NLP Extraction Engine

### A. Requirement Classification & Negation Handling
- **Required**: Skills identified under mandatory clauses (`"required"`, `"must have"`, `"essential"`, `"mandatory"`).
- **Preferred**: Skills under optional clauses (`"preferred"`, `"nice to have"`, `"plus"`, `"desirable"`).
- **Negated / Excluded**: Detects phrases like `"not required"`, `"no experience needed"`. (e.g., *"Docker is not required"* prevents Docker from being listed as a mandatory skill gap).

### B. Structured Experience Extraction
- Parses min/max year bounds and classifies seniority:
  - Range parsing: `"2-4 years"` $\rightarrow$ `min: 2, max: 4, level: "Mid Level"`.
  - Open-ended parsing: `"3+ years"` $\rightarrow$ `min: 3, max: null, level: "Mid Level"`.
  - Entry level / Internships: `"freshers can apply"` $\rightarrow$ `min: 0, max: 1, level: "Entry Level"`.

### C. Structured Education Extraction
- Identifies degrees (`B.Tech`, `B.E.`, `B.Sc`, `M.Tech`, `Master's`, `PhD`) and recognized majors (`Computer Science`, `IT`, `AI`, `Data Science`).
