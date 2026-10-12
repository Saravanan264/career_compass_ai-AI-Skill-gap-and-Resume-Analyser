import { useMemo } from "react";
import { useLocation } from "wouter";
import { ArrowRight, Info, Rocket, Star, Sparkles } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { useJobStore } from "@/state/job-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { recommendProjects } from "@/lib/project-recommender";
import { matchResumeToJd } from "@/lib/skill-matcher";
import { analyzeJobRole } from "@/lib/jd-analyzer";

export default function Projects() {
  const [, setLocation] = useLocation();
  const { analysis } = useResumeStore();
  const { matchResult, jdAnalysis, selectedRoleId, selectedRoleTitle } = useJobStore();

  const activeMatchResult = useMemo(() => {
    if (analysis?.skillsDetected?.length && jdAnalysis) {
      return matchResumeToJd(analysis.skillsDetected, jdAnalysis);
    }
    if (analysis?.skillsDetected?.length && selectedRoleId) {
      const roleJd = analyzeJobRole(selectedRoleId);
      if (roleJd) return matchResumeToJd(analysis.skillsDetected, roleJd);
    }
    return matchResult;
  }, [analysis, jdAnalysis, matchResult, selectedRoleId]);

  const projects = useMemo(() => {
    if (!activeMatchResult) return [];
    return recommendProjects(
      activeMatchResult.missingRequiredSkills ?? activeMatchResult.missingSkills ?? [],
      activeMatchResult.missingPreferredSkills ?? [],
      activeMatchResult.improvementAreas ?? [],
      6
    );
  }, [activeMatchResult]);

  if (!analysis) {
    return (
      <AppShell current="projects">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">No resume analyzed yet</div>
              <div className="text-sm text-muted-foreground">Upload and analyze your resume first to view recommended projects.</div>
              <Button className="mt-4" onClick={() => setLocation("/upload")}>Go to Upload</Button>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }

  const totalMissingGaps = (activeMatchResult?.missingRequiredSkills?.length || 0) +
                           (activeMatchResult?.missingPreferredSkills?.length || 0) +
                           (activeMatchResult?.missingSkills?.length || 0);

  const hasJdSelected = Boolean(jdAnalysis || selectedRoleId || matchResult);
  const isZeroMissingGaps = Boolean(activeMatchResult && totalMissingGaps === 0 && hasJdSelected);

  const difficultyColor: Record<string, string> = {
    Beginner: "bg-emerald-500/10 text-emerald-600",
    Intermediate: "bg-amber-500/10 text-amber-600",
    Advanced: "bg-rose-500/10 text-rose-600",
  };

  return (
    <AppShell current="projects">
      <div className="ai-fade-in space-y-6">
        <div>
          <div className="flex flex-wrap items-center gap-2 mb-2">
            <Badge variant="secondary" className="gap-1"><Rocket className="h-3.5 w-3.5" />Recommended Projects</Badge>
            {selectedRoleTitle && <Badge variant="secondary" className="gap-1"><Sparkles className="h-3.5 w-3.5" />{selectedRoleTitle}</Badge>}
          </div>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Projects to Close Your Skill Gaps</h2>
          <p className="text-muted-foreground max-w-2xl mt-1">Each project is recommended based on your missing skills. Build these to cover multiple gaps at once.</p>
        </div>

        {projects.length === 0 ? (
          <Card className="ai-card p-6 text-center space-y-3">
            {!hasJdSelected ? (
              <>
                <Info className="h-8 w-8 text-primary mx-auto" />
                <div className="font-medium text-lg">No Target Job Description Selected</div>
                <p className="text-sm text-muted-foreground max-w-md mx-auto">
                  Select a target job role or paste a job description to calculate your skill gaps and get tailored project recommendations.
                </p>
                <Button className="mt-2 gap-2" onClick={() => setLocation("/job-analysis")}>
                  Select Job Description <ArrowRight className="h-4 w-4" />
                </Button>
              </>
            ) : isZeroMissingGaps ? (
              <>
                <Star className="h-8 w-8 text-emerald-500 mx-auto" />
                <div className="font-medium text-lg">Outstanding Coverage!</div>
                <p className="text-sm text-muted-foreground max-w-md mx-auto">
                  Your resume covers all required skills for this target role! No additional skill gap projects required.
                </p>
                <div className="pt-2 flex justify-center gap-3">
                  <Button variant="secondary" onClick={() => setLocation("/job-roles")}>View Other Job Roles</Button>
                  <Button onClick={() => setLocation("/assessment")}>Take Assessment</Button>
                </div>
              </>
            ) : (
              <>
                <Info className="h-8 w-8 text-amber-500 mx-auto" />
                <div className="font-medium text-lg">Skill Gap Recommendations</div>
                <p className="text-sm text-muted-foreground max-w-md mx-auto">
                  Calculating project recommendations for your skill gaps...
                </p>
                <Button className="mt-2 gap-2" onClick={() => setLocation("/skills")}>
                  View Skill Gaps <ArrowRight className="h-4 w-4" />
                </Button>
              </>
            )}
          </Card>
        ) : (
          <div className="grid gap-4 lg:grid-cols-2">
            {projects.map((project, idx) => (
              <Card key={project.id} className="ai-card p-5">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <div className="h-8 w-8 rounded-lg bg-primary/10 text-primary grid place-items-center text-sm font-semibold">{idx + 1}</div>
                    <div>
                      <div className="font-medium">{project.title}</div>
                      <div className="flex items-center gap-2 mt-1">
                        <span className={`text-xs px-2 py-0.5 rounded-full ${difficultyColor[project.difficulty] ?? ""}`}>{project.difficulty}</span>
                        <span className="text-xs text-muted-foreground">~{project.estimatedHours}h</span>
                      </div>
                    </div>
                  </div>
                  <Badge variant="secondary" className="shrink-0">{project.coverageScore}% coverage</Badge>
                </div>
                <p className="mt-3 text-sm text-muted-foreground">{project.description}</p>
                <div className="mt-3">
                  <div className="text-xs text-muted-foreground mb-1.5">Skills covered:</div>
                  <div className="flex flex-wrap gap-1.5">
                    {project.skillsCovered.map((s) => (
                      <Badge key={s} variant={project.gapSkillsCovered.includes(s) ? "default" : "secondary"} className="text-xs">{s}</Badge>
                    ))}
                  </div>
                </div>
                <div className="mt-3 rounded-lg bg-muted/50 p-3">
                  <div className="text-xs font-medium text-primary">Why this project?</div>
                  <div className="text-xs text-muted-foreground mt-1">{project.reason}</div>
                </div>
                <div className="mt-3">
                  <div className="text-xs text-muted-foreground mb-1">Gap coverage</div>
                  <Progress value={project.coverageScore} />
                </div>
              </Card>
            ))}
          </div>
        )}

        <div className="flex gap-3">
          <Button variant="secondary" onClick={() => setLocation("/job-roles")} className="gap-2">View Job Roles <ArrowRight className="h-4 w-4" /></Button>
          <Button onClick={() => setLocation("/assessment")} className="gap-2">Start Assessment <ArrowRight className="h-4 w-4" /></Button>
        </div>
      </div>
    </AppShell>
  );
}
