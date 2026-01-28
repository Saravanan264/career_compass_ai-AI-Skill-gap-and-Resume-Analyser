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

  // Section heuristics (transparent, demo-friendly)
  const formatSignals = [
    "email",
    "phone",
    "linkedin",
    "github",
    "experience",
    "education",
    "skills",
    "projects",
  ];

  const impactSignals = [
    "%",
    "increased",
    "reduced",
    "improved",
    "optimized",
    "launched",
    "delivered",
    "saved",
    "grew",
    "achieved",
  ];

  const educationSignals = ["bachelor", "master", "b.sc", "m.sc", "phd", "university", "college"];
  const experienceSignals = ["intern", "engineer", "developer", "analyst", "lead", "manager", "company", "team"];

  const format = scorePresence(text, formatSignals);
  const impact = scorePresence(text, impactSignals);
  const education = scorePresence(text, educationSignals);
  const experience = scorePresence(text, experienceSignals);

  // Skills section is measured by detected skills coverage vs database
  const allSkills = (skillsDb as any).skills as { name: string; keywords: string[] }[];
  const topKeywords = allSkills.slice(0, 26).map((s) => s.name);
  const missingTop = topKeywords.filter((k) => !detectedSkills.includes(k));

  const coverage = Math.round((detectedSkills.length / Math.max(1, allSkills.length)) * 100);
  const skills = Math.max(20, Math.min(100, Math.round(coverage * 1.25)));

  // Weightages
  const weights = {
    format: 0.20,
    experience: 0.25,
    skills: 0.30,
    education: 0.10,
    impact: 0.15,
  } as const;

  const overall =
    format * weights.format +
    experience * weights.experience +
    skills * weights.skills +
    education * weights.education +
    impact * weights.impact;

  return {
    overallScore: Math.round(overall),
    keywordCoverage: Math.max(0, Math.min(100, coverage)),
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

export async function analyzeResumeText(textRaw: string): Promise<ResumeAnalysis> {
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
    ats,
    skillsDetected,
    domains,
    bestFitDomain,
    confidence,
    finalScorecard,
  };
}
