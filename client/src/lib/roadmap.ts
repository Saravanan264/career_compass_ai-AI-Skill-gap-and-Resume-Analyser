import roadmapDb from "@/data/roadmap.json";
import type { ResumeAnalysis, RoadmapStage } from "@/state/resume-store";

function unique<T>(arr: T[]) {
  return Array.from(new Set(arr));
}

export function buildRoadmap({
  analysis,
  domain,
}: {
  analysis: ResumeAnalysis;
  domain: string;
}): { domain: string; focusSkills: string[]; totalDuration: string; stages: RoadmapStage[] } {
  const domainFit = analysis.domains[domain] ?? analysis.domains[analysis.bestFitDomain];
  const missing = domainFit?.missing ?? [];

  const db = roadmapDb as any;
  const domainRoadmap = (db.domains?.[domain] ?? db.domains?.[analysis.bestFitDomain]) as {
    stages: Array<{ title: string; goal: string; duration: string; courses: string[]; projects: string[]; skillTags: string[] }>;
  };

  const focusSkills = unique(missing).slice(0, 12);

  const stages: RoadmapStage[] = (domainRoadmap?.stages ?? []).map((s) => ({
    title: s.title,
    goal: s.goal,
    duration: s.duration,
    courses: s.courses,
    projects: s.projects,
  }));

  // Simple timeline estimate based on missing skills
  const weeks = Math.max(6, Math.min(18, Math.round(focusSkills.length * 1.2)));
  const totalDuration = `${weeks}–${weeks + 2} weeks`;

  return { domain, focusSkills, totalDuration, stages };
}
