import { useMemo } from "react";
import { useLocation } from "wouter";
import { ArrowRight, GraduationCap, Info, Layers, Rocket } from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

import { buildRoadmap } from "@/lib/roadmap";

function useQueryParam(name: string) {
  const [location] = useLocation();
  return useMemo(() => {
    const q = location.split("?")[1] ?? "";
    const params = new URLSearchParams(q);
    return params.get(name);
  }, [location, name]);
}

export default function LearningRoadmap() {
  const [, setLocation] = useLocation();
  const { analysis } = useResumeStore();
  const domainParam = useQueryParam("domain") ?? analysis?.bestFitDomain ?? "Data Science";

  const roadmap = useMemo(() => {
    if (!analysis) return null;
    return buildRoadmap({ analysis, domain: domainParam });
  }, [analysis, domainParam]);

  if (!analysis || !roadmap) {
    return (
      <AppShell current="roadmap">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-muted-foreground">
              <Info className="h-5 w-5" />
            </div>
            <div>
              <div className="font-medium" data-testid="text-empty-roadmap-title">
                No roadmap yet
              </div>
              <div className="text-sm text-muted-foreground" data-testid="text-empty-roadmap-subtitle">
                Upload a resume and pick a domain first.
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
    <AppShell current="roadmap">
      <div className="ai-fade-in space-y-6">
        <div className="flex flex-col gap-2">
          <div className="flex flex-wrap items-center gap-2">
            <Badge data-testid="status-roadmap" variant="secondary" className="gap-1">
              <GraduationCap className="h-3.5 w-3.5" />
              Learning Roadmap
            </Badge>
            <Badge data-testid="status-domain" variant="secondary" className="gap-1">
              <Layers className="h-3.5 w-3.5" />
              {roadmap.domain}
            </Badge>
          </div>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Your vertical roadmap</h2>
          <p className="text-muted-foreground max-w-2xl">
            A step-by-step plan. Each stage includes courses and projects designed to close
            your biggest gaps first.
          </p>
        </div>

        <div className="grid gap-4 lg:grid-cols-[1fr_0.75fr]">
          <Card className="ai-card p-5 md:p-6">
            <div className="font-medium" data-testid="text-roadmap-title">
              Stages
            </div>
            <div className="mt-4 space-y-4" data-testid="list-roadmap-stages">
              {roadmap.stages.map((stage, idx) => (
                <div key={stage.title} className="relative">
                  <div className="absolute left-3 top-0 bottom-0 w-px bg-border" />
                  <div className="relative flex gap-4">
                    <div className="mt-0.5 h-7 w-7 rounded-full bg-primary/15 text-primary grid place-items-center">
                      <span className="text-xs font-semibold" data-testid={`text-stage-index-${idx}`}>
                        {idx + 1}
                      </span>
                    </div>
                    <div className="flex-1">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div className="ai-title text-lg font-semibold" data-testid={`text-stage-title-${idx}`}>
                          {stage.title}
                        </div>
                        <Badge data-testid={`badge-stage-duration-${idx}`} variant="secondary">
                          {stage.duration}
                        </Badge>
                      </div>
                      <div className="mt-1 text-sm text-muted-foreground" data-testid={`text-stage-goal-${idx}`}>
                        {stage.goal}
                      </div>

                      <div className="mt-3 grid gap-3 md:grid-cols-2">
                        <Card className="ai-card p-4">
                          <div className="text-sm font-medium" data-testid={`text-stage-courses-${idx}`}>
                            Courses
                          </div>
                          <ul className="mt-2 space-y-1 text-sm text-muted-foreground">
                            {stage.courses.map((c) => (
                              <li key={c} data-testid={`row-course-${idx}-${c.replaceAll(" ", "-")}`}>
                                • {c}
                              </li>
                            ))}
                          </ul>
                        </Card>

                        <Card className="ai-card p-4">
                          <div className="text-sm font-medium" data-testid={`text-stage-projects-${idx}`}>
                            Projects
                          </div>
                          <ul className="mt-2 space-y-1 text-sm text-muted-foreground">
                            {stage.projects.map((p) => (
                              <li key={p} data-testid={`row-project-${idx}-${p.replaceAll(" ", "-")}`}>
                                • {p}
                              </li>
                            ))}
                          </ul>
                        </Card>
                      </div>

                      {idx !== roadmap.stages.length - 1 ? (
                        <div className="pt-4">
                          <Separator />
                        </div>
                      ) : null}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <div className="space-y-4">
            <Card className="ai-card p-5 md:p-6">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <div className="font-medium" data-testid="text-roadmap-summary-title">
                    Summary
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Your plan at a glance.
                  </div>
                </div>
                <Badge data-testid="badge-stages-count" variant="secondary">
                  {roadmap.stages.length} stages
                </Badge>
              </div>

              <div className="mt-4 grid gap-3">
                <Card className="ai-card p-4">
                  <div className="text-xs text-muted-foreground">Estimated timeline</div>
                  <div className="mt-1 ai-title text-2xl font-semibold" data-testid="text-roadmap-timeline">
                    {roadmap.totalDuration}
                  </div>
                </Card>

                <Card className="ai-card p-4">
                  <div className="text-xs text-muted-foreground">Focus skills</div>
                  <div className="mt-2 flex flex-wrap gap-2" data-testid="list-roadmap-focus">
                    {roadmap.focusSkills.slice(0, 12).map((s) => (
                      <Badge key={s} data-testid={`badge-focus-${s.replaceAll(" ", "-")}`}>
                        {s}
                      </Badge>
                    ))}
                  </div>
                </Card>
              </div>

              <Button
                data-testid="button-next-insights"
                className="mt-5 w-full gap-2"
                onClick={() => setLocation("/insights")}
              >
                Next: Career Insights
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Card>

            <Card className="ai-card p-5 md:p-6">
              <div className="flex items-center gap-2 text-sm">
                <Rocket className="h-4 w-4 text-primary" />
                <span className="font-medium" data-testid="text-roadmap-tip-title">
                  Showcase tip
                </span>
              </div>
              <div className="mt-2 text-sm text-muted-foreground" data-testid="text-roadmap-tip-body">
                In a demo, open this page to show the vertical stage layout and how missing
                skills become actionable steps.
              </div>
            </Card>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
