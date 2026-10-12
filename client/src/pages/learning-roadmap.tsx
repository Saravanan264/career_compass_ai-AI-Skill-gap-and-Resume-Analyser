import { useMemo, useState, useEffect } from "react";
import { useLocation } from "wouter";
import {
  ArrowRight,
  GraduationCap,
  Info,
  Layers,
  Rocket,
  CheckCircle2,
  BookOpen,
  ArrowLeft,
  ChevronRight,
  Code2,
  Terminal,
  Trophy,
  RefreshCw,
  Sparkles
} from "lucide-react";

import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { useJobStore } from "@/state/job-store";
import { useAssessmentStore } from "@/state/assessment-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { buildRoadmap } from "@/lib/roadmap";
import { recommendProjects } from "@/lib/project-recommender";
import { getSkillRoadmapApi } from "@/lib/api";

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
  const { jdAnalysis, matchResult } = useJobStore();
  const { attempts } = useAssessmentStore();
  const domainParam = useQueryParam("domain") ?? analysis?.bestFitDomain ?? "Data Science";
  const skillParam = useQueryParam("skill");

  const [activeSkill, setActiveSkill] = useState<string | null>(skillParam);
  const [skillRoadmapData, setSkillRoadmapData] = useState<any | null>(null);
  const [loadingSkillData, setLoadingSkillData] = useState(false);

  // Sync activeSkill when URL parameter changes
  useEffect(() => {
    if (skillParam) {
      setActiveSkill(skillParam);
    }
  }, [skillParam]);

  // Fetch skill-specific roadmap when activeSkill changes
  useEffect(() => {
    if (!activeSkill) {
      setSkillRoadmapData(null);
      return;
    }
    setLoadingSkillData(true);
    getSkillRoadmapApi(activeSkill)
      .then((data) => {
        setSkillRoadmapData(data);
      })
      .catch((err) => {
        console.warn("Failed to load skill roadmap:", err);
      })
      .finally(() => setLoadingSkillData(false));
  }, [activeSkill]);

  const recommendedProjects = useMemo(() => {
    if (!analysis) return [];
    return recommendProjects(
      matchResult?.missingRequiredSkills ?? matchResult?.missingSkills ?? [],
      matchResult?.missingPreferredSkills ?? [],
      matchResult?.improvementAreas ?? [],
      3
    );
  }, [analysis, matchResult]);

  const roadmap = useMemo(() => {
    if (!analysis) return null;
    return buildRoadmap({
      analysis,
      domain: domainParam,
      jdAnalysis,
      matchResult,
      assessmentAttempts: attempts,
      recommendedProjects
    });
  }, [analysis, domainParam, jdAnalysis, matchResult, attempts, recommendedProjects]);

  // List of all skills requiring attention/development
  const selectableSkills = useMemo(() => {
    const set = new Set<string>();
    if (matchResult) {
      matchResult.missingRequiredSkills?.forEach((s) => set.add(s));
      matchResult.missingSkills?.forEach((s) => set.add(s));
      matchResult.missingPreferredSkills?.forEach((s) => set.add(s));
      matchResult.improvementAreas?.forEach((s) => set.add(s));
    }
    if (set.size === 0 && analysis) {
      analysis.skillsDetected.forEach((s) => set.add(s));
    }
    // Default fallback skills if none detected
    if (set.size === 0) {
      ["Docker", "Microservices", "AWS", "Python", "React", "SQL", "FastAPI"].forEach((s) => set.add(s));
    }
    return Array.from(set);
  }, [matchResult, analysis]);

  if (!analysis || !roadmap) {
    return (
      <AppShell current="roadmap">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">No roadmap generated yet</div>
              <div className="text-sm text-muted-foreground">
                Upload a resume and select a job description first.
              </div>
              <Button className="mt-4" onClick={() => setLocation("/upload")}>
                Go to Upload
              </Button>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }

  // DETAILED SKILL-SPECIFIC ROADMAP VIEW (BASIC -> INTERMEDIATE -> ADVANCED -> PROJECT -> ASSESSMENT -> REASSESSMENT)
  if (activeSkill) {
    return (
      <AppShell current="roadmap">
        <div className="ai-fade-in space-y-6">
          <div className="flex items-center justify-between gap-4">
            <Button
              variant="outline"
              size="sm"
              className="gap-2"
              onClick={() => {
                setActiveSkill(null);
                setLocation("/roadmap");
              }}
            >
              <ArrowLeft className="h-4 w-4" /> Back to All Skill Roadmaps
            </Button>
            <Badge variant="secondary" className="gap-1">
              <BookOpen className="h-3.5 w-3.5" /> Skill Learning Path
            </Badge>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1">
              <Badge variant="default" className="text-xs">
                {activeSkill}
              </Badge>
              <span className="text-xs text-muted-foreground">Step-by-Step Skill Mastery</span>
            </div>
            <h2 className="ai-title text-2xl md:text-3xl font-semibold">
              {activeSkill} Learning Roadmap
            </h2>
            <p className="text-muted-foreground max-w-3xl mt-1">
              {skillRoadmapData?.overview || `Comprehensive learning path to master ${activeSkill} step-by-step.`}
            </p>
          </div>

          {loadingSkillData ? (
            <Card className="ai-card p-8 text-center text-muted-foreground">
              Loading {activeSkill} roadmap...
            </Card>
          ) : (
            <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
              {/* Main Vertical Visual Roadmap Timeline */}
              <div className="space-y-6">
                {/* START NODE */}
                <div className="flex items-center gap-3">
                  <div className="h-8 w-8 rounded-full bg-emerald-500 text-white font-bold text-xs grid place-items-center">
                    START
                  </div>
                  <div className="text-sm font-medium text-muted-foreground">
                    Prerequisites: {(skillRoadmapData?.prerequisites || ["Core Programming Concepts"]).join(" • ")}
                  </div>
                </div>

                {/* STAGES (BASIC -> INTERMEDIATE -> ADVANCED) */}
                <div className="relative pl-4 space-y-6 border-l-2 border-primary/20 ml-4">
                  {(skillRoadmapData?.stages || [
                    {
                      level: "Basic",
                      topics: [`What is ${activeSkill}?`, "Setup & Environment", "Core Syntax"],
                      tasks: [`Install and configure ${activeSkill}`, "Write baseline script"],
                      project: `Simple ${activeSkill} CLI Application`
                    },
                    {
                      level: "Intermediate",
                      topics: ["Core Architecture & Modules", "Data Handling", "API & Database Integration"],
                      tasks: ["Build modular application components", "Write automated tests"],
                      project: `Full ${activeSkill} Service Module`
                    },
                    {
                      level: "Advanced",
                      topics: ["Performance Optimization", "Security Best Practices", "CI/CD & Cloud Deployment"],
                      tasks: ["Optimize memory and execution speed", "Configure container deployment"],
                      project: `Production-Grade ${activeSkill} Ecosystem`
                    }
                  ]).map((stg: any, idx: number) => (
                    <div key={stg.level || idx} className="relative group">
                      <div className="absolute -left-[25px] top-1.5 h-4 w-4 rounded-full bg-primary border-4 border-background" />

                      <Card className="ai-card p-5 transition-all hover:border-primary/50">
                        <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                          <Badge
                            variant={
                              stg.level === "Basic"
                                ? "secondary"
                                : stg.level === "Intermediate"
                                ? "default"
                                : "outline"
                            }
                            className="font-medium"
                          >
                            LEVEL {idx + 1} — {(stg.level || "Core").toUpperCase()}
                          </Badge>
                          <span className="text-xs text-muted-foreground">Stage Goal</span>
                        </div>

                        <div className="grid gap-4 md:grid-cols-2">
                          <div>
                            <div className="text-xs font-semibold text-muted-foreground flex items-center gap-1.5 mb-2">
                              <BookOpen className="h-3.5 w-3.5 text-primary" /> What to Learn & Concepts
                            </div>
                            <ul className="space-y-1.5 text-xs">
                              {stg.topics.map((tp: string) => (
                                <li key={tp} className="flex items-start gap-1.5 text-muted-foreground">
                                  <ChevronRight className="h-3.5 w-3.5 text-primary shrink-0 mt-0.5" />
                                  <span>{tp}</span>
                                </li>
                              ))}
                            </ul>
                          </div>

                          <div>
                            <div className="text-xs font-semibold text-muted-foreground flex items-center gap-1.5 mb-2">
                              <Terminal className="h-3.5 w-3.5 text-emerald-500" /> Hands-on Practice Tasks
                            </div>
                            <ul className="space-y-1.5 text-xs">
                              {stg.tasks.map((tk: string) => (
                                <li key={tk} className="flex items-start gap-1.5 text-muted-foreground">
                                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500 shrink-0 mt-0.5" />
                                  <span>{tk}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>

                        {stg.project && (
                          <div className="mt-4 pt-3 border-t flex items-center justify-between text-xs">
                            <div className="flex items-center gap-1.5 text-primary font-medium">
                              <Code2 className="h-3.5 w-3.5" /> Level Milestone: {stg.project}
                            </div>
                            <Badge variant="outline" className="text-[10px]">
                              Milestone
                            </Badge>
                          </div>
                        )}
                      </Card>
                    </div>
                  ))}

                  {/* CAPSTONE REAL-WORLD PROJECT */}
                  <div className="relative group">
                    <div className="absolute -left-[25px] top-1.5 h-4 w-4 rounded-full bg-amber-500 border-4 border-background" />
                    <Card className="ai-card p-5 border-amber-500/30 bg-amber-500/5">
                      <div className="flex items-center gap-2 mb-2">
                        <Trophy className="h-4 w-4 text-amber-500" />
                        <span className="font-semibold text-sm">Project Practice</span>
                      </div>
                      <div className="text-sm font-medium">
                        {skillRoadmapData?.handsOnProjects?.[1] || `Build & Deploy ${activeSkill} Production Infrastructure`}
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">
                        Apply basic, intermediate, and advanced concepts in an end-to-end practical project.
                      </p>
                    </Card>
                  </div>

                  {/* PRACTICE & SKILL ASSESSMENT */}
                  <div className="relative group">
                    <div className="absolute -left-[25px] top-1.5 h-4 w-4 rounded-full bg-emerald-500 border-4 border-background" />
                    <Card className="ai-card p-5 border-emerald-500/30 bg-emerald-500/5">
                      <div className="flex items-center justify-between gap-3">
                        <div>
                          <div className="flex items-center gap-2">
                            <RefreshCw className="h-4 w-4 text-emerald-600" />
                            <span className="font-semibold text-sm">Practice & Skill Assessment</span>
                          </div>
                          <p className="text-xs text-muted-foreground mt-1">
                            Validate your {activeSkill} proficiency with role-aligned assessment questions.
                          </p>
                        </div>
                        <Button
                          size="sm"
                          className="gap-2 shrink-0"
                          onClick={() => setLocation("/assessment")}
                        >
                          Take Assessment <ArrowRight className="h-4 w-4" />
                        </Button>
                      </div>
                    </Card>
                  </div>
                </div>
              </div>

              {/* Sidebar with all clickable skills */}
              <div className="space-y-4">
                <Card className="ai-card p-5">
                  <div className="font-medium text-sm mb-3">Priority Skills</div>
                  <div className="space-y-2">
                    {selectableSkills.map((sk) => {
                      const isActive = sk.toLowerCase() === activeSkill.toLowerCase();
                      return (
                        <Card
                          key={sk}
                          className={`p-3 cursor-pointer transition-all text-xs flex items-center justify-between ${
                            isActive
                              ? "ring-2 ring-primary bg-primary/5 font-semibold"
                              : "hover:border-primary/40"
                          }`}
                          onClick={() => {
                            setActiveSkill(sk);
                            setLocation(`/roadmap?skill=${encodeURIComponent(sk)}`);
                          }}
                        >
                          <span>{sk}</span>
                          <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
                        </Card>
                      );
                    })}
                  </div>
                </Card>
              </div>
            </div>
          )}
        </div>
      </AppShell>
    );
  }

  // OVERVIEW ADAPTIVE ROADMAP VIEW WITH CLICKABLE SKILLS
  return (
    <AppShell current="roadmap">
      <div className="ai-fade-in space-y-6">
        <div className="flex flex-col gap-2">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="secondary" className="gap-1">
              <GraduationCap className="h-3.5 w-3.5" />
              Learning Roadmap
            </Badge>
            <Badge variant="secondary" className="gap-1">
              <Layers className="h-3.5 w-3.5" />
              {roadmap.domain}
            </Badge>
          </div>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Learning Roadmap</h2>
          <p className="text-muted-foreground max-w-2xl">
            Select any skill below to view its structured learning path from basic concepts to advanced projects.
          </p>
        </div>

        {/* CLICKABLE SKILL SELECTOR CARDS */}
        <Card className="ai-card p-5 border-primary/20 bg-primary/5">
          <div className="flex items-center gap-2 mb-3">
            <Sparkles className="h-4 w-4 text-primary" />
            <div className="font-medium text-sm">Priority Skills (Click to view skill roadmap)</div>
          </div>
          <div className="flex flex-wrap gap-2.5">
            {selectableSkills.map((sk) => (
              <Badge
                key={sk}
                className="cursor-pointer px-3.5 py-2 text-xs transition-all hover:scale-105 gap-1.5 shadow-sm"
                variant="default"
                onClick={() => {
                  setActiveSkill(sk);
                  setLocation(`/roadmap?skill=${encodeURIComponent(sk)}`);
                }}
              >
                <span>{sk}</span>
                <ArrowRight className="h-3 w-3" />
              </Badge>
            ))}
          </div>
        </Card>

        {/* ADAPTIVE STAGES OVERVIEW */}
        <div className="grid gap-4 lg:grid-cols-[1fr_0.75fr]">
          <Card className="ai-card p-5 md:p-6">
            <div className="flex items-center justify-between">
              <div className="font-medium">Learning Stages</div>
              <Badge variant="outline">{roadmap.stages.length} Stages</Badge>
            </div>

            <div className="mt-4 space-y-4">
              {roadmap.stages.map((stage, idx) => (
                <div key={stage.title} className="relative">
                  <div className="absolute left-3 top-0 bottom-0 w-px bg-border" />
                  <div className="relative flex gap-4 min-w-0">
                    <div className="mt-0.5 h-7 w-7 rounded-full bg-primary/15 text-primary grid place-items-center shrink-0">
                      <span className="text-xs font-semibold">{idx + 1}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div className="ai-title text-lg font-semibold">{stage.title}</div>
                        <div className="flex items-center gap-2">
                          {stage.priority && (
                            <Badge variant={stage.priority === "High" ? "destructive" : "secondary"}>
                              {stage.priority} Priority
                            </Badge>
                          )}
                          <Badge variant="outline">{stage.duration}</Badge>
                        </div>
                      </div>
                      <div className="mt-1 text-sm text-muted-foreground">{stage.goal}</div>

                      {stage.explanation && (
                        <div className="mt-2 text-xs bg-muted/50 p-2.5 rounded-lg text-muted-foreground border">
                          💡 <strong>Why Prioritized:</strong> {stage.explanation}
                        </div>
                      )}

                      <div className="mt-3 grid gap-3 md:grid-cols-2 min-w-0">
                        <Card className="ai-card p-4 min-w-0 w-full overflow-hidden">
                          <div className="text-sm font-medium">Focus Skills</div>
                          <div className="mt-2 flex flex-wrap gap-1.5 min-w-0">
                            {stage.courses.map((c) => (
                              <Badge
                                key={c}
                                variant="outline"
                                className="cursor-pointer hover:bg-primary/10 text-xs break-words max-w-full"
                                onClick={() => {
                                  setActiveSkill(c);
                                  setLocation(`/roadmap?skill=${encodeURIComponent(c)}`);
                                }}
                              >
                                <span className="truncate max-w-[200px]">{c}</span> →
                              </Badge>
                            ))}
                          </div>
                        </Card>

                        <Card className="ai-card p-4 min-w-0 w-full overflow-hidden">
                          <div className="text-sm font-medium">Projects & Milestones</div>
                          <ul className="mt-2 space-y-1.5 text-sm text-muted-foreground min-w-0 break-words [overflow-wrap:anywhere]">
                            {stage.projects.map((p) => (
                              <li key={p} className="break-words [overflow-wrap:anywhere] min-w-0 leading-normal">
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
              <div className="font-medium mb-3">Longitudinal Skill Progress</div>
              <div className="space-y-2.5">
                {roadmap.skillProgressList.slice(0, 6).map((sp) => (
                  <div
                    key={sp.skill}
                    className="flex items-center justify-between p-2.5 rounded-xl border text-xs cursor-pointer hover:border-primary/40 transition-all"
                    onClick={() => {
                      setActiveSkill(sp.skill);
                      setLocation(`/roadmap?skill=${encodeURIComponent(sp.skill)}`);
                    }}
                  >
                    <div>
                      <div className="font-medium flex items-center gap-1">
                        <span>{sp.skill}</span>
                        <ArrowRight className="h-3 w-3 text-primary" />
                      </div>
                      <div className="text-muted-foreground">
                        {sp.requirement === "required" ? "Required" : "Preferred"} • {sp.resumeStatus === "matched" ? "In Resume" : "Gap"}
                      </div>
                    </div>
                    <Badge variant={sp.status === "Strong" ? "default" : sp.status === "Developing" ? "secondary" : "outline"}>
                      {sp.latestAssessmentScore !== null ? `${sp.latestAssessmentScore}%` : "Click for Roadmap"}
                    </Badge>
                  </div>
                ))}
              </div>

              <Button className="mt-5 w-full gap-2" onClick={() => setLocation("/analytics")}>
                View Skill Analytics & Trends <ArrowRight className="h-4 w-4" />
              </Button>
            </Card>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
