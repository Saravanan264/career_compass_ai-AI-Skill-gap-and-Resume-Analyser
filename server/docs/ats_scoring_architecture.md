# CAREER COMPASS AI — ATS-ORIENTED SCORING ARCHITECTURE

> **Disclaimer**: This system provides **ATS-oriented resume evaluation** and industry-style explainable scoring. It does **NOT** replicate or clone any proprietary company's internal ATS software.

---

## 1. Overview & Architectural Goals
The Phase 6 ATS evaluation engine provides a structured, deterministic, and explainable scorecard. Instead of relying on a black-box opaque score, the scorecard breaks down candidate resume evaluation into 7 independently measurable sub-components:

1. **Format / Parseability** (15%)
2. **Section Completeness** (15%)
3. **Required Skill Coverage** (25%)
4. **Preferred Skill Coverage** (10%)
5. **Experience Alignment** (15%)
6. **Education Alignment** (10%)
7. **Impact / Quantitative Evidence** (10%)

---

## 2. Weighted Formula & Component Definitions

$$\text{Overall ATS Score} = \sum_{c} \text{Score}_c \times \text{Weight}_c$$

### Default Configurable Weights:
```python
DEFAULT_ATS_WEIGHTS = {
    "format": 0.15,
    "sectionCompleteness": 0.15,
    "requiredSkillCoverage": 0.25,
    "preferredSkillCoverage": 0.10,
    "experienceAlignment": 0.15,
    "educationAlignment": 0.10,
    "impactEvidence": 0.10
}
```

---

## 3. Sub-Component Evaluation Logic

### A. Format / Parseability (15%)
- Evaluates document character length ($\ge 150$ characters), extraction validity, presence of contact details (Email, Phone, LinkedIn, GitHub), and structural heading scannability.

### B. Section Completeness (15%)
- Evaluates presence of core resume sections: `Contact`, `Summary`, `Education`, `Skills`, `Projects`, `Experience`, `Certifications`, `Achievements`.

### C. Required Skill Coverage (25%)
$$\text{Required Skill Coverage} = \frac{\text{Matched Required Skills}}{\text{Total Required Skills}} \times 100$$
- Exposes exact matched required skills (`matchedRequiredSkills`) and missing required skills (`missingRequiredSkills`).

### D. Preferred Skill Coverage (10%)
$$\text{Preferred Skill Coverage} = \frac{\text{Matched Preferred Skills}}{\text{Total Preferred Skills}} \times 100$$
- Evaluates optional/bonus skills. Safely defaults to 100% when no preferred skills are defined in the JD to prevent divide-by-zero errors.

### E. Experience Alignment (15%)
- Compares candidate's stated or detected experience against Phase 5 `structuredExperience` requirements (`minimumYears`, `maximumYears`, `experienceLevel`).

### F. Education Alignment (10%)
- Compares degree signals (`B.Tech`, `B.E.`, `B.Sc`, `M.Tech`, `Master's`, `PhD`) against Phase 5 `structuredEducation` requirements.

### G. Quantitative Impact Evidence (10%)
- Detects quantitative figures, metrics (`%`, `500+`, `10x`), and strong action verbs (`launched`, `optimized`, `reduced`, `engineered`).

---

## 4. Test Cases & Score Invariants
- **Controlled Test Cases**: Synthetic test suites A (Strong Match), B (Partial Match), and C (Weak Match) verify logical scoring progression.
- **Score Invariants**: 12 logical invariant tests verify properties such as score monotonicity, canonical alias normalization (`React.js` $\rightarrow$ `React`), false-positive prevention (`Java` vs `JavaScript`, `C` vs `CSS`), and zero divide-by-zero crashes.
