import companiesDb from "@/data/companies.json";
import type { SkillScore } from "@/state/assessment-store";

export type ReadinessBreakdown = {
  profileMatch: number;
  skillCoverage: number;
  assessmentPerformance: number;
};

export type CompanyReadiness = {
  companyId: string;
  companyName: string;
  roleTitle: string;
  readinessScore: number;
  breakdown: ReadinessBreakdown;
  matchedSkills: string[];
  missingSkills: string[];
  totalRequired: number;
};

const WEIGHTS = {
  profileMatch: 0.30,
  skillCoverage: 0.30,
  assessmentPerformance: 0.40,
};

/**
 * Calculate career readiness for each company/role profile.
 * 
 * Readiness = 0.30 × Profile Match + 0.30 × Skill Coverage + 0.40 × Assessment Performance
 */
export function calculateReadiness(
  resumeSkills: string[],
  assessmentSkillScores?: SkillScore[]
): CompanyReadiness[] {
  const companies = (companiesDb as any).companies as Array<{
    id: string;
    name: string;
    roles: Array<{
      title: string;
      requiredSkills: string[];
      preferredSkills: string[];
      importance: Record<string, number>;
    }>;
  }>;

  const results: CompanyReadiness[] = [];

  for (const company of companies) {
    for (const role of company.roles) {
      const allSkills = [...role.requiredSkills, ...role.preferredSkills];
      const matchedSkills = allSkills.filter((s) => resumeSkills.includes(s));
      const missingSkills = allSkills.filter((s) => !resumeSkills.includes(s));

      // Profile Match: weighted match against all required + preferred
      const totalImportance = allSkills.reduce(
        (sum, s) => sum + (role.importance[s] ?? 5),
        0
      );
      const matchedImportance = matchedSkills.reduce(
        (sum, s) => sum + (role.importance[s] ?? 5),
        0
      );
      const profileMatch = totalImportance > 0
        ? Math.round((matchedImportance / totalImportance) * 100)
        : 0;

      // Skill Coverage: required skills only
      const requiredMatched = role.requiredSkills.filter((s) =>
        resumeSkills.includes(s)
      ).length;
      const skillCoverage =
        role.requiredSkills.length > 0
          ? Math.round((requiredMatched / role.requiredSkills.length) * 100)
          : 100;

      // Assessment Performance: average score for matched skills with assessment data
      let assessmentPerformance = 50; // default if no assessment
      if (assessmentSkillScores && assessmentSkillScores.length > 0) {
        const relevantScores = assessmentSkillScores.filter((ss) =>
          allSkills.includes(ss.skill)
        );
        if (relevantScores.length > 0) {
          assessmentPerformance = Math.round(
            relevantScores.reduce((sum, ss) => sum + ss.score, 0) /
              relevantScores.length
          );
        }
      }

      const readinessScore = Math.round(
        WEIGHTS.profileMatch * profileMatch +
          WEIGHTS.skillCoverage * skillCoverage +
          WEIGHTS.assessmentPerformance * assessmentPerformance
      );

      results.push({
        companyId: company.id,
        companyName: company.name,
        roleTitle: role.title,
        readinessScore,
        breakdown: {
          profileMatch,
          skillCoverage,
          assessmentPerformance,
        },
        matchedSkills,
        missingSkills,
        totalRequired: role.requiredSkills.length,
      });
    }
  }

  return results.sort((a, b) => b.readinessScore - a.readinessScore);
}
