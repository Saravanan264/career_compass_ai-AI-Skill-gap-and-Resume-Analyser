import { create } from "zustand";
import { persist } from "zustand/middleware";

export type SkillScore = {
  skill: string;
  score: number;
  total: number;
  correct: number;
  status?: "strong" | "moderate" | "weak";
  isRequired?: boolean;
};

export type QuestionResultItem = {
  id: string;
  text: string;
  skill: string;
  difficulty: string;
  selectedAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
};

export type AssessmentAttempt = {
  id: string;
  roleId: string;
  roleTitle: string;
  date: string;
  overallScore: number;
  totalQuestions: number;
  correctAnswers: number;
  skillScores: SkillScore[];
  answers: Record<string, number>;
  timeTakenSeconds: number;
  explanation?: string;
  questionResults?: QuestionResultItem[];
  skillFeedback?: Array<{ skill: string; assessmentScore: number; status: string }>;
};

type AssessmentStore = {
  attempts: AssessmentAttempt[];
  currentAnswers: Record<string, number>;
  currentQuestionIds: string[];
  assessmentStartTime: number | null;

  addAttempt: (attempt: AssessmentAttempt) => void;
  setAttempts: (attempts: AssessmentAttempt[]) => void;
  setCurrentAnswers: (answers: Record<string, number>) => void;
  setCurrentAnswer: (questionId: string, answerIndex: number) => void;
  setCurrentQuestionIds: (ids: string[]) => void;
  setAssessmentStartTime: (time: number) => void;
  clearCurrent: () => void;
  clearAll: () => void;
};

export const useAssessmentStore = create<AssessmentStore>()(
  persist(
    (set, get) => ({
      attempts: [],
      currentAnswers: {},
      currentQuestionIds: [],
      assessmentStartTime: null,

      addAttempt: (attempt) =>
        set((s) => ({ attempts: [...s.attempts, attempt] })),
      setAttempts: (attempts) => set({ attempts }),
      setCurrentAnswers: (answers) => set({ currentAnswers: answers }),
      setCurrentAnswer: (questionId, answerIndex) =>
        set((s) => ({
          currentAnswers: { ...s.currentAnswers, [questionId]: answerIndex },
        })),
      setCurrentQuestionIds: (ids) => set({ currentQuestionIds: ids }),
      setAssessmentStartTime: (time) => set({ assessmentStartTime: time }),
      clearCurrent: () =>
        set({
          currentAnswers: {},
          currentQuestionIds: [],
          assessmentStartTime: null,
        }),
      clearAll: () =>
        set({
          attempts: [],
          currentAnswers: {},
          currentQuestionIds: [],
          assessmentStartTime: null,
        }),
    }),
    { name: "career-compass-assessment" }
  )
);
