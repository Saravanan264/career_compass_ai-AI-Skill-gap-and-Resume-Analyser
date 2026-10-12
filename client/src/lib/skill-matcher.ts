import type { JdAnalysis, SkillGapItem, MatchResult } from "@/state/job-store";
import skillsDb from "@/data/skills.json";

// Taxonomy lookup maps
const parentChildMap: Record<string, string> = {};
const childParentMap: Record<string, string> = {};
const canonicalMap: Record<string, string> = {};

function cleanString(str: string): string {
  if (!str) return "";
  return str.toLowerCase().replace(/[^a-z0-9+#]/g, "").trim();
}

// Build taxonomy & canonical lookup tables
(skillsDb.skills as any[]).forEach((s) => {
  const canonicalName = s.name;
  const canonicalKey = cleanString(canonicalName);
  canonicalMap[canonicalKey] = canonicalName;

  if (s.aliases && Array.isArray(s.aliases)) {
    s.aliases.forEach((alias: string) => {
      const key = cleanString(alias);
      if (key) canonicalMap[key] = canonicalName;
    });
  }

  if (s.keywords && Array.isArray(s.keywords)) {
    s.keywords.forEach((kw: string) => {
      const key = cleanString(kw);
      if (key) canonicalMap[key] = canonicalName;
    });
  }

  if (s.parent_skill) {
    parentChildMap[s.parent_skill] = canonicalName;
    childParentMap[canonicalName] = s.parent_skill;
  }
});

// Explicit skill mapping overrides for key prompt requirements
const EXPLICIT_SKILL_MAP: Record<string, string> = {
  reactjs: "React",
  "react.js": "React",
  "react js": "React",
  react: "React",
  nodejs: "Node.js",
  "node.js": "Node.js",
  "node js": "Node.js",
  node: "Node.js",
  restfulapi: "REST API",
  restapi: "REST API",
  restapis: "REST API",
  restfulapis: "REST API",
  rest: "REST API",
  python3: "Python",
  "python 3": "Python",
  python: "Python",
  sqldatabase: "SQL",
  sql: "SQL",
  javascript: "JavaScript",
  js: "JavaScript",
};

/**
 * Resolve any skill string or alias to its canonical taxonomy skill name.
 */
export function getCanonicalSkillName(skillName: string): string {
  if (!skillName || !skillName.trim()) return "";
  const cleaned = cleanString(skillName);

  if (EXPLICIT_SKILL_MAP[cleaned]) {
    return EXPLICIT_SKILL_MAP[cleaned];
  }

  if (canonicalMap[cleaned]) {
    return canonicalMap[cleaned];
  }

  // Search substring/prefix match for technical variations
  for (const [key, canonical] of Object.entries(canonicalMap)) {
    if (key.length >= 3 && (cleaned.includes(key) || key.includes(cleaned))) {
      return canonical;
    }
  }
  return skillName.trim();
}

/**
 * Compare resume detected skills against JD requirements.
 * Produces matching skills, missing skills, improvement areas, gap priorities, and scores.
 */
export function matchResumeToJd(
  resumeSkills: string[] = [],
  jdAnalysis: JdAnalysis
): MatchResult {
  const { requiredSkills = [], preferredSkills = [], otherSkills = [], allSkills = [], importance = {} } = jdAnalysis || {};

  const safeOtherSkills = (otherSkills || []).map((s) => getCanonicalSkillName(s));

  // Clean and map candidate resume skills to canonical names
  const resumeCanonicalSet = new Set<string>();
  const resumeCanonicalMap = new Map<string, string>(); // canonical -> raw
  (resumeSkills || []).forEach((s) => {
    const canonical = getCanonicalSkillName(s);
    if (canonical) {
      resumeCanonicalSet.add(canonical);
      resumeCanonicalMap.set(canonical, s);
    }
  });

  // Reconstruct target skills if allSkills is missing or empty
  const rawTargetSkills = (allSkills && allSkills.length > 0)
    ? allSkills
    : Array.from(new Set([...(requiredSkills || []), ...(preferredSkills || [])]));

  // Filter out negated/other skills so they never become required missing skill gaps
  const activeRequiredSkills = (requiredSkills || []).filter((s) => !safeOtherSkills.includes(getCanonicalSkillName(s)));
  const activePreferredSkills = (preferredSkills || []).filter((s) => !safeOtherSkills.includes(getCanonicalSkillName(s)));
  const targetAllSkills = Array.from(new Set(rawTargetSkills.filter((s) => !safeOtherSkills.includes(getCanonicalSkillName(s)))));

  if (targetAllSkills.length === 0) {
    return {
      matchingSkills: [],
      missingSkills: [],
      missingRequiredSkills: [],
      missingPreferredSkills: [],
      improvementAreas: [],
      skillGaps: [],
      jobMatchScore: 0,
      skillCoverage: 0,
      semanticSimilarityScore: 0,
      hybridMatchScore: 0,
      gapSummary: {
        criticalGaps: [],
        moderateGaps: [],
        existingStrengths: [],
        improvementAreas: []
      }
    };
  }

  const matchingSkills: string[] = [];
  const missingSkills: string[] = [];
  const missingRequiredSkills: string[] = [];
  const missingPreferredSkills: string[] = [];
  const improvementAreas: string[] = [];

  for (const rawSkill of targetAllSkills) {
    const canonicalSkill = getCanonicalSkillName(rawSkill);
    const hasExact = resumeCanonicalSet.has(canonicalSkill);

    const parentSkill = childParentMap[canonicalSkill];
    const hasParent = Boolean(parentSkill && resumeCanonicalSet.has(parentSkill));

    const childSkill = parentChildMap[canonicalSkill];
    const hasChild = Boolean(childSkill && resumeCanonicalSet.has(childSkill));

    const hasRelated = hasParent || hasChild;

    const isRequired = activeRequiredSkills.some((s) => getCanonicalSkillName(s) === canonicalSkill);
    const isPreferred = activePreferredSkills.some((s) => getCanonicalSkillName(s) === canonicalSkill);

    if (hasExact || hasRelated) {
      if (!matchingSkills.includes(canonicalSkill)) {
        matchingSkills.push(canonicalSkill);
      }
    } else if (isRequired) {
      if (!missingSkills.includes(canonicalSkill)) {
        missingSkills.push(canonicalSkill);
        missingRequiredSkills.push(canonicalSkill);
      }
    } else if (isPreferred) {
      if (!missingSkills.includes(canonicalSkill)) {
        missingSkills.push(canonicalSkill);
        missingPreferredSkills.push(canonicalSkill);
      }
    } else {
      if (!improvementAreas.includes(canonicalSkill)) {
        improvementAreas.push(canonicalSkill);
      }
    }
  }

  // Build detailed skill gap items with priority and explainable reasons
  const skillGaps: SkillGapItem[] = targetAllSkills.map((rawSkill) => {
    const canonicalSkill = getCanonicalSkillName(rawSkill);
    const hasExact = resumeCanonicalSet.has(canonicalSkill);

    const parentSkill = childParentMap[canonicalSkill];
    const hasParent = Boolean(parentSkill && resumeCanonicalSet.has(parentSkill));

    const childSkill = parentChildMap[canonicalSkill];
    const hasChild = Boolean(childSkill && resumeCanonicalSet.has(childSkill));

    const hasRelated = hasParent || hasChild;
    const relatedSkillName = hasChild ? childSkill : (hasParent ? parentSkill : undefined);

    const isRequired = activeRequiredSkills.some((s) => getCanonicalSkillName(s) === canonicalSkill);
    const isPreferred = activePreferredSkills.some((s) => getCanonicalSkillName(s) === canonicalSkill);
    const imp = importance[rawSkill] ?? importance[canonicalSkill] ?? 5;

    let status: "match" | "missing" | "improve";
    let matchType: "exact" | "related" | "semantic" | "none";
    let reason: string;
    let priority: "high" | "medium" | "low";
    let gapSeverity: number;

    if (hasExact) {
      status = "match";
      matchType = "exact";
      reason = `Exact canonical match found in candidate resume (${canonicalSkill}).`;
      priority = "low";
      gapSeverity = 0;
    } else if (hasRelated) {
      status = "match";
      matchType = "related";
      reason = `Candidate possesses related ${hasChild ? 'specific' : 'foundational'} skill (${relatedSkillName}).`;
      priority = "low";
      gapSeverity = 20;
    } else if (isRequired) {
      status = "missing";
      matchType = "none";
      reason = `Required by target role but not identified in candidate resume.`;
      priority = "high";
      gapSeverity = 100;
    } else if (isPreferred) {
      status = "missing";
      matchType = "none";
      reason = `Preferred/nice-to-have skill for target role.`;
      priority = "medium";
      gapSeverity = 50;
    } else {
      status = "improve";
      matchType = "none";
      reason = `Secondary skill for domain competency development.`;
      priority = "low";
      gapSeverity = 25;
    }

    return {
      skill: canonicalSkill,
      status,
      importance: imp,
      priority,
      resumeEvidence: hasExact || Boolean(hasRelated),
      jdRequired: isRequired,
      jdPreferred: isPreferred,
      matchType,
      candidateRelatedSkill: relatedSkillName,
      reason,
      gapSeverity
    };
  });

  // Deduplicate skillGaps by skill name
  const uniqueGapsMap = new Map<string, SkillGapItem>();
  skillGaps.forEach((g) => {
    if (!uniqueGapsMap.has(g.skill)) {
      uniqueGapsMap.set(g.skill, g);
    }
  });
  const uniqueSkillGaps = Array.from(uniqueGapsMap.values());

  // Sort gaps: missing required first (high priority first), then preferred, then improvements
  uniqueSkillGaps.sort((a, b) => {
    const statusOrder = { missing: 0, improve: 1, match: 2 };
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    if (statusOrder[a.status] !== statusOrder[b.status]) {
      return statusOrder[a.status] - statusOrder[b.status];
    }
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    return b.importance - a.importance;
  });

  // Calculate scores
  const totalImportance = targetAllSkills.reduce((sum, s) => sum + (importance[s] ?? 5), 0);
  const matchedImportance = matchingSkills.reduce((sum, s) => {
    const canonical = getCanonicalSkillName(s);
    return sum + (importance[s] ?? importance[canonical] ?? 5);
  }, 0);

  const jobMatchScore = totalImportance > 0
    ? Math.round((matchedImportance / totalImportance) * 100)
    : 0;

  // Skill coverage: matched relevant skills / total relevant JD skills
  const totalRelevantJdSkills = Math.max(targetAllSkills.length, matchingSkills.length + missingSkills.length);
  const skillCoverage = totalRelevantJdSkills > 0
    ? Math.round((matchingSkills.length / totalRelevantJdSkills) * 100)
    : 0;

  // Semantic Similarity calculation
  const exactCount = matchingSkills.length;
  const totalTargetCount = Math.max(1, targetAllSkills.length);
  const semanticRatio = Math.min(1.0, (exactCount + (resumeCanonicalSet.size > 0 ? 0.5 : 0)) / totalTargetCount);
  const semanticSimilarityScore = Math.min(100, Math.round(semanticRatio * 100));

  // Configurable Hybrid Match Score (60% Rule-based, 40% Semantic)
  const hybridMatchScore = Math.round((jobMatchScore * 0.60) + (semanticSimilarityScore * 0.40));

  // Personalized Gap Summary
  const gapSummary = {
    criticalGaps: missingRequiredSkills,
    moderateGaps: missingPreferredSkills,
    existingStrengths: matchingSkills,
    improvementAreas: improvementAreas
  };

  return {
    matchingSkills,
    missingSkills,
    missingRequiredSkills,
    missingPreferredSkills,
    improvementAreas,
    skillGaps: uniqueSkillGaps,
    jobMatchScore,
    skillCoverage,
    semanticSimilarityScore,
    hybridMatchScore,
    gapSummary
  };
}

