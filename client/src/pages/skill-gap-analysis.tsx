import React, { useMemo, useState, useEffect, Component, ErrorInfo, ReactNode } from "react";
import { useLocation } from "wouter";
import { ArrowRight, BadgeCheck, Info, Target, Wand2, CheckCircle2, XCircle, AlertCircle, RefreshCw } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { useJobStore } from "@/state/job-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { matchResumeToJd } from "@/lib/skill-matcher";
import { analyzeJobRole } from "@/lib/jd-analyzer";
import jobRolesDb from "@/data/job-roles.json";

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class SkillGapErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Skill Gap Analysis Render Error:", error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <AppShell current="skills">
          <Card className="ai-card p-6 text-center space-y-4 max-w-lg mx-auto my-12">
            <AlertCircle className="h-10 w-10 text-rose-500 mx-auto" />
            <div>
              <div className="font-semibold text-lg">Unable to load skill gap analysis.</div>
              <p className="text-xs text-muted-foreground mt-1">
                An unexpected error occurred while analyzing your skill gaps. Please try again.
              </p>
            </div>
            <Button onClick={this.handleReset} className="gap-2">
              <RefreshCw className="h-4 w-4" /> Try Again
            </Button>
          </Card>
        </AppShell>
      );
    }
    return this.props.children;
  }
}

function SkillGapContent() {
  const [, setLocation] = useLocation();
  const { analysis } = useResumeStore();
  const { matchResult, selectedRoleId, selectedRoleTitle, jdAnalysis, setMatchResult, setJdAnalysis, setSelectedRole } = useJobStore();

  const initialDomain = useMemo(() => {
    if (analysis?.bestFitDomain && analysis?.domains && analysis.domains[analysis.bestFitDomain]) {
      return analysis.bestFitDomain;
    }
    if (analysis?.domains && Object.keys(analysis.domains).length > 0) {
      return Object.keys(analysis.domains)[0];
    }
    return "Data Science";
  }, [analysis]);

  const [domain, setDomain] = useState<string>(initialDomain);

  useEffect(() => {
    if (initialDomain && !domain) {
      setDomain(initialDomain);
    }
  }, [initialDomain, domain]);

  // Auto-resolve jdAnalysis if selectedRoleId is set
  useEffect(() => {
    if (selectedRoleId) {
      const roleJd = analyzeJobRole(selectedRoleId);
      if (roleJd) {
        // Only set if different or missing
        if (!jdAnalysis || jdAnalysis.rawText !== roleJd.rawText) {
          setJdAnalysis(roleJd);
        }
        if (!selectedRoleTitle) {
          const roleObj = (jobRolesDb as any)?.roles?.find((r: any) => r.id === selectedRoleId);
          setSelectedRole(selectedRoleId, roleObj?.title || selectedRoleId);
        }
      }
    }
  }, [selectedRoleId, selectedRoleTitle, setJdAnalysis, setSelectedRole]);


  // Recompute matchResult dynamically without infinite loop
  const activeMatchResult = useMemo(() => {
    if (analysis?.skillsDetected && Array.isArray(analysis.skillsDetected) && analysis.skillsDetected.length > 0 && jdAnalysis) {
      return matchResumeToJd(analysis.skillsDetected, jdAnalysis);
    }
    return matchResult || null;
  }, [analysis?.skillsDetected, jdAnalysis, matchResult]);

  // Safely sync matchResult to Zustand store ONLY if matching/missing content changes
  const activeKey = useMemo(() => {
    if (!activeMatchResult) return "";
    return `${(activeMatchResult.matchingSkills || []).join(",")}|${(activeMatchResult.missingSkills || []).join(",")}|${activeMatchResult.jobMatchScore ?? 0}`;
  }, [activeMatchResult]);

  const storeKey = useMemo(() => {
    if (!matchResult) return "";
    return `${(matchResult.matchingSkills || []).join(",")}|${(matchResult.missingSkills || []).join(",")}|${matchResult.jobMatchScore ?? 0}`;
  }, [matchResult]);

  useEffect(() => {
    if (activeMatchResult && activeKey && activeKey !== storeKey) {
      setMatchResult(activeMatchResult);
    }
  }, [activeMatchResult, activeKey, storeKey, setMatchResult]);

  // Handle empty / missing states gracefully
  if (!analysis) {
    return (
      <AppShell current="skills">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">Please upload a resume before viewing your skill gap.</div>
              <div className="text-sm text-muted-foreground mt-1">Upload and analyze your resume first to view detailed skill gap results.</div>
              <Button className="mt-4" onClick={() => setLocation("/upload")}>Go to Upload</Button>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }

  if (!analysis.skillsDetected || !Array.isArray(analysis.skillsDetected) || analysis.skillsDetected.length === 0) {
    return (
      <AppShell current="skills">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">Resume skills could not be detected.</div>
              <div className="text-sm text-muted-foreground mt-1">Please upload a resume with a readable Skills section.</div>
              <Button className="mt-4" onClick={() => setLocation("/upload")}>Go to Upload</Button>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }

  if (!jdAnalysis || !jdAnalysis.allSkills || jdAnalysis.allSkills.length === 0) {
    return (
      <AppShell current="skills">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">Please select a job role or provide a job description.</div>
              <div className="text-sm text-muted-foreground mt-1">Select a target job role or paste a job description to calculate your skill gaps.</div>
              <div className="flex flex-wrap gap-3 mt-4">
                <Button onClick={() => setLocation("/job-roles")}>Select Job Role</Button>
                <Button variant="secondary" onClick={() => setLocation("/job-analysis")}>Paste Job Description</Button>
              </div>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }


  const priorityColor: Record<string, string> = {
    high: "bg-rose-500/10 text-rose-600 border-rose-500/20",
    critical: "bg-rose-500/10 text-rose-600 border-rose-500/20",
    medium: "bg-amber-500/10 text-amber-600 border-amber-500/20",
    low: "bg-blue-500/10 text-blue-600 border-blue-500/20",
  };

  const getPriorityColor = (priority?: string) => {
    const key = (priority || "low").toLowerCase();
    return priorityColor[key] || "bg-slate-500/10 text-slate-600 border-slate-500/20";
  };

  const statusBadgeMap: Record<string, { label: string; variant: "default" | "secondary" | "outline" | "destructive" }> = {
    match: { label: "Match", variant: "default" },
    matched: { label: "Match", variant: "default" },
    missing: { label: "Missing", variant: "destructive" },
    "missing-required": { label: "Missing", variant: "destructive" },
    "missing_required": { label: "Missing", variant: "destructive" },
    "missing-preferred": { label: "Missing", variant: "outline" },
    "missing_preferred": { label: "Missing", variant: "outline" },
    improve: { label: "Improve", variant: "outline" },
    developing: { label: "Develop", variant: "outline" },
  };

  const getStatusBadge = (status?: string) => {
    const key = (status || "missing").toLowerCase();
    return statusBadgeMap[key] || { label: status || "Missing", variant: "outline" };
  };

  // Safe data arrays
  const matchingSkills = activeMatchResult?.matchingSkills ?? [];
  const missingSkills = activeMatchResult?.missingSkills ?? [];
  const improvementAreas = activeMatchResult?.improvementAreas ?? [];
  const skillGaps = activeMatchResult?.skillGaps ?? [];
  const jobMatchScore = activeMatchResult?.jobMatchScore ?? 0;
  const semanticSimilarityScore = activeMatchResult?.semanticSimilarityScore ?? jobMatchScore;
  const hybridMatchScore = activeMatchResult?.hybridMatchScore ?? jobMatchScore;
  const skillCoverage = activeMatchResult?.skillCoverage ?? 0;

  return (
    <AppShell current="skills">
      <div className="ai-fade-in space-y-6">
        <div>
          <div className="flex flex-wrap items-center gap-2 mb-2">
            <Badge variant="secondary" className="gap-1"><Target className="h-3.5 w-3.5" />Skill Gap Analysis</Badge>
            <Badge variant="secondary" className="gap-1"><Wand2 className="h-3.5 w-3.5" />{(analysis.skillsDetected || []).length} skills detected</Badge>
            {selectedRoleTitle && <Badge variant="secondary" className="gap-1"><BadgeCheck className="h-3.5 w-3.5" />{selectedRoleTitle}</Badge>}
          </div>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Resume vs Job Requirements</h2>
          <p className="text-muted-foreground max-w-2xl mt-1">Skills compared against your target job description with prioritized gaps.</p>
        </div>

        {/* Scores Cards */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Card className="ai-card p-5">
            <div className="text-sm text-muted-foreground">Rule-Based Match</div>
            <div className="ai-title text-3xl font-semibold mt-1">{jobMatchScore}%</div>
            <Progress value={jobMatchScore} className="mt-3" />
          </Card>
          <Card className="ai-card p-5">
            <div className="text-sm text-muted-foreground">Semantic Similarity</div>
            <div className="ai-title text-3xl font-semibold mt-1">{semanticSimilarityScore}%</div>
            <Progress value={semanticSimilarityScore} className="mt-3" />
          </Card>
          <Card className="ai-card p-5">
            <div className="text-sm text-muted-foreground">Hybrid Compatibility</div>
            <div className="ai-title text-3xl font-semibold mt-1">{hybridMatchScore}%</div>
            <Progress value={hybridMatchScore} className="mt-3" />
          </Card>
          <Card className="ai-card p-5">
            <div className="text-sm text-muted-foreground">Skill Coverage</div>
            <div className="ai-title text-3xl font-semibold mt-1">{skillCoverage}%</div>
            <Progress value={skillCoverage} className="mt-3" />
          </Card>
        </div>

        {/* Matching / Missing / Improvement Column Cards */}
        <div className="grid gap-4 lg:grid-cols-3">
          <Card className="ai-card p-5">
            <div className="text-sm font-medium text-emerald-600 mb-3 flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4" /> Matching Skills ({matchingSkills.length})
            </div>
            {matchingSkills.length === 0 ? (
              <div className="text-xs text-muted-foreground">No direct matching skills detected.</div>
            ) : (
              <div className="flex flex-wrap gap-1.5">
                {matchingSkills.map((s) => <Badge key={s} className="text-xs bg-emerald-500/10 text-emerald-700 border-emerald-500/20">✓ {s}</Badge>)}
              </div>
            )}
          </Card>

          <Card className="ai-card p-5">
            <div className="text-sm font-medium text-rose-600 mb-3 flex items-center gap-1.5">
              <XCircle className="h-4 w-4" /> Missing Skills ({missingSkills.length})
            </div>
            {missingSkills.length === 0 ? (
              <div className="text-xs text-muted-foreground">All required role skills matched!</div>
            ) : (
              <div className="flex flex-wrap gap-1.5">
                {missingSkills.map((s) => <Badge key={s} variant="outline" className="text-xs border-rose-500/30 text-rose-600">✕ {s}</Badge>)}
              </div>
            )}
          </Card>

          <Card className="ai-card p-5">
            <div className="text-sm font-medium text-amber-600 mb-3 flex items-center gap-1.5">
              <Info className="h-4 w-4" /> Improvement Areas ({improvementAreas.length})
            </div>
            {improvementAreas.length === 0 ? (
              <div className="text-xs text-muted-foreground">No additional improvement areas identified.</div>
            ) : (
              <div className="flex flex-wrap gap-1.5">
                {improvementAreas.map((s) => <Badge key={s} variant="outline" className="text-xs border-amber-500/30 text-amber-600">{s}</Badge>)}
              </div>
            )}
          </Card>
        </div>

        {/* Skill Gap Prioritization Table */}
        <Card className="ai-card p-5">
          <div className="font-medium mb-4">Skill Gap Prioritization</div>
          {skillGaps.length === 0 ? (
            <div className="text-xs text-muted-foreground text-center py-4">No skill gaps prioritized.</div>
          ) : (
            <div className="space-y-2">
              {skillGaps.map((gap) => {
                const badge = getStatusBadge(gap.status);
                const color = getPriorityColor(gap.priority);
                return (
                  <div
                    key={gap.skill}
                    className="flex items-center justify-between gap-3 rounded-xl border p-3 cursor-pointer hover:border-primary/50 hover:bg-primary/5 transition-all"
                    onClick={() => setLocation(`/roadmap?skill=${encodeURIComponent(gap.skill)}`)}
                  >
                    <div className="flex items-center gap-3">
                      <Badge variant={badge.variant} className="text-xs w-16 justify-center">{badge.label}</Badge>
                      <span className="text-sm font-medium">{gap.skill}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-muted-foreground">Importance: {gap.importance ?? 5}/10</span>
                      {gap.status !== "match" && (
                        <span className={`text-xs px-2 py-0.5 rounded-full border ${color}`}>{(gap.priority || "low").toUpperCase()}</span>
                      )}
                      <span className="text-xs text-primary font-medium ml-1">View Roadmap →</span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </Card>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <Button onClick={() => setLocation("/projects")} className="gap-2">Recommended Projects <ArrowRight className="h-4 w-4" /></Button>
          <Button variant="secondary" onClick={() => setLocation("/job-roles")} className="gap-2">Job Roles <ArrowRight className="h-4 w-4" /></Button>
        </div>
      </div>
    </AppShell>
  );
}

export default function SkillGapAnalysis() {
  return (
    <SkillGapErrorBoundary>
      <SkillGapContent />
    </SkillGapErrorBoundary>
  );
}
