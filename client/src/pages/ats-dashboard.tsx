import { useEffect, useMemo, useState } from "react";
import { useLocation } from "wouter";
import { ArrowRight, BarChart3, CheckCircle2, FileText, Info, Loader2 } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { getUserResumesApi, getResumeAnalysisApi } from "@/lib/api";

import { AtsScoreBreakdownChart } from "@/components/charts/ats-score-breakdown";

export default function AtsDashboard() {
  const [, setLocation] = useLocation();
  const { resumeFileName, analysis, setResume } = useResumeStore();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!analysis) {
      setLoading(true);
      getUserResumesApi()
        .then(async (resumes) => {
          if (resumes && resumes.length > 0) {
            const latest = resumes[0];
            try {
              const fullResume = await getResumeAnalysisApi(latest.id);
              if (fullResume) {
                setResume({
                  resumeFileName: latest.file_name,
                  resumeText: "",
                  analysis: fullResume,
                });
              }
            } catch (e) {}
          }
        })
        .catch(() => {})
        .finally(() => setLoading(false));
    }
  }, [analysis, setResume]);

  const missing = useMemo((): string[] => {
    if (!analysis) return [];
    return analysis.ats.missingTopKeywords.slice(0, 10);
  }, [analysis]);

  if (loading) {
    return (
      <AppShell current="ats">
        <Card className="ai-card p-6 flex items-center justify-center gap-3">
          <Loader2 className="h-5 w-5 animate-spin text-primary" />
          <span className="text-sm text-muted-foreground">Loading your resume analysis...</span>
        </Card>
      </AppShell>
    );
  }

  if (!analysis) {
    return (
      <AppShell current="ats">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-muted-foreground">
              <Info className="h-5 w-5" />
            </div>
            <div>
              <div className="font-medium" data-testid="text-empty-ats-title">
                No resume analyzed yet
              </div>
              <div className="text-sm text-muted-foreground" data-testid="text-empty-ats-subtitle">
                Go back to upload a PDF or use the sample.
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


  return (
    <AppShell current="ats">
      <div className="ai-fade-in space-y-6">
        <div className="flex flex-col gap-2">
          <div className="flex flex-wrap items-center gap-2">
            <Badge data-testid="status-ats" variant="secondary" className="gap-1">
              <BarChart3 className="h-3.5 w-3.5" />
              ATS Score Dashboard
            </Badge>
            <Badge data-testid="status-file" variant="secondary" className="gap-1">
              <FileText className="h-3.5 w-3.5" />
              {resumeFileName ?? "Resume"}
            </Badge>
          </div>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">
            Your ATS-style score
          </h2>
          <p className="text-muted-foreground max-w-2xl">
            A transparent, rule-based score using weighted sections and keyword coverage.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-3">
          <Card className="ai-card p-5 md:p-6">
            <div className="text-sm text-muted-foreground">Overall ATS Score</div>
            <div
              className="mt-2 flex items-end gap-2"
              data-testid="text-ats-overall"
            >
              <div className="ai-title text-4xl font-semibold">
                {analysis.ats.overallScore}
              </div>
              <div className="pb-1 text-sm text-muted-foreground">/ 100</div>
            </div>
            <div className="mt-4" data-testid="progress-ats-overall">
              <Progress value={analysis.ats.overallScore} />
            </div>
          </Card>

          <Card className="ai-card p-5 md:p-6">
            <div className="text-sm text-muted-foreground">Keyword Coverage</div>
            <div className="mt-2 flex items-end gap-2" data-testid="text-ats-coverage">
              <div className="ai-title text-4xl font-semibold">
                {analysis.ats.keywordCoverage}
              </div>
              <div className="pb-1 text-sm text-muted-foreground">%</div>
            </div>
            <div className="mt-4" data-testid="progress-ats-coverage">
              <Progress value={analysis.ats.keywordCoverage} />
            </div>
          </Card>

          <Card className="ai-card p-5 md:p-6">
            <div className="text-sm text-muted-foreground">Format & Structure</div>
            <div className="mt-2 flex items-end gap-2" data-testid="text-ats-format">
              <div className="ai-title text-4xl font-semibold">
                {analysis.ats.sectionScores.format}
              </div>
              <div className="pb-1 text-sm text-muted-foreground">/ 100</div>
            </div>
            <div className="mt-4" data-testid="progress-ats-format">
              <Progress value={analysis.ats.sectionScores.format} />
            </div>
          </Card>
        </div>

        <div className="grid gap-4 lg:grid-cols-[1.35fr_0.65fr]">
          <Card className="ai-card p-5 md:p-6">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="font-medium" data-testid="text-breakdown-title">
                  Score breakdown
                </div>
                <div className="text-sm text-muted-foreground">
                  Weightages are applied per section for the final score.
                </div>
              </div>
              <Badge data-testid="badge-weighted" variant="secondary" className="gap-1">
                <CheckCircle2 className="h-3.5 w-3.5" />
                Weighted
              </Badge>
            </div>

            <div className="mt-5" data-testid="chart-ats-breakdown">
              <AtsScoreBreakdownChart analysis={analysis} />
            </div>
          </Card>

          <Card className="ai-card p-5 md:p-6">
            <div className="font-medium" data-testid="text-missing-title">
              Missing top keywords
            </div>
            <div className="mt-2 text-sm text-muted-foreground">
              Add these naturally where relevant.
            </div>

            <div className="mt-4 flex flex-wrap gap-2" data-testid="list-missing-keywords">
              {missing.length ? (
                missing.map((k: string) => (
                  <Badge
                    key={k}
                    variant="outline"
                    data-testid={`badge-missing-${k.replaceAll(" ", "-")}`}
                  >
                    {k}
                  </Badge>
                ))
              ) : (
                <div className="text-sm text-muted-foreground" data-testid="text-missing-none">
                  Great coverage—no major gaps detected.
                </div>
              )}
            </div>

            <div className="mt-5">
              <Button
                data-testid="button-next-skills"
                className="w-full gap-2"
                onClick={() => setLocation("/skills")}
              >
                Next: Skill Gap Analysis
                <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
