import questionsDb from "@/data/questions.json";
import type { AssessmentAttempt, SkillScore, QuestionResultItem } from "@/state/assessment-store";
import { getCanonicalSkillName } from "./skill-matcher";

export type AssessmentQuestion = {
  id: string;
  skill: string;
  difficulty: string;
  text: string;
  options: string[];
  correctIndex: number;
};

// Implied / related skill mappings based on technology ecosystems
const RELATED_TECH_MAP: Record<string, string[]> = {
  React: ["JavaScript", "HTML", "CSS", "REST API", "Git"],
  JavaScript: ["React", "HTML", "CSS", "Node.js", "REST API", "Git"],
  TypeScript: ["JavaScript", "React", "Node.js", "REST API", "Git"],
  Python: ["FastAPI", "Django", "SQL", "Machine Learning", "Data Analysis", "REST API", "Git", "Problem Solving"],
  FastAPI: ["Python", "REST API", "SQL", "Git"],
  Django: ["Python", "REST API", "SQL", "Git"],
  Java: ["Spring Boot", "SQL", "REST API", "Microservices", "System Design", "Git", "Problem Solving"],
  "Spring Boot": ["Java", "SQL", "REST API", "Microservices", "System Design", "Git"],
  "Node.js": ["JavaScript", "REST API", "MongoDB", "SQL", "Git"],
  "Data Analysis": ["Python", "SQL", "Statistics", "Data Visualization", "Machine Learning"],
  "Data Science": ["Python", "SQL", "Statistics", "Machine Learning", "Data Analysis"],
  "Machine Learning": ["Python", "SQL", "Statistics", "Deep Learning", "Data Analysis", "Problem Solving"],
  "ML Engineer": ["Python", "Machine Learning", "Deep Learning", "Docker", "REST API"],
};

const GENERAL_TECHNICAL_FOUNDATIONS = [
  "Git", "Problem Solving", "Testing", "REST API", "SQL", "System Design", "Microservices", "Linux", "Docker"
];

/**
 * Select questions for an assessment based on:
 * - Candidate resume detected skills (PRIMARY SOURCE)
 * - Target role context (SECONDARY PRIORITIZATION)
 * - Difficulty adjustment based on previous performance
 * - Exactly 30 questions with zero duplicate questions
 */
export function selectQuestions(
  targetSkills: string[] = [],
  missingRequiredSkills: string[] = [],
  missingPreferredSkills: string[] = [],
  existingSkills: string[] = [],
  previousScore?: number,
  maxQuestions = 30
): AssessmentQuestion[] {
  const allQuestions = (questionsDb as any).questions as AssessmentQuestion[];
  const selected: AssessmentQuestion[] = [];
  const usedIds = new Set<string>();

  // Determine difficulty preference
  let preferredDifficulties: string[] = ["Easy", "Medium", "Hard"];
  if (previousScore !== undefined) {
    if (previousScore >= 75) {
      preferredDifficulties = ["Medium", "Hard", "Easy"];
    } else if (previousScore < 50) {
      preferredDifficulties = ["Easy", "Medium", "Hard"];
    }
  }

  // Primary source: Candidate resume detected skills
  const resumeSkillsToUse = existingSkills.length > 0
    ? existingSkills
    : (targetSkills.length > 0 ? targetSkills : ["Python", "SQL", "Git"]);

  const resumeCanonicalSet = new Set<string>();
  resumeSkillsToUse.forEach((s) => {
    const c = getCanonicalSkillName(s);
    if (c) resumeCanonicalSet.add(c);
  });

  // Secondary context: Target role skills
  const targetCanonicalSet = new Set<string>();
  [...targetSkills, ...missingRequiredSkills, ...missingPreferredSkills].forEach((s) => {
    const c = getCanonicalSkillName(s);
    if (c) targetCanonicalSet.add(c);
  });

  // Build implied / related skills set for candidate's resume
  const candidateImpliedSet = new Set<string>(resumeCanonicalSet);
  resumeCanonicalSet.forEach((skill) => {
    const related = RELATED_TECH_MAP[skill] || [];
    related.forEach((r) => candidateImpliedSet.add(getCanonicalSkillName(r)));
  });
  GENERAL_TECHNICAL_FOUNDATIONS.forEach((f) => candidateImpliedSet.add(getCanonicalSkillName(f)));

  // Categorize questions into priority tiers
  const tier1: AssessmentQuestion[] = [];
  const tier2: AssessmentQuestion[] = [];
  const tier3: AssessmentQuestion[] = [];
  const tier4: AssessmentQuestion[] = [];

  for (const q of allQuestions) {
    const qCanonical = getCanonicalSkillName(q.skill);
    const isDirectResume = resumeCanonicalSet.has(qCanonical);
    const isTargetRole = targetCanonicalSet.has(qCanonical);
    const isCandidateImplied = candidateImpliedSet.has(qCanonical);

    if (isDirectResume && isTargetRole) {
      tier1.push(q);
    } else if (isDirectResume) {
      tier2.push(q);
    } else if (isCandidateImplied) {
      tier3.push(q);
    } else {
      tier4.push(q);
    }
  }

  // Helper to pick questions by difficulty while avoiding duplicate IDs
  const pickFromList = (list: AssessmentQuestion[], limit: number) => {
    for (const diff of preferredDifficulties) {
      const match = list.filter((q) => q.difficulty === diff && !usedIds.has(q.id));
      for (const q of match) {
        if (selected.length < limit) {
          selected.push(q);
          usedIds.add(q.id);
        }
      }
    }
    const fallback = list.filter((q) => !usedIds.has(q.id));
    for (const q of fallback) {
      if (selected.length < limit) {
        selected.push(q);
        usedIds.add(q.id);
      }
    }
  };

  // Pick Tier 1 questions (Resume skills overlapping with target role)
  pickFromList(tier1, maxQuestions);

  // Pick Tier 2 questions (Other direct resume skills)
  if (selected.length < maxQuestions) {
    pickFromList(tier2, maxQuestions);
  }

  // Pick Tier 3 questions (Candidate implied & foundational skills)
  if (selected.length < maxQuestions) {
    pickFromList(tier3, maxQuestions);
  }

  // Pick Tier 4 questions (General pool fallback if needed to reach maxQuestions)
  if (selected.length < maxQuestions) {
    pickFromList(tier4, maxQuestions);
  }

  return selected.slice(0, maxQuestions);
}

/**
 * Evaluate an assessment and produce skill-wise scores, detailed question results, and explanations.
 */
export function evaluateAssessment(
  questions: AssessmentQuestion[],
  answers: Record<string, number>,
  roleId: string,
  roleTitle: string,
  timeTakenSeconds: number,
  requiredSkillsList: string[] = []
): AssessmentAttempt {
  let totalCorrect = 0;
  const skillMap: Record<string, { correct: number; total: number }> = {};
  const questionResults: QuestionResultItem[] = [];

  for (const q of questions) {
    if (!skillMap[q.skill]) {
      skillMap[q.skill] = { correct: 0, total: 0 };
    }
    skillMap[q.skill].total++;

    const userAnsIdx = answers[q.id];
    const isCorrect = userAnsIdx === q.correctIndex;
    if (isCorrect) {
      totalCorrect++;
      skillMap[q.skill].correct++;
    }

    questionResults.push({
      id: q.id,
      text: q.text,
      skill: q.skill,
      difficulty: q.difficulty,
      selectedAnswer: userAnsIdx !== undefined ? (q.options[userAnsIdx] || "Not Answered") : "Not Answered",
      correctAnswer: q.options[q.correctIndex] || "",
      isCorrect
    });
  }

  const skillScores: SkillScore[] = Object.entries(skillMap).map(([skill, data]) => {
    const scorePct = data.total > 0 ? Math.round((data.correct / data.total) * 100) : 0;
    let status: "strong" | "moderate" | "weak" = "moderate";
    if (scorePct >= 75) status = "strong";
    else if (scorePct < 50) status = "weak";

    return {
      skill,
      score: scorePct,
      total: data.total,
      correct: data.correct,
      status,
      isRequired: requiredSkillsList.includes(skill)
    };
  });

  skillScores.sort((a, b) => b.score - a.score);

  const overallScore = questions.length > 0 ? Math.round((totalCorrect / questions.length) * 100) : 0;

  const strongSkills = skillScores.filter((s) => s.score >= 75).map((s) => s.skill);
  const weakSkills = skillScores.filter((s) => s.score < 50).map((s) => s.skill);

  let explanation = `Overall score: ${overallScore}%. `;
  if (strongSkills.length > 0) {
    explanation += `Strong performance in: ${strongSkills.join(", ")}. `;
  }
  if (weakSkills.length > 0) {
    explanation += `Improvement needed in: ${weakSkills.join(", ")}.`;
  } else {
    explanation += `Consistent performance across all tested skills.`;
  }

  const skillFeedback = skillScores.map((s) => ({
    skill: s.skill,
    assessmentScore: s.score,
    status: s.status || "moderate"
  }));

  return {
    id: `attempt-${Date.now()}`,
    roleId,
    roleTitle,
    date: new Date().toISOString(),
    overallScore,
    totalQuestions: questions.length,
    correctAnswers: totalCorrect,
    skillScores,
    answers,
    timeTakenSeconds,
    explanation,
    questionResults,
    skillFeedback
  };
}
