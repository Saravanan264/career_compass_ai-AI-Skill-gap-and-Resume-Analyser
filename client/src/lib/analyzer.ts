import skillsDb from "@/data/skills.json";
import domainsDb from "@/data/domains.json";

import type { ResumeAnalysis } from "@/state/resume-store";

function normalize(text: string) {
  return text
    .toLowerCase()
    .replaceAll(/[^a-z0-9+.#\s-]/g, " ")
    .replaceAll(/\s+/g, " ")
    .trim();
}

function unique<T>(arr: T[]) {
  return Array.from(new Set(arr));
}

function countMatches(text: string, keywords: string[]) {
  let hits = 0;
  for (const k of keywords) {
    const kk = normalize(k);
    if (!kk) continue;
    if (text.includes(kk)) hits++;
  }
  return hits;
}

function scorePresence(text: string, patterns: string[], max = 100) {
  const n = countMatches(text, patterns);
  const denom = Math.max(1, patterns.length);
  return Math.round((n / denom) * max);
}

function computeAts(textRaw: string, detectedSkills: string[]) {
  const text = normalize(textRaw);
  const charLen = textRaw.trim().length;

  if (charLen === 0) {
    return {
      overallScore: 0,
      keywordCoverage: 0,
      sectionScores: { format: 0, experience: 0, skills: 0, education: 0, impact: 0 },
      missingTopKeywords: [],
    };
  }

  // 1. Format & Scannability (up to 100)
  const hasEmail = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/.test(textRaw);
  const hasPhone = /(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b/.test(textRaw) || text.includes("phone");
  const hasProfile = ["linkedin", "github", "portfolio", "address", "location"].some((k) => text.includes(k));
  
  let contactScore = 0;
  if (hasEmail) contactScore += 10;
  if (hasPhone) contactScore += 8;
  if (hasProfile) contactScore += 7;

  const sectionsFound = {
    summary: ["summary", "objective", "profile", "about"].some((k) => text.includes(k)),
    experience: ["experience", "employment", "work history", "internship"].some((k) => text.includes(k)),
    education: ["education", "academic", "university", "degree"].some((k) => text.includes(k)),
    skills: ["skills", "technologies", "proficiencies", "competencies"].some((k) => text.includes(k)),
    projects: ["projects", "personal projects", "academic projects"].some((k) => text.includes(k)),
  };
  const coreSectionCount = Object.values(sectionsFound).filter(Boolean).length;
  let sectionScore = 0;
  if (coreSectionCount >= 4) sectionScore = 30;
  else if (coreSectionCount === 3) sectionScore = 22;
  else if (coreSectionCount === 2) sectionScore = 15;
  else if (coreSectionCount === 1) sectionScore = 8;

  let lengthScore = 5;
  if (charLen >= 1200 && charLen <= 6000) lengthScore = 25;
  else if ((charLen >= 600 && charLen < 1200) || (charLen > 6000 && charLen <= 9000)) lengthScore = 18;
  else if (charLen >= 250 && charLen < 600) lengthScore = 10;

  const bulletMatches = (textRaw.match(/(?:^|\n)\s*[\u2022\u2023\u25b6\u25c0\u2013\u2014\-\*]\s+|(?:\d+\.\s+)/g) || []).length;
  let formatOrgScore = 5;
  if (bulletMatches >= 5) formatOrgScore = 20;
  else if (bulletMatches >= 2) formatOrgScore = 12;
  else if (textRaw.includes("\n") && charLen >= 300) formatOrgScore = 8;

  const format = Math.min(100, contactScore + sectionScore + lengthScore + formatOrgScore);

  // 2. Education Alignment
  const hasHigherDegree = ["master", "phd", "doctorate", "m.tech", "m.sc", "m.s.", "ms degree"].some((d) => text.includes(d));
  const hasBachelor = ["bachelor", "b.tech", "b.e", "b.sc", "b.s", "bs degree", "b.a"].some((d) => text.includes(d));
  const hasAssociate = ["associate", "diploma", "coursework"].some((d) => text.includes(d));
  const hasUniversity = ["university", "college", "institute", "school", "academy"].some((u) => text.includes(u));
  const hasField = ["computer science", "data science", "engineering", "information technology", "mathematics", "software", "information systems"].some((f) => text.includes(f));
  const hasHonors = ["gpa", "cgpa", "honors", "cum laude", "first class"].some((h) => text.includes(h));

  let degreeScore = 15;
  if (hasHigherDegree) degreeScore = 45;
  else if (hasBachelor) degreeScore = 40;
  else if (hasAssociate) degreeScore = 25;

  const instScore = hasUniversity ? 25 : 10;
  const fieldScore = hasField ? 20 : 5;
  const honorsScore = hasHonors ? 10 : 0;
  const education = Math.min(100, Math.max(20, degreeScore + instScore + fieldScore + honorsScore));

  // 3. Experience Alignment
  const hasRoleTitle = ["engineer", "developer", "architect", "lead", "manager", "analyst", "consultant", "specialist", "intern"].some((r) => text.includes(r));
  const hasWorkSection = ["experience", "employment", "work history", "career history"].some((s) => text.includes(s));
  const expMatch = textRaw.match(/\b(\d+)\s*\+?\s*(?:years?|yrs?)\b/i);
  const candYears = expMatch ? parseInt(expMatch[1], 10) : null;
  const hasCompany = ["company", "inc", "ltd", "corp", "solutions", "tech", "systems", "team", "startup"].some((c) => text.includes(c));

  let baseExp = 0;
  if (hasRoleTitle) baseExp += 25;
  if (hasWorkSection) baseExp += 25;
  if (candYears !== null) {
    if (candYears >= 5) baseExp += 30;
    else if (candYears >= 3) baseExp += 25;
    else if (candYears >= 1) baseExp += 20;
    else baseExp += 12;
  } else {
    baseExp += 10;
  }
  if (hasCompany) baseExp += 20;
  const experience = Math.min(100, Math.max(15, baseExp));

  // 4. Impact Evidence
  const metricsMatches = textRaw.match(/\b\d+[\%\+]?\b|\b\d+\s*(?:percent|users|customers|k|m|ms|sec|hours|sprint)\b/gi) || [];
  let metricScore = 5;
  if (metricsMatches.length >= 3) metricScore = 40;
  else if (metricsMatches.length >= 1) metricScore = 25;

  const actionVerbs = ["increased", "reduced", "improved", "optimized", "launched", "delivered", "saved", "grew", "achieved", "developed", "built", "engineered", "architected", "automated", "created", "designed", "spearheaded", "transformed", "implemented"];
  const matchedVerbs = unique(actionVerbs.filter((v) => text.includes(v)));
  let verbScore = 0;
  if (matchedVerbs.length >= 6) verbScore = 40;
  else if (matchedVerbs.length >= 3) verbScore = 25;
  else if (matchedVerbs.length >= 1) verbScore = 15;

  const scaleWords = ["production", "scaled", "automated", "benchmark", "uptime", "latency", "revenue", "efficiency", "throughput"];
  const matchedScale = scaleWords.filter((w) => text.includes(w));
  let scaleScore = 0;
  if (matchedScale.length >= 2) scaleScore = 20;
  else if (matchedScale.length === 1) scaleScore = 10;

  const impact = Math.min(100, Math.max(5, metricScore + verbScore + scaleScore));

  // 5. Skills Coverage & Keyword Coverage
  const { domains, bestFitDomain } = computeDomainFits(detectedSkills);
  const bestDomainFit = domains[bestFitDomain] ?? { fitScore: 0, have: [], missing: [] };
  const domainHaveCount = bestDomainFit.have.length;
  const domainMissingCount = bestDomainFit.missing.length;
  const domainReqCount = Math.max(10, domainHaveCount + domainMissingCount);

  const allSkills = (skillsDb as any).skills as { name: string; keywords: string[] }[];
  const topKeywords = allSkills.slice(0, 26).map((s) => s.name);
  const missingTop = topKeywords.filter((k) => !detectedSkills.includes(k));

  const keywordCoverage = Math.min(100, Math.round((domainHaveCount / domainReqCount) * 100));
  const domainRatio = domainHaveCount / Math.max(1, domainHaveCount + domainMissingCount);
  const overallSkillsRatio = detectedSkills.length / 25.0;
  const skills = Math.min(100, Math.max(15, Math.round((domainRatio * 0.65 + overallSkillsRatio * 0.35) * 100)));

  // Weighted Overall ATS Score
  const overall =
    format * 0.15 +
    experience * 0.20 +
    skills * 0.25 +
    education * 0.15 +
    impact * 0.10;

  return {
    overallScore: Math.max(10, Math.min(100, Math.round(overall))),
    keywordCoverage,
    sectionScores: { format, experience, skills, education, impact },
    missingTopKeywords: missingTop,
  };
}

function computeDomainFits(detectedSkills: string[]) {
  const domains = (domainsDb as any).domains as {
    name: string;
    requiredSkills: string[];
  }[];

  const byDomain: Record<string, { fitScore: number; have: string[]; missing: string[] }> = {};

  for (const d of domains) {
    const required = unique(d.requiredSkills);
    const have = required.filter((s) => detectedSkills.includes(s));
    const missing = required.filter((s) => !detectedSkills.includes(s));
    const fitScore = Math.round((have.length / Math.max(1, required.length)) * 100);
    byDomain[d.name] = { fitScore, have, missing };
  }

  const best = domains
    .map((d) => ({ name: d.name, fit: byDomain[d.name].fitScore }))
    .sort((a, b) => b.fit - a.fit)[0]?.name;

  return { domains: byDomain, bestFitDomain: best ?? domains[0]?.name ?? "Data Science" };
}

function computeConfidence(atsScore: number, bestFitScore: number, detectedSkillsCount: number) {
  const signal = Math.min(100, Math.round((detectedSkillsCount / 30) * 100));
  const blended = Math.round(atsScore * 0.55 + bestFitScore * 0.30 + signal * 0.15);
  return Math.max(25, Math.min(98, blended));
}

function computeFinalScorecard(analysis: {
  atsScore: number;
  coverage: number;
  impact: number;
  format: number;
  bestFit: number;
}) {
  const resumeScore = Math.round(
    analysis.atsScore * 0.55 +
      analysis.coverage * 0.15 +
      analysis.impact * 0.10 +
      analysis.format * 0.10 +
      analysis.bestFit * 0.10,
  );

  return {
    resumeScore,
    metrics: [
      {
        key: "ats",
        label: "ATS Score",
        score: analysis.atsScore,
        note: "Weighted overall ATS-style score.",
      },
      {
        key: "coverage",
        label: "Keyword Coverage",
        score: analysis.coverage,
        note: "How much of the skills database you hit.",
      },
      {
        key: "impact",
        label: "Impact Signals",
        score: analysis.impact,
        note: "Quantified outcomes and strong action verbs.",
      },
      {
        key: "format",
        label: "Format & Structure",
        score: analysis.format,
        note: "Clear sections, contact details, and scannability.",
      },
      {
        key: "domain",
        label: "Domain Fit",
        score: analysis.bestFit,
        note: "Match against the target skill map.",
      },
    ],
  };
}

export function validateResumeStructure(textRaw: string): { isValidResume: boolean; validationReason: string } {
  if (!textRaw || !textRaw.trim()) {
    return {
      isValidResume: false,
      validationReason: "This document does not appear to be a valid resume. Please upload a resume containing candidate details, skills, education, experience, projects, or other resume sections."
    };
  }

  const textNorm = normalize(textRaw);
  const charLen = textRaw.trim().length;
  const words = textRaw.match(/\b[a-zA-Z]{2,}\b/g) || [];
  const wordCount = words.length;

  const hasMinimumLength = charLen >= 150 && wordCount >= 25;

  const hasEmail = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/.test(textRaw);
  const hasPhone = /(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b/.test(textRaw);
  const hasProfileLinks = ["linkedin", "github", "portfolio", "address", "location"].some((k) => textNorm.includes(k));
  const hasContactInfo = hasEmail || hasPhone || hasProfileLinks;

  const sectionPatterns = [
    /\b(?:work\s+)?experience\b/, /\bemployment\b/, /\bwork\s+history\b/, /\bcareer\s+history\b/,
    /\beducation\b/, /\bacademic\b/, /\bdegree\b/,
    /\bskills\b/, /\btechnologies\b/, /\bcompetencies\b/, /\bproficiencies\b/,
    /\bprojects\b/, /\bpersonal\s+projects\b/,
    /\bsummary\b/, /\bobjective\b/, /\bprofile\b/,
    /\bcertifications?\b/, /\bachievements?\b/
  ];
  const sectionsMatched = sectionPatterns.filter((p) => p.test(textNorm)).length;
  const hasResumeSections = sectionsMatched >= 2;

  const roleTerms = ["developer", "engineer", "analyst", "architect", "manager", "specialist", "intern", "consultant", "lead", "designer", "administrator"];
  const eduTerms = ["bachelor", "master", "degree", "university", "college", "institute", "b.tech", "b.e", "b.sc", "m.tech", "m.sc", "phd", "gpa"];
  const contentSignalCount = [...roleTerms, ...eduTerms].filter((t) => textNorm.includes(t)).length;
  const hasContentSignals = contentSignalCount >= 2;

  const isValid = hasMinimumLength && (
    (hasContactInfo && hasResumeSections) ||
    (hasResumeSections && hasContentSignals) ||
    (hasContactInfo && hasContentSignals && sectionsMatched >= 1)
  );

  return {
    isValidResume: isValid,
    validationReason: isValid ? "Valid resume document detected." : "This document does not appear to be a valid resume. Please upload a resume containing candidate details, skills, education, experience, projects, or other resume sections."
  };
}

export async function analyzeResumeText(textRaw: string): Promise<ResumeAnalysis> {
  const validation = validateResumeStructure(textRaw);
  if (!validation.isValidResume) {
    return {
      isValidResume: false,
      validationReason: validation.validationReason,
      ats: {
        overallScore: 0,
        keywordCoverage: 0,
        sectionScores: { format: 0, experience: 0, skills: 0, education: 0, impact: 0 },
        missingTopKeywords: [],
      },
      skillsDetected: [],
      domains: {},
      bestFitDomain: "None",
      confidence: 0,
      finalScorecard: {
        resumeScore: 0,
        metrics: [],
      },
    };
  }

  const text = normalize(textRaw);

  const allSkills = (skillsDb as any).skills as { name: string; keywords: string[] }[];

  const detected: string[] = [];
  for (const s of allSkills) {
    const keywords = unique([s.name, ...(s.keywords ?? [])]);
    const hit = keywords.some((k) => text.includes(normalize(k)));
    if (hit) detected.push(s.name);
  }

  const skillsDetected = unique(detected).sort((a, b) => a.localeCompare(b));

  const ats = computeAts(textRaw, skillsDetected);
  const { domains, bestFitDomain } = computeDomainFits(skillsDetected);
  const bestFitScore = domains[bestFitDomain]?.fitScore ?? 0;

  const confidence = computeConfidence(ats.overallScore, bestFitScore, skillsDetected.length);

  const finalScorecard = computeFinalScorecard({
    atsScore: ats.overallScore,
    coverage: ats.keywordCoverage,
    impact: ats.sectionScores.impact,
    format: ats.sectionScores.format,
    bestFit: bestFitScore,
  });

  return {
    isValidResume: true,
    validationReason: validation.validationReason,
    ats,
    skillsDetected,
    domains,
    bestFitDomain,
    confidence,
    finalScorecard,
  };
}

