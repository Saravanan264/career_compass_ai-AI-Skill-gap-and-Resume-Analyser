import { useMemo, useState } from "react";
import { useLocation } from "wouter";
import {
  ArrowRight,
  BadgeCheck,
  Boxes,
  Info,
  Target,
  Wand2,
} from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";

export default function SkillGapAnalysis() {
  const [, setLocation] = useLocation();
  const { analysis } = useResumeStore();
  const [domain, setDomain] = useState<string>(analysis?.bestFitDomain ?? "Data Science");

  const domainFit = useMemo(() => {
    if (!analysis) return null;
    return analysis.domains[domain];
  }, [analysis, domain]);

  if (!analysis) {
    return (
      <AppShell current="skills">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 text-muted-foreground">
              <Info className="h-5 w-5" />
            </div>
            <div>
              <div className="font-medium" data-testid="text-empty-skills-title">
                No analysis found
              </div>
              <div className="text-sm text-muted-foreground" data-testid="text-empty-skills-subtitle">
                Upload a resume first.
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

  const domains = Object.keys(analysis.domains);

  return (
    <AppShell current="skills">
      <div className="ai-fade-in space-y-6">
        <div className="flex flex-col gap-2">
          <div className="flex flex-wrap items-center gap-2">
            <Badge data-testid="status-skills" variant="secondary" className="gap-1">
              <Target className="h-3.5 w-3.5" />
              Skill Gap Analysis
            </Badge>
            <Badge data-testid="status-detected" variant="secondary" className="gap-1">
              <Wand2 className="h-3.5 w-3.5" />
              {analysis.skillsDetected.length} skills detected
            </Badge>
          </div>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Compare against a target domain</h2>
          <p className="text-muted-foreground max-w-2xl">
            Choose a domain to see what you already have and what to learn next.
          </p>
        </div>

        <Tabs value={domain} onValueChange={setDomain}>
          <TabsList className="flex flex-wrap" data-testid="tabs-domains">
            {domains.map((d: string) => (
              <TabsTrigger key={d} value={d} data-testid={`tab-domain-${d.replaceAll(" ", "-")}`}>
                {d}
              </TabsTrigger>
            ))}
          </TabsList>

          {domains.map((d: string) => {
            const fit = analysis.domains[d];
            return (
              <TabsContent key={d} value={d} className="mt-4">
                <div className="grid gap-4 lg:grid-cols-[1fr_0.8fr]">
                  <Card className="ai-card p-5 md:p-6">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <div className="font-medium" data-testid="text-domain-title">
                          {d} Fit
                        </div>
                        <div className="text-sm text-muted-foreground">
                          Skill match based on your resume keywords.
                        </div>
                      </div>
                      <Badge data-testid="badge-domain-fit" variant="secondary" className="gap-1">
                        <BadgeCheck className="h-3.5 w-3.5" />
                        {fit.fitScore}% match
                      </Badge>
                    </div>

                    <div className="mt-4" data-testid="progress-domain-fit">
                      <Progress value={fit.fitScore} />
                    </div>

                    <div className="mt-5 grid gap-3 md:grid-cols-2">
                      <Card className="ai-card p-4">
                        <div className="text-xs text-muted-foreground">You already have</div>
                        <div className="mt-1 ai-title text-2xl font-semibold" data-testid="text-have-count">
                          {fit.have.length}
                        </div>
                        <div className="mt-3 flex flex-wrap gap-2" data-testid="list-have">
                          {fit.have.slice(0, 14).map((s: string) => (
                            <Badge key={s} data-testid={`badge-have-${s.replaceAll(" ", "-")}`}>
                              {s}
                            </Badge>
                          ))}
                        </div>
                      </Card>

                      <Card className="ai-card p-4">
                        <div className="text-xs text-muted-foreground">You should learn next</div>
                        <div className="mt-1 ai-title text-2xl font-semibold" data-testid="text-missing-count">
                          {fit.missing.length}
                        </div>
                        <div className="mt-3 flex flex-wrap gap-2" data-testid="list-missing">
                          {fit.missing.slice(0, 14).map((s: string) => (
                            <Badge
                              key={s}
                              variant="outline"
                              data-testid={`badge-missing-${s.replaceAll(" ", "-")}`}
                            >
                              {s}
                            </Badge>
                          ))}
                        </div>
                      </Card>
                    </div>
                  </Card>

                  <Card className="ai-card p-5 md:p-6">
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <div className="font-medium" data-testid="text-next-title">
                          Next step
                        </div>
                        <div className="text-sm text-muted-foreground">
                          Generate a roadmap from this domain.
                        </div>
                      </div>
                      <Badge data-testid="badge-selected-domain" variant="secondary" className="gap-1">
                        <Boxes className="h-3.5 w-3.5" />
                        {d}
                      </Badge>
                    </div>

                    <div className="mt-4 text-sm text-muted-foreground">
                      We’ll turn the missing skills into an ordered plan with courses and
                      projects.
                    </div>

                    <Button
                      data-testid="button-next-roadmap"
                      className="mt-5 w-full gap-2"
                      onClick={() => setLocation(`/roadmap?domain=${encodeURIComponent(d)}`)}
                    >
                      Next: Learning Roadmap
                      <ArrowRight className="h-4 w-4" />
                    </Button>
                  </Card>
                </div>
              </TabsContent>
            );
          })}
        </Tabs>

        {domainFit ? (
          <div className="sr-only" data-testid="text-current-domain">
            {domainFit.fitScore}
          </div>
        ) : null}
      </div>
    </AppShell>
  );
}
