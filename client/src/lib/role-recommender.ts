import jobRolesDb from "@/data/job-roles.json";

export type RoleSuitability = {
  roleId: string;
  title: string;
  description: string;
  suitabilityScore: number;
  matchedSkills: string[];
  missingRequired: string[];
  missingPreferred: string[];
  totalRequired: number;
  requiredCoverage: number;
};

/**
 * Compare student profile against all predefined job roles.
 * Returns sorted list of role suitabilities.
 */
export function calculateRoleSuitability(
  resumeSkills: string[],
  assessmentScores?: Record<string, number>
): RoleSuitability[] {
  const roles = (jobRolesDb as any).roles as Array<{
    id: string;
    title: string;
    description: string;
    requiredSkills: string[];
    preferredSkills: string[];
    importance: Record<string, number>;
  }>;

  return roles
    .map((role) => {
      const allRoleSkills = [...role.requiredSkills, ...role.preferredSkills];
      const matchedSkills = allRoleSkills.filter((s) => resumeSkills.includes(s));
      const missingRequired = role.requiredSkills.filter((s) => !resumeSkills.includes(s));
      const missingPreferred = role.preferredSkills.filter((s) => !resumeSkills.includes(s));

      // Weighted suitability
      const totalImportance = allRoleSkills.reduce(
        (sum, s) => sum + (role.importance[s] ?? 5),
        0
      );
      const matchedImportance = matchedSkills.reduce(
        (sum, s) => sum + (role.importance[s] ?? 5),
        0
      );

      let suitabilityScore = totalImportance > 0
        ? Math.round((matchedImportance / totalImportance) * 100)
        : 0;

      // If assessment scores exist, blend them in (20% weight)
      if (assessmentScores) {
        const assessedSkills = matchedSkills.filter((s) => assessmentScores[s] !== undefined);
        if (assessedSkills.length > 0) {
          const avgAssessment = assessedSkills.reduce(
            (sum, s) => sum + (assessmentScores[s] ?? 0),
            0
          ) / assessedSkills.length;
          suitabilityScore = Math.round(suitabilityScore * 0.8 + avgAssessment * 0.2);
        }
      }

      const requiredCoverage =
        role.requiredSkills.length > 0
          ? Math.round(
              ((role.requiredSkills.length - missingRequired.length) /
                role.requiredSkills.length) *
                100
            )
          : 100;

      return {
        roleId: role.id,
        title: role.title,
        description: role.description,
        suitabilityScore,
        matchedSkills,
        missingRequired,
        missingPreferred,
        totalRequired: role.requiredSkills.length,
        requiredCoverage,
      };
    })
    .sort((a, b) => b.suitabilityScore - a.suitabilityScore);
}
