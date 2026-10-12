import { useMemo } from "react";
import { useLocation } from "wouter";
import { ArrowRight, BriefcaseBusiness, Info, CheckCircle } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { useAssessmentStore } from "@/state/assessment-store";
import { useJobStore } from "@/state/job-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { calculateRoleSuitability } from "@/lib/role-recommender";
import { analyzeJobRole } from "@/lib/jd-analyzer";
import { matchResumeToJd } from "@/lib/skill-matcher";

export default function JobRoles() {
  const [, setLocation] = useLocation();
  const { analysis } = useResumeStore();
  const { attempts } = useAssessmentStore();
  const { selectJobRole, selectedRoleId } = useJobStore();

  const roles = useMemo(() => {
    if (!analysis) return [];
    const latestAttempt = attempts.length > 0 ? attempts[attempts.length - 1] : undefined;
    const assessmentScores = latestAttempt
      ? Object.fromEntries(latestAttempt.skillScores.map((s) => [s.skill, s.score]))
      : undefined;
    return calculateRoleSuitability(analysis.skillsDetected, assessmentScores);
  }, [analysis, attempts]);

  const handleSelectRole = (roleId: string, title: string) => {
    const roleJd = analyzeJobRole(roleId);
    if (roleJd) {
      const match = analysis?.skillsDetected ? matchResumeToJd(analysis.skillsDetected, roleJd) : null;
      selectJobRole(roleId, title, roleJd, match);
      setLocation("/skills");
    }
  };

  if (!analysis) {
    return (
      <AppShell current="job-roles">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">No resume analyzed yet</div>
              <div className="text-sm text-muted-foreground">Upload a resume to see suitable job roles.</div>
              <Button className="mt-4" onClick={() => setLocation("/upload")}>Go to Upload</Button>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }

  const suitabilityColor = (score: number) => {
    if (score >= 80) return "text-emerald-600";
    if (score >= 60) return "text-amber-600";
    return "text-rose-600";
  };

  return (
    <AppShell current="job-roles">
      <div className="ai-fade-in space-y-6">
        <div>
          <div className="flex flex-wrap items-center gap-2 mb-2">
            <Badge variant="secondary" className="gap-1"><BriefcaseBusiness className="h-3.5 w-3.5" />Job Role Suitability</Badge>
          </div>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Best Suitable Job Roles</h2>
          <p className="text-muted-foreground max-w-2xl mt-1">Your profile is compared against multiple job roles based on skill coverage and assessment performance.</p>
        </div>

        <Card className="ai-card p-4">
          <div className="flex items-start gap-2 text-sm">
            <Info className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
            <span className="text-muted-foreground">These scores are <strong>profile alignment indicators</strong>, not guaranteed job selection probabilities. Click <strong>Analyze Skill Gap</strong> on any role to compare your resume.</span>
          </div>
        </Card>

        <div className="grid gap-4">
          {roles.map((role, idx) => {
            const isSelected = selectedRoleId === role.roleId;
            return (
              <Card key={role.roleId} className={`ai-card p-5 transition-all ${isSelected ? "border-primary ring-1 ring-primary/20" : ""}`}>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-xl bg-primary/10 text-primary grid place-items-center font-semibold">{idx + 1}</div>
                    <div>
                      <div className="font-medium flex items-center gap-2">
                        {role.title}
                        {isSelected && <Badge variant="default" className="text-xs gap-1 bg-emerald-600"><CheckCircle className="h-3 w-3" />Active Target Role</Badge>}
                      </div>
                      <div className="text-sm text-muted-foreground mt-0.5">{role.description}</div>
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <div className={`ai-title text-2xl font-semibold ${suitabilityColor(role.suitabilityScore)}`}>{role.suitabilityScore}%</div>
                    <div className="text-xs text-muted-foreground">suitability</div>
                  </div>
                </div>
                <div className="mt-4"><Progress value={role.suitabilityScore} /></div>
                <div className="mt-4 grid gap-3 sm:grid-cols-3">
                  <div>
                    <div className="text-xs text-muted-foreground mb-1.5">Matched ({role.matchedSkills.length})</div>
                    <div className="flex flex-wrap gap-1">{role.matchedSkills.slice(0, 6).map((s) => <Badge key={s} variant="secondary" className="text-xs">{s}</Badge>)}</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground mb-1.5">Missing Required ({role.missingRequired.length})</div>
                    <div className="flex flex-wrap gap-1">{role.missingRequired.map((s) => <Badge key={s} variant="outline" className="text-xs text-rose-600">{s}</Badge>)}</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground mb-1.5">Missing Preferred ({role.missingPreferred.length})</div>
                    <div className="flex flex-wrap gap-1">{role.missingPreferred.slice(0, 4).map((s) => <Badge key={s} variant="outline" className="text-xs">{s}</Badge>)}</div>
                  </div>
                </div>
                <div className="mt-4 flex items-center justify-between pt-3 border-t">
                  <div className="text-xs text-muted-foreground">Required coverage: {role.requiredCoverage}% ({role.totalRequired - role.missingRequired.length}/{role.totalRequired})</div>
                  <Button size="sm" className="gap-1.5" onClick={() => handleSelectRole(role.roleId, role.title)}>
                    {isSelected ? "View Skill Gap" : "Analyze Skill Gap"} <ArrowRight className="h-3.5 w-3.5" />
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>

        <Button onClick={() => setLocation("/assessment")} className="gap-2">Start Mock Assessment <ArrowRight className="h-4 w-4" /></Button>
      </div>
    </AppShell>
  );
}

