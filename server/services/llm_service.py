import os
import json
import urllib.request
import urllib.error

class LLMService:
    def __init__(self):
        self.enabled = os.getenv("LLM_ENABLED", "false").lower() in ("true", "1", "t")
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def is_available(self) -> bool:
        return self.enabled and bool(self.api_key.strip())

    def _call_openai_api(self, system_prompt: str, user_prompt: str) -> str:
        if not self.is_available():
            raise ValueError("LLM service is disabled or API key is missing")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]

    def generate_ats_explanation(self, ats_scorecard: dict) -> dict:
        """
        Generate optional LLM natural-language feedback for ATS scorecard.
        Falls back cleanly to deterministic explanation if LLM is disabled or fails.
        """
        score_val = ats_scorecard.get('overallScore', ats_scorecard.get('overallAtsScore', 0))
        fallback = {
            "summary": f"Your resume achieved an overall ATS score of {score_val}%. Core areas like format and skills align with general industry standards.",
            "actionableTips": [
                "Ensure top required keywords are prominently placed under Work Experience.",
                "Use standard section headers like Work Experience and Technical Skills.",
                "Quantify achievements using metrics and percentages."
            ],
            "source": "deterministic_fallback"
        }

        if not self.is_available():
            return fallback

        system_prompt = (
            "You are an expert ATS resume consultant. Use ONLY the provided resume ATS scorecard context. "
            "Do NOT invent candidate experience, do NOT claim guaranteed hiring, do NOT produce unsupported numerical scores. "
            "Return JSON matching key 'summary' (string) and 'actionableTips' (array of strings)."
        )
        user_prompt = f"ATS Scorecard Context: {json.dumps(ats_scorecard)}"

        try:
            raw_res = self._call_openai_api(system_prompt, user_prompt)
            parsed = json.loads(raw_res)
            return {
                "summary": str(parsed.get("summary", fallback["summary"])),
                "actionableTips": list(parsed.get("actionableTips", fallback["actionableTips"])),
                "source": "llm_enhanced"
            }
        except Exception:
            return fallback

    def generate_skill_gap_explanation(self, skill: str, requirement: str, candidate_status: str, assessment_score: float = None) -> dict:
        """
        Generate optional LLM skill gap natural-language explanation.
        """
        fallback = {
            "explanation": f"{skill} is a {requirement} skill for your target role. Currently classified as '{candidate_status}', focused practice is recommended to close this requirement gap.",
            "nextSteps": f"Review foundational documentation for {skill} and complete a practical project milestone.",
            "source": "deterministic_fallback"
        }

        if not self.is_available():
            return fallback

        system_prompt = (
            "You are a technical career advisor. Use ONLY the supplied skill gap context. "
            "Do NOT invent requirements or candidate skills. Return JSON matching 'explanation' (string) and 'nextSteps' (string)."
        )
        user_prompt = f"Skill: {skill}, Requirement: {requirement}, Candidate Status: {candidate_status}, Assessment Score: {assessment_score}"

        try:
            raw_res = self._call_openai_api(system_prompt, user_prompt)
            parsed = json.loads(raw_res)
            return {
                "explanation": str(parsed.get("explanation", fallback["explanation"])),
                "nextSteps": str(parsed.get("nextSteps", fallback["nextSteps"])),
                "source": "llm_enhanced"
            }
        except Exception:
            return fallback

    def generate_roadmap_explanation(self, stage_title: str, focus_skills: list, priority: str) -> dict:
        """
        Generate optional LLM explanation for why a roadmap stage is prioritized.
        """
        fallback = {
            "rationale": f"Stage '{stage_title}' is marked as {priority} Priority because it targets critical skills ({', '.join(focus_skills)}) required for your target job description.",
            "source": "deterministic_fallback"
        }

        if not self.is_available():
            return fallback

        system_prompt = (
            "You are a learning path advisor. Explain concisely why the roadmap stage is prioritized based ONLY on supplied context. "
            "Return JSON matching key 'rationale' (string)."
        )
        user_prompt = f"Stage: {stage_title}, Focus Skills: {focus_skills}, Priority: {priority}"

        try:
            raw_res = self._call_openai_api(system_prompt, user_prompt)
            parsed = json.loads(raw_res)
            return {
                "rationale": str(parsed.get("rationale", fallback["rationale"])),
                "source": "llm_enhanced"
            }
        except Exception:
            return fallback

llm_service = LLMService()
