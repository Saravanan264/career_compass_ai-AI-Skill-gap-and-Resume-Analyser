import type { AssessmentAttempt } from "@/state/assessment-store";

export type SkillProgress = {
  skill: string;
  scores: { attempt: number; date: string; score: number }[];
  latestScore: number;
  previousScore: number | null;
  improvement: number | null;
  attemptCount: number;
  status: "Weak" | "Developing" | "Strong";
  trend: "improving" | "declining" | "stable" | "Not Enough Data";
};

export type AnalyticsSummary = {
  totalAttempts: number;
  averageScore: number;
  bestScore: number;
  latestScore: number;
  overallImprovement: number;
  strongestSkill: string | null;
  weakestSkill: string | null;
  skillProgress: SkillProgress[];
};

/**
 * Compute analytics from assessment attempt history deterministically.
 */
export function computeAnalytics(attempts: AssessmentAttempt[]): AnalyticsSummary {
  if (!attempts || attempts.length === 0) {
    return {
      totalAttempts: 0,
      averageScore: 0,
      bestScore: 0,
      latestScore: 0,
      overallImprovement: 0,
      strongestSkill: null,
      weakestSkill: null,
      skillProgress: [],
    };
  }

  const sorted = [...attempts].sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
  );

  const totalAttempts = sorted.length;
  const averageScore = Math.round(
    sorted.reduce((sum, a) => sum + a.overallScore, 0) / totalAttempts
  );
  const bestScore = Math.max(...sorted.map((a) => a.overallScore));
  const latestScore = sorted[sorted.length - 1].overallScore;
  const overallImprovement =
    sorted.length >= 2
      ? sorted[sorted.length - 1].overallScore - sorted[0].overallScore
      : 0;

  // Build skill progress map
  const skillMap: Record<string, { attempt: number; date: string; score: number }[]> = {};

  sorted.forEach((attempt, idx) => {
    (attempt.skillScores || []).forEach((ss) => {
      if (!skillMap[ss.skill]) skillMap[ss.skill] = [];
      skillMap[ss.skill].push({
        attempt: idx + 1,
        date: attempt.date,
        score: ss.score,
      });
    });
  });

  const skillProgress: SkillProgress[] = Object.entries(skillMap).map(
    ([skill, scores]) => {
      const attemptCount = scores.length;
      const latest = scores[scores.length - 1].score;
      const previous = attemptCount >= 2 ? scores[scores.length - 2].score : null;
      const improvement = previous !== null ? latest - previous : null;

      let status: "Weak" | "Developing" | "Strong" = "Developing";
      if (latest >= 70) status = "Strong";
      else if (latest < 50) status = "Weak";

      let trend: "improving" | "declining" | "stable" | "Not Enough Data" = "Not Enough Data";
      if (improvement !== null) {
        if (improvement > 5) trend = "improving";
        else if (improvement < -5) trend = "declining";
        else trend = "stable";
      }

      return {
        skill,
        scores,
        latestScore: latest,
        previousScore: previous,
        improvement,
        attemptCount,
        status,
        trend,
      };
    }
  );

  skillProgress.sort((a, b) => b.latestScore - a.latestScore);

  const strongestSkill =
    skillProgress.length > 0 ? skillProgress[0].skill : null;
  const weakestSkill =
    skillProgress.length > 0
      ? skillProgress[skillProgress.length - 1].skill
      : null;

  return {
    totalAttempts,
    averageScore,
    bestScore,
    latestScore,
    overallImprovement,
    strongestSkill,
    weakestSkill,
    skillProgress,
  };
}
