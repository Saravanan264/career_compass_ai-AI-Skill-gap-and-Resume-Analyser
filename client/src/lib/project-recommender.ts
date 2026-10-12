import projectsDb from "@/data/projects.json";
import { getCanonicalSkillName } from "./skill-matcher";

export type RecommendedProject = {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  estimatedHours: number;
  skillsCovered: string[];
  gapSkillsCovered: string[];
  coveredMissingSkills: string[];
  uncoveredMissingSkills: string[];
  requiredSkillCoverage: number;
  preferredSkillCoverage: number;
  coverageScore: number;
  priority: "High" | "Medium" | "Low";
  tags: string[];
  reason: string;
};

/**
 * Recommend projects based on missing/weak skills.
 * Projects that cover more missing skills rank higher.
 */
export function recommendProjects(
  missingRequiredSkills: string[] = [],
  missingPreferredSkills: string[] = [],
  improvementSkills: string[] = [],
  maxProjects = 5
): RecommendedProject[] {
  const reqCanonical = missingRequiredSkills.map(getCanonicalSkillName).filter(Boolean);
  const prefCanonical = missingPreferredSkills.map(getCanonicalSkillName).filter(Boolean);
  const impCanonical = improvementSkills.map(getCanonicalSkillName).filter(Boolean);
  
  const allMissingCanonical = Array.from(new Set([...reqCanonical, ...prefCanonical]));
  const allGapCanonical = Array.from(new Set([...allMissingCanonical, ...impCanonical]));

  if (allGapCanonical.length === 0) return [];

  const projects = (projectsDb as any).projects as Array<{
    id: string;
    title: string;
    description: string;
    difficulty: string;
    estimatedHours: number;
    skillsCovered: string[];
    tags: string[];
  }>;

  let scored: RecommendedProject[] = projects
    .map((p) => {
      const pSkillsCanonical = p.skillsCovered.map(getCanonicalSkillName);

      const coveredReq = pSkillsCanonical.filter((s) => reqCanonical.includes(s));
      const coveredPref = pSkillsCanonical.filter((s) => prefCanonical.includes(s));
      const gapSkillsCovered = pSkillsCanonical.filter((s) => allGapCanonical.includes(s));
      const uncoveredReq = reqCanonical.filter((s) => !pSkillsCanonical.includes(s));

      const displayGapSkillsCovered = p.skillsCovered.filter((raw) =>
        allGapCanonical.includes(getCanonicalSkillName(raw))
      );
      const displayCoveredReq = p.skillsCovered.filter((raw) =>
        reqCanonical.includes(getCanonicalSkillName(raw))
      );
      const displayCoveredPref = p.skillsCovered.filter((raw) =>
        prefCanonical.includes(getCanonicalSkillName(raw))
      );

      const reqCoveragePct = reqCanonical.length > 0
        ? Math.round((coveredReq.length / reqCanonical.length) * 100)
        : 100;

      const prefCoveragePct = prefCanonical.length > 0
        ? Math.round((coveredPref.length / prefCanonical.length) * 100)
        : 100;

      // Deterministic Ranking Score based on gap coverage
      let score = coveredReq.length * 35 + coveredPref.length * 20 + gapSkillsCovered.length * 10;
      if (gapSkillsCovered.length >= 2) {
        score += 20; // Multi-skill bonus
      }

      const totalMissing = Math.max(1, allMissingCanonical.length);
      const coveredCount = Array.from(new Set([...coveredReq, ...coveredPref])).length;
      const coveragePct = allMissingCanonical.length > 0
        ? Math.round((coveredCount / totalMissing) * 100)
        : Math.min(100, score);

      const coverageScore = coveragePct > 0 ? coveragePct : Math.min(100, score);
      const priority: "High" | "Medium" | "Low" = coveredReq.length > 0 ? "High" : (coveredPref.length > 0 ? "Medium" : "Low");

      let reason = "";
      if (displayCoveredReq.length > 0) {
        reason = `Recommended because it directly addresses ${displayCoveredReq.length} missing required skill gap${displayCoveredReq.length > 1 ? 's' : ''}: ${displayCoveredReq.join(", ")}.`;
      } else if (displayCoveredPref.length > 0) {
        reason = `Recommended because it covers ${displayCoveredPref.length} preferred target skill${displayCoveredPref.join(", ")}.`;
      } else {
        reason = `Covers key candidate development skills: ${displayGapSkillsCovered.join(", ")}.`;
      }

      return {
        id: p.id,
        title: p.title,
        description: p.description,
        difficulty: p.difficulty,
        estimatedHours: p.estimatedHours,
        skillsCovered: p.skillsCovered,
        gapSkillsCovered: displayGapSkillsCovered,
        coveredMissingSkills: [...displayCoveredReq, ...displayCoveredPref],
        uncoveredMissingSkills: uncoveredReq,
        requiredSkillCoverage: reqCoveragePct,
        preferredSkillCoverage: prefCoveragePct,
        coverageScore,
        priority,
        tags: p.tags,
        reason,
      };
    })
    .filter((p) => p.gapSkillsCovered.length > 0)
    .sort((a, b) => b.coverageScore - a.coverageScore)
    .slice(0, maxProjects);

  // Fallback: If candidate has missing skills but no project matched exact tags, return top general backend/fullstack/data projects
  if (scored.length === 0 && allMissingCanonical.length > 0) {
    scored = projects.slice(0, maxProjects).map((p) => ({
      id: p.id,
      title: p.title,
      description: p.description,
      difficulty: p.difficulty,
      estimatedHours: p.estimatedHours,
      skillsCovered: p.skillsCovered,
      gapSkillsCovered: p.skillsCovered.slice(0, 3),
      coveredMissingSkills: [],
      uncoveredMissingSkills: reqCanonical,
      requiredSkillCoverage: 50,
      preferredSkillCoverage: 50,
      coverageScore: 60,
      priority: "Medium",
      tags: p.tags,
      reason: `Recommended hands-on project to strengthen candidate technical portfolio.`
    }));
  }

  return scored;
}
