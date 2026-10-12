export const API_URL = "http://localhost:8000/api";

export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const authStore = localStorage.getItem("career-compass-auth");
  let token = null;
  if (authStore) {
    try {
      const parsed = JSON.parse(authStore);
      token = parsed.state?.accessToken;
    } catch (e) {}
  }

  const headers: Record<string, string> = { ...((options.headers as Record<string, string>) || {}) };

  // Only default to application/json if body is not FormData
  if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export async function uploadResumeApi(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  return fetchWithAuth("/resumes/upload", {
    method: "POST",
    body: formData,
  });
}

export async function getUserResumesApi() {
  return fetchWithAuth("/resumes");
}

export async function getResumeAnalysisApi(resumeId: string) {
  return fetchWithAuth(`/resumes/${resumeId}/analysis`);
}

export async function createJobDescriptionApi(payload: { title?: string; company_name?: string; description: string }) {
  return fetchWithAuth("/job-descriptions", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getUserJobDescriptionsApi() {
  return fetchWithAuth("/job-descriptions");
}

export async function getJobDescriptionAnalysisApi(jdId: string) {
  return fetchWithAuth(`/job-descriptions/${jdId}/analysis`);
}

export async function createAssessmentAttemptApi(payload: {
  role_id?: string;
  role_title: string;
  overall_score: number;
  time_taken_seconds: number;
  question_count: number;
  skill_breakdown: Record<string, any>;
}) {
  return fetchWithAuth("/assessments", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getUserAssessmentAttemptsApi() {
  return fetchWithAuth("/assessments");
}

export async function getSkillRoadmapApi(skill: string) {
  return fetchWithAuth(`/roadmap/skill/${encodeURIComponent(skill)}`);
}

export async function getLlmStatusApi() {
  return fetchWithAuth("/llm/status").catch(() => ({ enabled: false, available: false, provider: "none" }));
}

export async function getLlmAtsExplanationApi(payload: { overallScore: number; keywordCoverage: number; missingTopKeywords: string[] }) {
  return fetchWithAuth("/llm/explain-ats", {
    method: "POST",
    body: JSON.stringify(payload),
  }).catch(() => ({
    summary: `Overall score of ${payload.overallScore}%. Resume contains relevant structure.`,
    actionableTips: ["Quantify accomplishments with metrics.", "Tailor keywords to target JD."],
    source: "deterministic_fallback"
  }));
}

export async function getLlmSkillGapExplanationApi(payload: { skill: string; requirement: string; candidate_status: string; assessment_score?: number }) {
  return fetchWithAuth("/llm/explain-skill-gap", {
    method: "POST",
    body: JSON.stringify(payload),
  }).catch(() => ({
    explanation: `${payload.skill} is a ${payload.requirement} skill for target role. Currently classified as ${payload.candidate_status}.`,
    nextSteps: `Review documentation and complete a practical project focused on ${payload.skill}.`,
    source: "deterministic_fallback"
  }));
}

export async function getLlmRoadmapExplanationApi(payload: { stage_title: string; focus_skills: string[]; priority: string }) {
  return fetchWithAuth("/llm/explain-roadmap", {
    method: "POST",
    body: JSON.stringify(payload),
  }).catch(() => ({
    rationale: `Stage ${payload.stage_title} is marked as ${payload.priority} Priority to target key required skills (${payload.focus_skills.join(", ")}).`,
    source: "deterministic_fallback"
  }));
}
