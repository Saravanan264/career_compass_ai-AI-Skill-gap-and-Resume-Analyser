import { useMemo } from "react";
import { useLocation } from "wouter";
import {
  Award,
  Briefcase,
  CheckCircle2,
  Gauge,
  Info,
  Sparkles,
  Target,
} from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import type { FinalScoreMetric } from "@/state/resume-store";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

import { DomainFitRadarChart } from "@/components/charts/domain-fit-radar";

function badgeForReadiness(score: number) {
  if (score >= 85) return { label: "Ready", tone: "good" as const };
  if (score >= 70) return { label: "Almost Ready", tone: "ok" as const };
  return { label: "Building", tone: "warn" as const };
}

export default function CareerInsights() {
  const [, setLocation] = useLocation();
  const { resumeFileName, analysis } = useResumeStore();

  const best = useMemo(() => {
    if (!analysis) return null;
    const d = analysis.bestFitDomain;
    return {
      domain: d,
      fit: analysis.domains[d]?.fitScore ?? 0,
    };
  }, [analysis]);

  if (!analysis || !best) {
    return (
      <AppShell current="insights">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-muted-foreground">
              <Info className="h-5 w-5" />
            </div>
            <div>
              <div className="font-medium" data-testid="text-empty-insights-title">
                No insights yet
              </div>
              <div className="text-sm text-muted-foreground" data-testid="text-empty-insights-subtitle">
                Upload a resume to generate your scorecard.
              </div>
              <Button
                data-testid="button-go-upload"
                className="mt-4"
                onClick={() => setLocation("/upload")}
              >
                Go to Upload
              </Button>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }

  const readiness = badgeForReadiness(analysis.finalScorecard.resumeScore);
  const confidence = analysis.confidence;

  return (
    <AppShell current="insights">
      <div className="ai-fade-in space-y-6">
        <div className="flex flex-col gap-2">
          <div className="flex flex-wrap items-center gap-2">
            <Badge data-testid="status-insights" variant="secondary" className="gap-1">
              <Briefcase className="h-3.5 w-3.5" />
              Career Insights
            </Badge>
            <Badge data-testid="status-file" variant="secondary" className="gap-1">
              <CheckCircle2 className="h-3.5 w-3.5" />
              {resumeFileName ?? "Resume"}
            </Badge>
          </div>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Your final scorecard</h2>
          <p className="text-muted-foreground max-w-2xl">
            Best-fit domain recommendation, confidence, readiness badge, and a clean resume
            scorecard.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Card className="ai-card p-5 md:p-6">
            <div className="text-sm text-muted-foreground">Best-fit domain</div>
            <div className="mt-2 ai-title text-2xl font-semibold" data-testid="text-best-domain">
              {best.domain}
            </div>
            <div className="mt-3" data-testid="progress-best-domain">
              <Progress value={best.fit} />
            </div>
            <div className="mt-2 text-xs text-muted-foreground" data-testid="text-domain-fit">
              Match score: {best.fit}%
            </div>
          </Card>

          <Card className="ai-card p-5 md:p-6">
            <div className="text-sm text-muted-foreground">Confidence score</div>
            <div className="mt-2 ai-title text-2xl font-semibold" data-testid="text-confidence">
              {confidence}%
            </div>
            <div className="mt-3" data-testid="progress-confidence">
              <Progress value={confidence} />
            </div>
            <div className="mt-2 text-xs text-muted-foreground">
              Higher when skill signals are strong and consistent.
            </div>
          </Card>

          <Card className="ai-card p-5 md:p-6">
            <div className="text-sm text-muted-foreground">Career readiness badge</div>
            <div className="mt-2 flex items-center gap-2" data-testid="badge-readiness">
              <span
                className={
                  readiness.tone === "good"
                    ? "rounded-full bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 px-3 py-1 text-sm font-medium"
                    : readiness.tone === "ok"
                      ? "rounded-full bg-amber-500/15 text-amber-600 dark:text-amber-400 px-3 py-1 text-sm font-medium"
                      : "rounded-full bg-sky-500/15 text-sky-600 dark:text-sky-400 px-3 py-1 text-sm font-medium"
                }
              >
                {readiness.label}
              </span>
              <span className="text-xs text-muted-foreground">(based on resume score)</span>
            </div>
          </Card>
        </div>

        <div className="grid gap-4 lg:grid-cols-[1.15fr_0.85fr]">
          <Card className="ai-card p-5 md:p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium" data-testid="text-radar-title">
                  Domain fit overview
                </div>
                <div className="text-sm text-muted-foreground">
                  Compare your fit across top career domains.
                </div>
              </div>
              <Badge data-testid="badge-ai" variant="secondary" className="gap-1">
                <Sparkles className="h-3.5 w-3.5" />
                Insight
              </Badge>
            </div>

            <div className="mt-5" data-testid="chart-domain-radar">
              <DomainFitRadarChart analysis={analysis} />
            </div>
          </Card>

          <Card className="ai-card p-5 md:p-6">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="font-medium" data-testid="text-scorecard-title">
                  Final resume scorecard
                </div>
                <div className="text-sm text-muted-foreground">
                  A simple breakdown you can act on.
                </div>
              </div>
              <Badge data-testid="badge-score" variant="secondary" className="gap-1">
                <Award className="h-3.5 w-3.5" />
                {analysis.finalScorecard.resumeScore}/100
              </Badge>
            </div>

            <div className="mt-4 space-y-3" data-testid="list-scorecard">
              {analysis.finalScorecard.metrics.map((m: FinalScoreMetric) => (
                <div
                  key={m.key}
                  className="rounded-xl border border-border/80 bg-background/40 p-3"
                  data-testid={`row-metric-${m.key}`}
                >
                  <div className="flex items-center justify-between">
                    <div className="text-sm font-medium">{m.label}</div>
                    <div className="text-sm text-muted-foreground">{m.score}/100</div>
                  </div>
                  <div className="mt-2">
                    <Progress value={m.score} />
                  </div>
                  <div className="mt-2 text-xs text-muted-foreground">{m.note}</div>
                </div>
              ))}
            </div>

            <div className="mt-5 grid gap-2">
              <Button
                data-testid="button-back-ats"
                variant="secondary"
                className="w-full"
                onClick={() => setLocation("/ats")}
              >
                Back to ATS Dashboard
              </Button>
              <Button
                data-testid="button-start-over"
                className="w-full"
                onClick={() => setLocation("/upload")}
              >
                Start Over
              </Button>
            </div>
          </Card>
        </div>

        <Card className="ai-card p-5 md:p-6">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-primary">
              <Gauge className="h-5 w-5" />
            </div>
            <div>
              <div className="font-medium" data-testid="text-insights-note-title">
                How this recommendation works
              </div>
              <div className="text-sm text-muted-foreground" data-testid="text-insights-note-body">
                We score each domain by matching your detected skills to a target skills
                map. Confidence is based on signal strength (coverage and consistency).
              </div>
              <div className="mt-3 flex flex-wrap items-center gap-2 text-sm">
                <Badge data-testid="badge-best" variant="secondary" className="gap-1">
                  <Target className="h-3.5 w-3.5" />
                  Best-fit: {best.domain}
                </Badge>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </AppShell>
  );
}
