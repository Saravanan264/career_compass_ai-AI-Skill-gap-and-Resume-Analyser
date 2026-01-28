import { PropsWithChildren, useMemo } from "react";
import { Link } from "wouter";
import {
  BarChart3,
  Compass,
  FileUp,
  GraduationCap,
  LayoutGrid,
  Sparkles,
  Target,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useResumeStore } from "@/state/resume-store";

type NavKey = "upload" | "ats" | "skills" | "roadmap" | "insights";

function NavItem({
  href,
  active,
  icon,
  label,
  testId,
}: {
  href: string;
  active: boolean;
  icon: React.ReactNode;
  label: string;
  testId: string;
}) {
  return (
    <Link href={href} data-testid={testId}>
      <a
        className={
          "flex items-center gap-2 rounded-xl px-3 py-2 text-sm transition-colors hover:bg-muted/70 " +
          (active ? "bg-muted text-foreground" : "text-muted-foreground")
        }
      >
        <span className={active ? "text-primary" : "text-muted-foreground"}>{icon}</span>
        <span className="font-medium">{label}</span>
      </a>
    </Link>
  );
}

export function AppShell({
  children,
  current,
}: PropsWithChildren<{ current: NavKey }>) {
  const { analysis, resumeFileName } = useResumeStore();

  const step = useMemo(() => {
    const order: NavKey[] = ["upload", "ats", "skills", "roadmap", "insights"];
    return order.indexOf(current) + 1;
  }, [current]);

  return (
    <div className="min-h-screen ai-grid">
      <div className="mx-auto max-w-6xl px-4 py-6 md:px-6 md:py-8">
        <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-2xl bg-primary/15 text-primary grid place-items-center shadow-sm">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <div className="ai-title font-semibold" data-testid="text-app-title">
                AI Resume Analyzer
              </div>
              <div className="text-xs text-muted-foreground" data-testid="text-app-subtitle">
                ATS score • skill gaps • roadmap • insights
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <Badge data-testid="badge-step" variant="secondary" className="gap-1">
              <LayoutGrid className="h-3.5 w-3.5" />
              Step {step} / 5
            </Badge>
            {analysis ? (
              <Badge data-testid="badge-overall" variant="secondary" className="gap-1">
                <BarChart3 className="h-3.5 w-3.5" />
                ATS {analysis.ats.overallScore}/100
              </Badge>
            ) : null}
            {resumeFileName ? (
              <Badge data-testid="badge-filename" variant="secondary" className="gap-1">
                <FileUp className="h-3.5 w-3.5" />
                {resumeFileName}
              </Badge>
            ) : null}
            <Button
              data-testid="button-dark-toggle"
              variant="secondary"
              className="gap-2"
              onClick={() => {
                document.documentElement.classList.toggle("dark");
              }}
            >
              <Compass className="h-4 w-4" />
              Toggle theme
            </Button>
          </div>
        </header>

        <div className="mt-6 grid gap-4 lg:grid-cols-[260px_1fr]">
          <aside className="lg:sticky lg:top-6 h-fit">
            <Card className="ai-card ai-glass p-3">
              <nav className="flex flex-col gap-1">
                <NavItem
                  href="/upload"
                  active={current === "upload"}
                  icon={<FileUp className="h-4 w-4" />}
                  label="Resume Upload"
                  testId="link-nav-upload"
                />
                <NavItem
                  href="/ats"
                  active={current === "ats"}
                  icon={<BarChart3 className="h-4 w-4" />}
                  label="ATS Dashboard"
                  testId="link-nav-ats"
                />
                <NavItem
                  href="/skills"
                  active={current === "skills"}
                  icon={<Target className="h-4 w-4" />}
                  label="Skill Gap Analysis"
                  testId="link-nav-skills"
                />
                <NavItem
                  href="/roadmap"
                  active={current === "roadmap"}
                  icon={<GraduationCap className="h-4 w-4" />}
                  label="Learning Roadmap"
                  testId="link-nav-roadmap"
                />
                <NavItem
                  href="/insights"
                  active={current === "insights"}
                  icon={<Compass className="h-4 w-4" />}
                  label="Career Insights"
                  testId="link-nav-insights"
                />
              </nav>
            </Card>

            <div className="mt-4">
              <Card className="ai-card p-4">
                <div className="text-sm font-medium" data-testid="text-mini-title">
                  Best-fit domain
                </div>
                <div className="mt-1 ai-title text-lg font-semibold" data-testid="text-mini-domain">
                  {analysis?.bestFitDomain ?? "—"}
                </div>
                <div className="mt-2 text-xs text-muted-foreground" data-testid="text-mini-note">
                  Rule-based matching (demo).
                </div>
              </Card>
            </div>
          </aside>

          <main className="min-w-0">{children}</main>
        </div>
      </div>
    </div>
  );
}
