import { create } from "zustand";
import { persist } from "zustand/middleware";

export type SkillGapItem = {
  skill: string;
  status: "match" | "missing" | "improve";
  importance: number;
  priority: "high" | "medium" | "low";
  resumeEvidence: boolean;
  jdRequired: boolean;
  jdPreferred: boolean;
  matchType?: "exact" | "related" | "semantic" | "none";
  candidateRelatedSkill?: string;
  reason?: string;
  gapSeverity?: number;
};

export type JdAnalysis = {
  rawText: string;
  requiredSkills: string[];
  preferredSkills: string[];
  otherSkills?: string[];
  allSkills: string[];
  importance: Record<string, number>;
};

export type MatchResult = {
  matchingSkills: string[];
  missingSkills: string[];
  missingRequiredSkills?: string[];
  missingPreferredSkills?: string[];
  improvementAreas: string[];
  skillGaps: SkillGapItem[];
  jobMatchScore: number;
  skillCoverage: number;
  semanticSimilarityScore?: number;
  hybridMatchScore?: number;
  gapSummary?: {
    criticalGaps: string[];
    moderateGaps: string[];
    existingStrengths: string[];
    improvementAreas: string[];
  };
};

type JobStore = {
  selectedRoleId: string | null;
  selectedRoleTitle: string | null;
  jdText: string;
  jdAnalysis: JdAnalysis | null;
  matchResult: MatchResult | null;

  setSelectedRole: (id: string, title: string) => void;
  setJdText: (text: string) => void;
  setJdAnalysis: (analysis: JdAnalysis) => void;
  setMatchResult: (result: MatchResult) => void;
  selectJobRole: (id: string, title: string, analysis: JdAnalysis, match?: MatchResult | null) => void;
  clearJob: () => void;
};

export const useJobStore = create<JobStore>()(
  persist(
    (set) => ({
      selectedRoleId: null,
      selectedRoleTitle: null,
      jdText: "",
      jdAnalysis: null,
      matchResult: null,

      setSelectedRole: (id, title) => set({ selectedRoleId: id, selectedRoleTitle: title }),
      setJdText: (text) => set({ jdText: text }),
      setJdAnalysis: (analysis) => set({ jdAnalysis: analysis }),
      setMatchResult: (result) => set({ matchResult: result }),
      selectJobRole: (id, title, analysis, match = null) =>
        set({
          selectedRoleId: id,
          selectedRoleTitle: title,
          jdText: analysis.rawText,
          jdAnalysis: analysis,
          matchResult: match,
        }),
      clearJob: () =>
        set({
          selectedRoleId: null,
          selectedRoleTitle: null,
          jdText: "",
          jdAnalysis: null,
          matchResult: null,
        }),
    }),
    { name: "career-compass-job" }
  )
);

