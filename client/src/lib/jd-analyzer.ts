import skillsDb from "@/data/skills.json";
import jobRolesDb from "@/data/job-roles.json";
import type { JdAnalysis } from "@/state/job-store";

const allSkills = skillsDb.skills;

function normalize(text: string) {
  return text
    .toLowerCase()
    .replaceAll(/[^a-z0-9+.#\s-]/g, " ")
    .replaceAll(/\s+/g, " ")
    .trim();
}

/** Extract skills from free-text JD by matching against skills database */
function extractSkillsFromText(text: string): string[] {
  const normText = normalize(text);
  const found: string[] = [];

  for (const s of allSkills) {
    const keywords = [s.name, ...(s.keywords ?? [])];
    const hit = keywords.some((k) => normText.includes(normalize(k)));
    if (hit && !found.includes(s.name)) {
      found.push(s.name);
    }
  }

  return found;
}

/** Analyze a JD from free text — extract required/preferred skills */
export function analyzeJdText(text: string): JdAnalysis {
  const detectedSkills = extractSkillsFromText(text);
  const normText = normalize(text);

  // Heuristic: skills mentioned near "required" are required, near "preferred"/"nice to have" are preferred
  const requiredSkills: string[] = [];
  const preferredSkills: string[] = [];

  for (const skill of detectedSkills) {
    // Simple heuristic — check if skill appears in a "preferred" or "nice to have" context
    const skillLower = normalize(skill);
    const prefPatterns = ["preferred", "nice to have", "bonus", "good to have", "optional", "desirable"];
    const isPreferred = prefPatterns.some((p) => {
      const idx = normText.indexOf(skillLower);
      if (idx === -1) return false;
      const surrounding = normText.slice(Math.max(0, idx - 120), idx + skillLower.length + 120);
      return surrounding.includes(p);
    });

    if (isPreferred) {
      preferredSkills.push(skill);
    } else {
      requiredSkills.push(skill);
    }
  }

  // Assign importance: required skills get 8-10, preferred get 4-6
  const importance: Record<string, number> = {};
  requiredSkills.forEach((s, i) => {
    importance[s] = Math.max(7, 10 - Math.floor(i * 0.5));
  });
  preferredSkills.forEach((s, i) => {
    importance[s] = Math.max(4, 6 - Math.floor(i * 0.5));
  });

  return {
    rawText: text,
    requiredSkills,
    preferredSkills,
    allSkills: [...requiredSkills, ...preferredSkills],
    importance,
  };
}

/** Create a JdAnalysis from a predefined job role */
export function analyzeJobRole(roleId: string): JdAnalysis | null {
  const role = (jobRolesDb as any).roles.find((r: any) => r.id === roleId);
  if (!role) return null;

  return {
    rawText: `${role.title}: ${role.description}`,
    requiredSkills: role.requiredSkills,
    preferredSkills: role.preferredSkills,
    allSkills: [...role.requiredSkills, ...role.preferredSkills],
    importance: role.importance,
  };
}
