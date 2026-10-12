import { useEffect, useState } from "react";
import { useLocation } from "wouter";
import { ArrowRight, BriefcaseBusiness, CheckCircle2, ClipboardPaste, Info, Layers, Sparkles } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { useJobStore } from "@/state/job-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "@/hooks/use-toast";
import { analyzeJdText, analyzeJobRole } from "@/lib/jd-analyzer";
import { matchResumeToJd } from "@/lib/skill-matcher";
import { createJobDescriptionApi, getUserJobDescriptionsApi } from "@/lib/api";
import jobRolesDb from "@/data/job-roles.json";

export default function JobAnalysis() {
  const [, setLocation] = useLocation();
  const { analysis } = useResumeStore();
  const { jdText, selectedRoleId, setJdText, setSelectedRole, setJdAnalysis, setMatchResult, jdAnalysis, selectJobRole } = useJobStore();
  const [mode, setMode] = useState<string>(selectedRoleId ? "role" : "paste");
  const [pastedText, setPastedText] = useState(jdText);
  const [localRoleId, setLocalRoleId] = useState(selectedRoleId ?? "");
  const [busy, setBusy] = useState(false);
  const roles = (jobRolesDb as any).roles as Array<{ id: string; title: string; description: string }>;

  useEffect(() => {
    if (!jdAnalysis) {
      getUserJobDescriptionsApi()
        .then((jds) => {
          if (jds && jds.length > 0) {
            const latest = jds[0];
            if (latest.analysis) {
              const adaptedAnalysis = {
                rawText: latest.description,
                requiredSkills: latest.analysis.requiredSkills,
                preferredSkills: latest.analysis.preferredSkills,
                allSkills: latest.analysis.allSkills,
                importance: latest.analysis.importance,
              };
              setJdText(latest.description);
              setJdAnalysis(adaptedAnalysis);
              if (analysis) {
                const match = matchResumeToJd(analysis.skillsDetected, adaptedAnalysis);
                setMatchResult(match);
              }
            }
          }
        })
        .catch(() => {});
    }
  }, [jdAnalysis, analysis, setJdAnalysis, setJdText, setMatchResult]);

  if (!analysis) {
    return (
      <AppShell current="job-analysis">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">No resume analyzed yet</div>
              <div className="text-sm text-muted-foreground">Upload and analyze your resume first.</div>
              <Button className="mt-4" onClick={() => setLocation("/upload")}>Go to Upload</Button>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }

  async function handleAnalyze() {
    if (!analysis) return;
    setBusy(true);
    try {
      if (mode === "role") {
        if (!localRoleId) {
          toast({ title: "No role selected", variant: "destructive" });
          setBusy(false);
          return;
        }
        const roleObj = roles.find((r) => r.id === localRoleId);
        const roleTitle = roleObj?.title ?? localRoleId;
        const roleJd = analyzeJobRole(localRoleId);
        if (!roleJd) {
          toast({ title: "Invalid role selected", variant: "destructive" });
          setBusy(false);
          return;
        }
        const match = analysis.skillsDetected ? matchResumeToJd(analysis.skillsDetected, roleJd) : null;
        selectJobRole(localRoleId, roleTitle, roleJd, match);
        toast({
          title: "Job analysis complete",
          description: match ? `Match: ${match.jobMatchScore}% — ${match.matchingSkills.length} matched, ${match.missingSkills.length} missing.` : undefined,
        });
        setLocation("/skills");
        return;
      }

      if (!pastedText.trim()) {
        toast({ title: "Empty JD", variant: "destructive" });
        setBusy(false);
        return;
      }

      let jdResult;
      try {
        const backendRes = await createJobDescriptionApi({
          title: "Custom Job Description",
          description: pastedText,
        });

        if (backendRes && backendRes.analysis) {
          jdResult = {
            rawText: backendRes.description,
            requiredSkills: backendRes.analysis.requiredSkills,
            preferredSkills: backendRes.analysis.preferredSkills,
            allSkills: backendRes.analysis.allSkills,
            importance: backendRes.analysis.importance,
          };
        }
      } catch (backendErr) {
        console.warn("Backend JD submission failed, falling back to local analysis:", backendErr);
      }

      if (!jdResult) {
        jdResult = analyzeJdText(pastedText);
      }

      const match = matchResumeToJd(analysis.skillsDetected, jdResult);
      selectJobRole("custom", "Custom Job Description", jdResult, match);
      toast({
        title: "Job analysis complete",
        description: `Match: ${match.jobMatchScore}% — ${match.matchingSkills.length} matched, ${match.missingSkills.length} missing.`,
      });
      setLocation("/skills");
    } catch (e) {
      toast({ title: "Analysis failed", description: e instanceof Error ? e.message : "Error", variant: "destructive" });
    } finally {
      setBusy(false);
    }
  }


  return (
    <AppShell current="job-analysis">
      <div className="ai-fade-in space-y-6">
        <div>
          <div className="flex flex-wrap items-center gap-2 mb-2">
            <Badge variant="secondary" className="gap-1"><BriefcaseBusiness className="h-3.5 w-3.5" />Job Analysis</Badge>
            <Badge variant="secondary" className="gap-1"><Sparkles className="h-3.5 w-3.5" />{analysis.skillsDetected.length} skills detected</Badge>
          </div>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Target Job Description</h2>
          <p className="text-muted-foreground max-w-2xl mt-1">Select a job role or paste a job description to compare against your resume.</p>
        </div>

        <Tabs value={mode} onValueChange={setMode}>
          <TabsList>
            <TabsTrigger value="role" className="gap-2"><Layers className="h-4 w-4" />Select Role</TabsTrigger>
            <TabsTrigger value="paste" className="gap-2"><ClipboardPaste className="h-4 w-4" />Paste JD</TabsTrigger>
          </TabsList>
          <TabsContent value="role" className="mt-4">
            <Card className="ai-card p-5">
              <div className="font-medium">Choose a target job role</div>
              <div className="text-sm text-muted-foreground mt-1">Select from predefined roles with defined skill requirements.</div>
              <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {roles.map((role) => (
                  <Card key={role.id} className={`ai-card p-4 cursor-pointer transition-all hover:shadow-md hover:-translate-y-0.5 ${localRoleId === role.id ? "ring-2 ring-primary bg-primary/5" : ""}`} onClick={() => setLocalRoleId(role.id)}>
                    <div className="flex items-start gap-2">
                      {localRoleId === role.id && <CheckCircle2 className="h-4 w-4 text-primary mt-0.5 shrink-0" />}
                      <div>
                        <div className="text-sm font-medium">{role.title}</div>
                        <div className="mt-1 text-xs text-muted-foreground line-clamp-2">{role.description}</div>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </Card>
          </TabsContent>
          <TabsContent value="paste" className="mt-4">
            <Card className="ai-card p-5">
              <div className="font-medium">Paste Job Description</div>
              <div className="text-sm text-muted-foreground mt-1">Copy and paste the full job description text below.</div>
              <Textarea className="mt-4 min-h-[200px] font-mono text-sm" placeholder={"Paste the job description here...\n\nExample:\nWe are looking for a Backend Developer with experience in Java, Spring Boot, REST APIs, Docker, and AWS..."} value={pastedText} onChange={(e) => setPastedText(e.target.value)} />
            </Card>
          </TabsContent>
        </Tabs>

        <Button className="gap-2" size="lg" disabled={busy} onClick={handleAnalyze}>
          {busy ? "Analyzing..." : "Analyze & Compare"}<ArrowRight className="h-4 w-4" />
        </Button>
      </div>
    </AppShell>
  );
}
