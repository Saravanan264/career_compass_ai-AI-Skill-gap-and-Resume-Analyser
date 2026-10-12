import { useMemo } from "react";
import { useLocation } from "wouter";
import {
  ArrowRight,
  BarChart3,
  BookOpen,
  BriefcaseBusiness,
  ClipboardCheck,
  Compass,
  FileText,
  Layers,
  LineChart,
  Rocket,
  Shield,
  Target,
  TrendingUp,
} from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { useJobStore } from "@/state/job-store";
import { useAssessmentStore } from "@/state/assessment-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { computeAnalytics } from "@/lib/analytics-engine";
import { calculateReadiness } from "@/lib/readiness-engine";

function ScoreCard({
  label,
  score,
  icon,
  color,
}: {
  label: string;
  score: number | null;
  icon: React.ReactNode;
  color: string;
}) {
  return (
    <Card className="ai-card p-5">
      <div className="flex items-center gap-3">
        <div
          className={`h-10 w-10 rounded-xl grid place-items-center ${color}`}
        >
          {icon}
        </div>
        <div>
          <div className="text-sm text-muted-foreground">{label}</div>
          <div className="ai-title text-2xl font-semibold">
            {score !== null ? `${score}%` : "—"}
          </div>
        </div>
      </div>
      <div className="mt-3">
        <Progress value={score ?? 0} />
      </div>
    </Card>
  );
}

export default function Dashboard() {
  const [, setLocation] = useLocation();
  const { analysis } = useResumeStore();
  const { matchResult, selectedRoleTitle } = useJobStore();
  const { attempts } = useAssessmentStore();
  const resumeSkills = analysis?.skillsDetected ?? [];

  const analytics = useMemo(() => computeAnalytics(attempts), [attempts]);

  const readiness = useMemo(() => {
    if (resumeSkills.length === 0) return null;
    const latestAttempt = attempts.length > 0 ? attempts[attempts.length - 1] : null;
    const results = calculateReadiness(resumeSkills, latestAttempt?.skillScores);
    return results[0] ?? null;
  }, [resumeSkills, attempts]);

  const resumeScore = analysis?.ats.overallScore ?? null;
  const jobMatch = matchResult?.jobMatchScore ?? null;
  const skillCoverage = matchResult?.skillCoverage ?? null;
  const assessmentScore = analytics.totalAttempts > 0 ? analytics.latestScore : null;
  const readinessScore = readiness?.readinessScore ?? null;

  const hasResume = Boolean(analysis);
  const hasJob = Boolean(matchResult);

  return (
    <AppShell current="dashboard">
      <div className="ai-fade-in space-y-6">
        {/* Welcome */}
        <div>
          <h1 className="ai-title text-2xl md:text-3xl font-semibold">
            Your Career Readiness Overview
          </h1>
          <p className="mt-1 text-muted-foreground max-w-2xl">
            Track your progress across resume analysis, skill gaps, assessments,
            and career readiness — all in one place.
          </p>
        </div>

        {/* Score Cards */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <ScoreCard
            label="Resume Score"
            score={resumeScore}
            icon={<FileText className="h-5 w-5" />}
            color="bg-blue-500/10 text-blue-600"
          />
          <ScoreCard
            label="Job Match"
            score={jobMatch}
            icon={<Target className="h-5 w-5" />}
            color="bg-indigo-500/10 text-indigo-600"
          />
          <ScoreCard
            label="Skill Coverage"
            score={skillCoverage}
            icon={<Layers className="h-5 w-5" />}
            color="bg-violet-500/10 text-violet-600"
          />
          <ScoreCard
            label="Assessment"
            score={assessmentScore}
            icon={<ClipboardCheck className="h-5 w-5" />}
            color="bg-emerald-500/10 text-emerald-600"
          />
          <ScoreCard
            label="Readiness"
            score={readinessScore}
            icon={<Shield className="h-5 w-5" />}
            color="bg-amber-500/10 text-amber-600"
          />
        </div>

        {/* Target Role */}
        {selectedRoleTitle && (
          <Card className="ai-card p-5">
            <div className="flex items-center gap-3">
              <div className="h-9 w-9 rounded-xl bg-primary/10 text-primary grid place-items-center">
                <BriefcaseBusiness className="h-4.5 w-4.5" />
              </div>
              <div>
                <div className="text-sm text-muted-foreground">Target Role</div>
                <div className="font-semibold">{selectedRoleTitle}</div>
              </div>
            </div>
          </Card>
        )}

        {/* Quick Actions */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {!hasResume && (
            <Card className="ai-card p-5 border-dashed">
              <div className="flex items-start gap-3">
                <div className="h-9 w-9 rounded-xl bg-blue-500/10 text-blue-600 grid place-items-center shrink-0">
                  <FileText className="h-4.5 w-4.5" />
                </div>
                <div className="flex-1">
                  <div className="font-medium">Upload Resume</div>
                  <div className="mt-1 text-sm text-muted-foreground">
                    Start by uploading your resume to analyze skills and get your ATS score.
                  </div>
                  <Button
                    className="mt-3 gap-2"
                    size="sm"
                    onClick={() => setLocation("/upload")}
                  >
                    Get Started <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </Card>
          )}

          {hasResume && !hasJob && (
            <Card className="ai-card p-5 border-dashed">
              <div className="flex items-start gap-3">
                <div className="h-9 w-9 rounded-xl bg-indigo-500/10 text-indigo-600 grid place-items-center shrink-0">
                  <BriefcaseBusiness className="h-4.5 w-4.5" />
                </div>
                <div className="flex-1">
                  <div className="font-medium">Add Target Job</div>
                  <div className="mt-1 text-sm text-muted-foreground">
                    Select a job role or paste a job description to identify your skill gaps.
                  </div>
                  <Button
                    className="mt-3 gap-2"
                    size="sm"
                    onClick={() => setLocation("/job-analysis")}
                  >
                    Continue <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </Card>
          )}

          {hasResume && hasJob && analytics.totalAttempts === 0 && (
            <Card className="ai-card p-5 border-dashed">
              <div className="flex items-start gap-3">
                <div className="h-9 w-9 rounded-xl bg-emerald-500/10 text-emerald-600 grid place-items-center shrink-0">
                  <ClipboardCheck className="h-4.5 w-4.5" />
                </div>
                <div className="flex-1">
                  <div className="font-medium">Take Mock Assessment</div>
                  <div className="mt-1 text-sm text-muted-foreground">
                    Validate your skills through a role-specific assessment to track progress.
                  </div>
                  <Button
                    className="mt-3 gap-2"
                    size="sm"
                    onClick={() => setLocation("/assessment")}
                  >
                    Start Assessment <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </Card>
          )}
        </div>

        {/* Skill Gap Overview */}
        {matchResult && (
          <Card className="ai-card p-5">
            <div className="flex items-center justify-between gap-3">
              <div className="font-medium">Skill Gap Overview</div>
              <Button
                variant="secondary"
                size="sm"
                className="gap-2"
                onClick={() => setLocation("/skills")}
              >
                View Details <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              <div className="rounded-xl bg-emerald-500/5 border border-emerald-500/20 p-4">
                <div className="text-xs text-muted-foreground">Matching</div>
                <div className="mt-1 text-2xl font-semibold text-emerald-600">
                  {matchResult.matchingSkills.length}
                </div>
                <div className="mt-2 flex flex-wrap gap-1">
                  {matchResult.matchingSkills.slice(0, 5).map((s) => (
                    <Badge key={s} variant="secondary" className="text-xs">
                      {s}
                    </Badge>
                  ))}
                </div>
              </div>
              <div className="rounded-xl bg-rose-500/5 border border-rose-500/20 p-4">
                <div className="text-xs text-muted-foreground">Missing</div>
                <div className="mt-1 text-2xl font-semibold text-rose-600">
                  {matchResult.missingSkills.length}
                </div>
                <div className="mt-2 flex flex-wrap gap-1">
                  {matchResult.missingSkills.slice(0, 5).map((s) => (
                    <Badge key={s} variant="outline" className="text-xs">
                      {s}
                    </Badge>
                  ))}
                </div>
              </div>
              <div className="rounded-xl bg-amber-500/5 border border-amber-500/20 p-4">
                <div className="text-xs text-muted-foreground">Improvement</div>
                <div className="mt-1 text-2xl font-semibold text-amber-600">
                  {matchResult.improvementAreas.length}
                </div>
                <div className="mt-2 flex flex-wrap gap-1">
                  {matchResult.improvementAreas.slice(0, 5).map((s) => (
                    <Badge key={s} variant="outline" className="text-xs">
                      {s}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
          </Card>
        )}

        {/* Assessment Progress */}
        {analytics.totalAttempts > 0 && (
          <Card className="ai-card p-5">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="font-medium">Assessment Progress</div>
                <div className="text-sm text-muted-foreground">
                  {analytics.totalAttempts} attempt{analytics.totalAttempts !== 1 ? "s" : ""} completed
                </div>
              </div>
              <Button
                variant="secondary"
                size="sm"
                className="gap-2"
                onClick={() => setLocation("/analytics")}
              >
                View Analytics <LineChart className="h-4 w-4" />
              </Button>
            </div>
            <div className="mt-4 grid gap-3 sm:grid-cols-4">
              <div className="rounded-xl border p-3">
                <div className="text-xs text-muted-foreground">Latest Score</div>
                <div className="mt-1 ai-title text-xl font-semibold">{analytics.latestScore}%</div>
              </div>
              <div className="rounded-xl border p-3">
                <div className="text-xs text-muted-foreground">Best Score</div>
                <div className="mt-1 ai-title text-xl font-semibold">{analytics.bestScore}%</div>
              </div>
              <div className="rounded-xl border p-3">
                <div className="text-xs text-muted-foreground">Improvement</div>
                <div className="mt-1 ai-title text-xl font-semibold flex items-center gap-1">
                  {analytics.overallImprovement > 0 ? "+" : ""}
                  {analytics.overallImprovement}%
                  {analytics.overallImprovement > 0 && (
                    <TrendingUp className="h-4 w-4 text-emerald-500" />
                  )}
                </div>
              </div>
              <div className="rounded-xl border p-3">
                <div className="text-xs text-muted-foreground">Strongest</div>
                <div className="mt-1 text-sm font-semibold">
                  {analytics.strongestSkill ?? "—"}
                </div>
              </div>
            </div>
          </Card>
        )}

        {/* Next Action */}
        <Card className="ai-card p-5">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 h-9 w-9 rounded-xl bg-primary/10 text-primary grid place-items-center shrink-0">
              <Compass className="h-5 w-5" />
            </div>
            <div>
              <div className="font-medium">Recommended Next Step</div>
              <div className="mt-1 text-sm text-muted-foreground">
                {!hasResume
                  ? "Upload your resume to begin your career assessment journey."
                  : !hasJob
                    ? "Select a target job role or paste a job description to identify your exact skill gaps."
                    : analytics.totalAttempts === 0
                      ? "Take a mock assessment to validate your skills and start tracking improvement."
                      : "Review your skill analytics and update your roadmap based on your latest performance."}
              </div>
            </div>
          </div>
        </Card>

        {/* Navigation Cards */}
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { label: "Resume Analysis", icon: FileText, href: "/ats", color: "text-blue-600" },
            { label: "Skill Gap", icon: Target, href: "/skills", color: "text-rose-600" },
            { label: "Projects", icon: Rocket, href: "/projects", color: "text-violet-600" },
            { label: "Career Roadmap", icon: BookOpen, href: "/roadmap", color: "text-emerald-600" },
          ].map((item) => (
            <Card
              key={item.href}
              className="ai-card p-4 cursor-pointer transition-all hover:shadow-md hover:-translate-y-0.5"
              onClick={() => setLocation(item.href)}
            >
              <div className="flex items-center gap-3">
                <item.icon className={`h-5 w-5 ${item.color}`} />
                <span className="text-sm font-medium">{item.label}</span>
                <ArrowRight className="ml-auto h-4 w-4 text-muted-foreground" />
              </div>
            </Card>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
