import { create } from "zustand";
import { persist } from "zustand/middleware";

export type AtsSectionScores = {
  format: number;
  experience: number;
  skills: number;
  education: number;
  impact: number;
};

export type AtsAnalysis = {
  overallScore: number;
  keywordCoverage: number;
  sectionScores: AtsSectionScores;
  missingTopKeywords: string[];
};

export type DomainFit = {
  fitScore: number;
  have: string[];
  missing: string[];
};

export type RoadmapStage = {
  title: string;
  goal: string;
  duration: string;
  courses: string[];
  projects: string[];
  status?: "Not Started" | "In Progress" | "Completed" | "Needs Review";
  priority?: "High" | "Medium" | "Low";
  explanation?: string;
  focusSkills?: string[];
};

export type FinalScoreMetric = {
  key: string;
  label: string;
  score: number;
  note: string;
};

export type FinalScorecard = {
  resumeScore: number;
  metrics: FinalScoreMetric[];
};

export type ResumeAnalysis = {
  isValidResume?: boolean;
  validationReason?: string;
  ats: AtsAnalysis;
  skillsDetected: string[];
  domains: Record<string, DomainFit>;
  bestFitDomain: string;
  confidence: number;
  finalScorecard: FinalScorecard;
};


type ResumeStore = {
  resumeFileName: string | null;
  resumeText: string;
  analysis: ResumeAnalysis | null;
  setResume: (payload: {
    resumeFileName: string;
    resumeText: string;
    analysis: ResumeAnalysis;
  }) => void;
  clearResume: () => void;
  clearAll: () => void;
};

export const useResumeStore = create<ResumeStore>()(
  persist(
    (set) => ({
      resumeFileName: null,
      resumeText: "",
      analysis: null,
      setResume: ({ resumeFileName, resumeText, analysis }) =>
        set({ resumeFileName, resumeText, analysis }),
      clearResume: () =>
        set({ resumeFileName: null, resumeText: "", analysis: null }),
      clearAll: () =>
        set({ resumeFileName: null, resumeText: "", analysis: null }),
    }),
    { name: "career-compass-resume" }
  )
);
