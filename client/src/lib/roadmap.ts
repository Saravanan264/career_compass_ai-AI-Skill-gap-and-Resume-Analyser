import roadmapDb from "@/data/roadmap.json";
import type { ResumeAnalysis, RoadmapStage } from "@/state/resume-store";
import type { JdAnalysis, MatchResult } from "@/state/job-store";
import type { AssessmentAttempt } from "@/state/assessment-store";
import type { RecommendedProject } from "@/lib/project-recommender";

function unique<T>(arr: T[]) {
  return Array.from(new Set(arr));
}

export type SkillProgressItem = {
  skill: string;
  requirement: "required" | "preferred" | "none";
  resumeStatus: "matched" | "missing";
  latestAssessmentScore: number | null;
  previousAssessmentScore: number | null;
  improvement: number | null;
  attemptCount: number;
  status: "Not Assessed" | "Weak" | "Developing" | "Strong";
  trend: "improving" | "declining" | "stable" | "Not Enough Data";
};

export function buildRoadmap({
  analysis,
  domain,
  jdAnalysis,
  matchResult,
  assessmentAttempts = [],
  recommendedProjects = []
}: {
  analysis: ResumeAnalysis;
  domain: string;
  jdAnalysis?: JdAnalysis | null;
  matchResult?: MatchResult | null;
  assessmentAttempts?: AssessmentAttempt[];
  recommendedProjects?: RecommendedProject[];
}): {
  domain: string;
  focusSkills: string[];
  totalDuration: string;
  stages: RoadmapStage[];
  skillProgressList: SkillProgressItem[];
} {
  // Compute skill-wise historical assessment metrics
  const sortedAttempts = [...assessmentAttempts].sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
  );

  const skillHistory: Record<string, number[]> = {};
  sortedAttempts.forEach((attempt) => {
    (attempt.skillScores || []).forEach((ss) => {
      if (!skillHistory[ss.skill]) skillHistory[ss.skill] = [];
      skillHistory[ss.skill].push(ss.score);
    });
  });

  const resumeSkills = analysis.skillsDetected;
  const reqSkills = matchResult?.missingRequiredSkills ?? jdAnalysis?.requiredSkills ?? [];
  const prefSkills = matchResult?.missingPreferredSkills ?? jdAnalysis?.preferredSkills ?? [];
  const allTargetSkills = matchResult?.skillGaps.map((g) => g.skill) ?? jdAnalysis?.allSkills ?? analysis.domains[domain]?.missing ?? [];

  // Build longitudinal progress model for all target skills
  const skillProgressList: SkillProgressItem[] = unique(allTargetSkills).map((skill) => {
    const isReq = reqSkills.includes(skill);
    const isPref = prefSkills.includes(skill);
    const isResumeHave = resumeSkills.includes(skill);

    const scores = skillHistory[skill] ?? [];
    const attemptCount = scores.length;
    const latestAssessmentScore = attemptCount > 0 ? scores[scores.length - 1] : null;
    const previousAssessmentScore = attemptCount >= 2 ? scores[scores.length - 2] : null;
    const improvement = (latestAssessmentScore !== null && previousAssessmentScore !== null)
      ? latestAssessmentScore - previousAssessmentScore
      : null;

    let status: "Not Assessed" | "Weak" | "Developing" | "Strong" = "Not Assessed";
    if (latestAssessmentScore !== null) {
      if (latestAssessmentScore >= 70) status = "Strong";
      else if (latestAssessmentScore >= 50) status = "Developing";
      else status = "Weak";
    }

    let trend: "improving" | "declining" | "stable" | "Not Enough Data" = "Not Enough Data";
    if (improvement !== null) {
      if (improvement > 5) trend = "improving";
      else if (improvement < -5) trend = "declining";
      else trend = "stable";
    }

    return {
      skill,
      requirement: isReq ? "required" : (isPref ? "preferred" : "none"),
      resumeStatus: isResumeHave ? "matched" : "missing",
      latestAssessmentScore,
      previousAssessmentScore,
      improvement,
      attemptCount,
      status,
      trend
    };
  });

  // Classify skills for adaptive stage ordering
  const criticalRequiredGaps = skillProgressList
    .filter((sp) => sp.requirement === "required" && sp.status !== "Strong")
    .map((sp) => sp.skill);

  const moderatePreferredGaps = skillProgressList
    .filter((sp) => sp.requirement === "preferred" && sp.status !== "Strong")
    .map((sp) => sp.skill);

  const strongMasteredSkills = skillProgressList
    .filter((sp) => sp.status === "Strong")
    .map((sp) => sp.skill);

  const focusSkills = unique([...criticalRequiredGaps, ...moderatePreferredGaps]).slice(0, 12);
  if (focusSkills.length === 0) {
    focusSkills.push(...unique(allTargetSkills).slice(0, 8));
  }

  // Load baseline domain database
  const db = roadmapDb as any;
  const domainRoadmap = (db.domains?.[domain] ?? db.domains?.[analysis.bestFitDomain]) as {
    stages: Array<{ title: string; goal: string; duration: string; courses: string[]; projects: string[]; skillTags: string[] }>;
  };

  const stages: RoadmapStage[] = [];

  // Stage 1: Core Foundation & High-Priority Required Gaps
  const stage1Skills = criticalRequiredGaps.length > 0 ? criticalRequiredGaps : focusSkills.slice(0, 3);
  const stage1Explanation = stage1Skills.length > 0
    ? `Prioritized because ${stage1Skills.join(", ")} are required skills for target role and assessment score is below threshold (<70%).`
    : `Focusing on core foundational mastery.`;

  stages.push({
    title: "Stage 1: Core Foundation & High-Priority Required Gaps",
    goal: `Close critical role gaps in ${stage1Skills.slice(0, 3).join(", ")}.`,
    duration: `${Math.max(2, stage1Skills.length * 2)} weeks`,
    courses: stage1Skills.map((s) => `Mastering ${s} - Industry Fundamentals & Hands-on Patterns`),
    projects: [
      `Build a functional project implementing ${stage1Skills[0] ?? "Core Backend"} architecture.`,
      `Implement unit & integration testing for ${stage1Skills.slice(0, 2).join(" & ")}.`
    ],
    status: criticalRequiredGaps.length > 0 ? "In Progress" : "Completed",
    priority: "High",
    explanation: stage1Explanation,
    focusSkills: stage1Skills
  });

  // Stage 2: Applied Projects & Preferred Skill Enhancement
  const stage2Skills = moderatePreferredGaps.length > 0 ? moderatePreferredGaps : focusSkills.slice(3, 6);
  const stage2Projects = recommendedProjects.length > 0
    ? recommendedProjects.slice(0, 2).map((p) => `${p.title} (${p.reason})`)
    : (domainRoadmap?.stages?.[1]?.projects ?? [`Build full-stack feature integrating target skills.`]);

  stages.push({
    title: "Stage 2: Applied Projects & Preferred Skill Enhancement",
    goal: `Develop practical project experience and expand preferred role competencies.`,
    duration: `${Math.max(3, stage2Skills.length * 2)} weeks`,
    courses: stage2Skills.length > 0 ? stage2Skills.map((s) => `Advanced ${s} Optimization & Patterns`) : [`Advanced Full-Stack Engineering`],
    projects: stage2Projects,
    status: "Not Started",
    priority: "Medium",
    explanation: `Enhances resume project strength with recommended practical builds matching target JD gaps.`,
    focusSkills: stage2Skills
  });

  // Stage 3: Reassessment Validation & Career Readiness
  stages.push({
    title: "Stage 3: Reassessment Validation & Career Readiness",
    goal: `Validate skill progress via mock assessments and complete final interview prep.`,
    duration: "2-3 weeks",
    courses: [
      `System Design & Architecture Deep Dive`,
      `Technical Mock Assessment Reassessment Protocol`
    ],
    projects: [
      `CapStone Project Final Review & Performance Benchmarking`,
      `Simulated Interview Evaluation`
    ],
    status: strongMasteredSkills.length >= 3 ? "In Progress" : "Not Started",
    priority: "Low",
    explanation: `Re-evaluates mock assessment performance to verify skill retention and score progression.`,
    focusSkills: strongMasteredSkills.length > 0 ? strongMasteredSkills : focusSkills
  });

  // Dynamic timeline calculation based on remaining unresolved gaps
  const unresolvedGapCount = criticalRequiredGaps.length + moderatePreferredGaps.length;
  const weeks = Math.max(4, Math.min(16, Math.round(unresolvedGapCount * 2.5) + 3));
  const totalDuration = `${weeks}–${weeks + 2} weeks`;

  return {
    domain,
    focusSkills,
    totalDuration,
    stages,
    skillProgressList
  };
}
