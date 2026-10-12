import { useMemo } from "react";
import { useLocation } from "wouter";
import { ArrowRight, Building2, Info, Shield } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { useAssessmentStore } from "@/state/assessment-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { calculateReadiness } from "@/lib/readiness-engine";

export default function Readiness() {
  const [, setLocation] = useLocation();
  const { analysis } = useResumeStore();
  const { attempts } = useAssessmentStore();

  const readinessData = useMemo(() => {
    if (!analysis) return [];
    const latestAttempt = attempts.length > 0 ? attempts[attempts.length - 1] : undefined;
    return calculateReadiness(analysis.skillsDetected, latestAttempt?.skillScores);
  }, [analysis, attempts]);

  if (!analysis) {
    return (
      <AppShell current="readiness">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">No data available</div>
              <div className="text-sm text-muted-foreground">Upload a resume to calculate readiness scores.</div>
              <Button className="mt-4" onClick={() => setLocation("/upload")}>Go to Upload</Button>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }

  const readinessColor = (score: number) => {
    if (score >= 80) return "text-emerald-600";
    if (score >= 60) return "text-amber-600";
    return "text-rose-600";
  };

  const readinessLabel = (score: number) => {
    if (score >= 80) return "Ready";
    if (score >= 60) return "Almost Ready";
    return "Building";
  };

  return (
    <AppShell current="readiness">
      <div className="ai-fade-in space-y-6">
        <div>
          <Badge variant="secondary" className="gap-1 mb-2"><Shield className="h-3.5 w-3.5" />Career Readiness</Badge>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Job & Company Readiness</h2>
          <p className="text-muted-foreground max-w-2xl mt-1">See how prepared you are for each company based on your profile, skills, and assessment performance.</p>
        </div>

        <Card className="ai-card p-4">
          <div className="flex items-start gap-2 text-sm">
            <Info className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
            <span className="text-muted-foreground">The readiness score is a <strong>preparation and profile-alignment indicator</strong>. It is not a prediction or guarantee of job selection. Formula: <code className="text-xs bg-muted px-1 py-0.5 rounded">0.30 × Profile Match + 0.30 × Skill Coverage + 0.40 × Assessment</code></span>
          </div>
        </Card>

        <div className="grid gap-4">
          {readinessData.map((company) => (
            <Card key={`${company.companyId}-${company.roleTitle}`} className="ai-card p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-xl bg-muted grid place-items-center">
                    <Building2 className="h-5 w-5 text-muted-foreground" />
                  </div>
                  <div>
                    <div className="font-medium">{company.companyName}</div>
                    <div className="text-sm text-muted-foreground">{company.roleTitle}</div>
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <div className={`ai-title text-2xl font-semibold ${readinessColor(company.readinessScore)}`}>{company.readinessScore}%</div>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    company.readinessScore >= 80 ? "bg-emerald-500/10 text-emerald-600" :
                    company.readinessScore >= 60 ? "bg-amber-500/10 text-amber-600" :
                    "bg-rose-500/10 text-rose-600"
                  }`}>{readinessLabel(company.readinessScore)}</span>
                </div>
              </div>

              <div className="mt-4"><Progress value={company.readinessScore} /></div>

              <div className="mt-4 grid gap-3 sm:grid-cols-3">
                <div className="rounded-xl border p-3">
                  <div className="text-xs text-muted-foreground">Profile Match</div>
                  <div className="text-lg font-semibold mt-1">{company.breakdown.profileMatch}%</div>
                  <Progress value={company.breakdown.profileMatch} className="mt-1.5" />
                </div>
                <div className="rounded-xl border p-3">
                  <div className="text-xs text-muted-foreground">Skill Coverage</div>
                  <div className="text-lg font-semibold mt-1">{company.breakdown.skillCoverage}%</div>
                  <Progress value={company.breakdown.skillCoverage} className="mt-1.5" />
                </div>
                <div className="rounded-xl border p-3">
                  <div className="text-xs text-muted-foreground">Assessment</div>
                  <div className="text-lg font-semibold mt-1">{company.breakdown.assessmentPerformance}%</div>
                  <Progress value={company.breakdown.assessmentPerformance} className="mt-1.5" />
                </div>
              </div>

              {company.missingSkills.length > 0 && (
                <div className="mt-3">
                  <div className="text-xs text-muted-foreground mb-1.5">Missing ({company.missingSkills.length}):</div>
                  <div className="flex flex-wrap gap-1">{company.missingSkills.slice(0, 6).map((s) => <Badge key={s} variant="outline" className="text-xs">{s}</Badge>)}</div>
                </div>
              )}
            </Card>
          ))}
        </div>

        <Button variant="secondary" onClick={() => setLocation("/dashboard")} className="gap-2">Back to Dashboard <ArrowRight className="h-4 w-4" /></Button>
      </div>
    </AppShell>
  );
}
