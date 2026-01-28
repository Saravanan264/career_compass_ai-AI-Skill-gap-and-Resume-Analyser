import { create } from "zustand";

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
  clearAll: () => void;
};

export const useResumeStore = create<ResumeStore>((set) => ({
  resumeFileName: null,
  resumeText: "",
  analysis: null,
  setResume: ({ resumeFileName, resumeText, analysis }) =>
    set({ resumeFileName, resumeText, analysis }),
  clearAll: () => set({ resumeFileName: null, resumeText: "", analysis: null }),
}));
