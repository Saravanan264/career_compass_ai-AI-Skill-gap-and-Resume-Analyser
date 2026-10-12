import { useMemo, useRef, useState } from "react";
import { useLocation } from "wouter";
import { Upload, FileText, Sparkles, ArrowRight, ShieldCheck } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { toast } from "@/hooks/use-toast";

import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { extractTextFromPdf } from "@/lib/pdf";
import { analyzeResumeText } from "@/lib/analyzer";
import { uploadResumeApi } from "@/lib/api";

export default function ResumeUpload() {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [, setLocation] = useLocation();

  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(0);

  const {
    resumeFileName,
    resumeText,
    analysis,
    setResume,
    clearAll,
  } = useResumeStore();

  const hasData = useMemo(() => Boolean(resumeText && analysis), [resumeText, analysis]);

  async function handleFile(file: File) {
    if (!file) return;

    if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
      toast({
        title: "Please upload a PDF",
        description: "This prototype supports PDF resumes for the demo.",
        variant: "destructive",
      });
      return;
    }

    setBusy(true);
    setProgress(15);
    clearAll(); // Clear previous store state for fresh upload

    try {
      // Try backend upload first
      try {
        setProgress(40);
        const backendRes = await uploadResumeApi(file);
        if (backendRes && backendRes.analysis) {
          if (backendRes.analysis.isValidResume === false) {
            clearAll();
            toast({
              title: "Invalid Resume Document",
              description: backendRes.analysis.validationReason || "This document does not appear to be a valid resume. Please upload a resume containing candidate details, skills, education, experience, projects, or other resume sections.",
              variant: "destructive",
            });
            setBusy(false);
            setProgress(0);
            return;
          }
          setProgress(100);
          setResume({
            resumeFileName: file.name,
            resumeText: backendRes.analysis.parsed_text || "",
            analysis: backendRes.analysis,
          });
          toast({
            title: "Resume uploaded & analyzed",
            description: "Your ATS dashboard is ready with backend persistence.",
          });
          setTimeout(() => {
            setLocation("/ats");
          }, 250);
          return;
        }
      } catch (backendError: any) {
        console.warn("Backend upload failed or returned error:", backendError);
        const errMsg = backendError?.message || String(backendError);
        if (errMsg.includes("does not appear to be a valid resume") || errMsg.includes("400")) {
          clearAll();
          toast({
            title: "Invalid Resume Document",
            description: "This document does not appear to be a valid resume. Please upload a resume containing candidate details, skills, education, experience, projects, or other resume sections.",
            variant: "destructive",
          });
          setBusy(false);
          setProgress(0);
          return;
        }
      }

      // Local fallback
      setProgress(50);
      const text = await extractTextFromPdf(file, (p) => setProgress(50 + Math.round(p * 0.4)));

      if (!text.trim()) {
        toast({
          title: "Couldn’t read the PDF",
          description:
            "Try a different resume PDF (some scans don’t contain selectable text).",
          variant: "destructive",
        });
        setBusy(false);
        setProgress(0);
        return;
      }

      setProgress(90);
      const analyzed = await analyzeResumeText(text);

      if (analyzed.isValidResume === false) {
        clearAll();
        toast({
          title: "Invalid Resume Document",
          description: analyzed.validationReason || "This document does not appear to be a valid resume. Please upload a resume containing candidate details, skills, education, experience, projects, or other resume sections.",
          variant: "destructive",
        });
        setBusy(false);
        setProgress(0);
        return;
      }

      setResume({
        resumeFileName: file.name,
        resumeText: text,
        analysis: analyzed,
      });

      setProgress(100);
      toast({
        title: "Resume analyzed",
        description: "Your ATS dashboard is ready.",
      });

      setTimeout(() => {
        setLocation("/ats");
      }, 250);
    } catch (e) {
      toast({
        title: "Upload failed",
        description: e instanceof Error ? e.message : "Something went wrong.",
        variant: "destructive",
      });
      setProgress(0);
    } finally {
      setBusy(false);
    }
  }



  async function onPick() {
    inputRef.current?.click();
  }

  return (
    <AppShell current="upload">
      <div className="ai-fade-in space-y-6">
        <div className="flex flex-col gap-3">
          <div className="flex items-center gap-2">
            <Badge data-testid="status-demo" variant="secondary" className="gap-1">
              <Sparkles className="h-3.5 w-3.5" />
              Demo-ready prototype
            </Badge>
            <Badge data-testid="status-private" variant="secondary" className="gap-1">
              <ShieldCheck className="h-3.5 w-3.5" />
              Local analysis (mock)
            </Badge>
          </div>

          <h1 className="ai-title text-3xl md:text-4xl font-semibold">
            Career Compass AI
          </h1>
          <p className="text-muted-foreground max-w-2xl">
            Upload your resume to begin your career assessment. We analyse your skills,
            compare against job requirements, and guide you with a personalized roadmap.
          </p>
        </div>

        <Card className="ai-card ai-glass p-5 md:p-7">
          <div className="grid gap-5 md:grid-cols-[1.3fr_0.7fr]">
            <div className="space-y-4">
              <div className="rounded-xl border border-dashed border-border/80 bg-background/40 p-6 md:p-7">
                <div className="flex flex-col items-start gap-3">
                  <div className="flex items-center gap-3">
                    <div className="grid place-items-center rounded-xl bg-primary/10 text-primary h-11 w-11">
                      <Upload className="h-5 w-5" />
                    </div>
                    <div>
                      <div className="font-medium" data-testid="text-upload-title">
                        Upload resume PDF
                      </div>
                      <div
                        className="text-sm text-muted-foreground"
                        data-testid="text-upload-subtitle"
                      >
                        We extract text client-side for this mockup.
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center gap-2">
                    <Button
                      data-testid="button-pick-file"
                      onClick={onPick}
                      disabled={busy}
                      className="gap-2"
                    >
                      <FileText className="h-4 w-4" />
                      Choose PDF
                    </Button>

                    <Button
                      data-testid="button-use-sample"
                      variant="secondary"
                      disabled={busy}
                      className="gap-2"
                      onClick={async () => {
                        setBusy(true);
                        setProgress(10);
                        try {
                          const res = await fetch("/sample-resume.txt");
                          const text = await res.text();
                          setProgress(70);
                          const analyzed = await analyzeResumeText(text);
                          setResume({
                            resumeFileName: "Sample Resume (text)",
                            resumeText: text,
                            analysis: analyzed,
                          });
                          setProgress(100);
                          toast({
                            title: "Sample loaded",
                            description: "Jumping to your ATS dashboard.",
                          });
                          setTimeout(() => setLocation("/ats"), 200);
                        } catch (e) {
                          toast({
                            title: "Couldn’t load sample",
                            description:
                              e instanceof Error ? e.message : "Something went wrong.",
                            variant: "destructive",
                          });
                          setProgress(0);
                        } finally {
                          setBusy(false);
                        }
                      }}
                    >
                      <Sparkles className="h-4 w-4" />
                      Use sample
                    </Button>

                    {hasData ? (
                      <Button
                        data-testid="button-continue"
                        variant="outline"
                        className="gap-2"
                        onClick={() => setLocation("/ats")}
                      >
                        Continue
                        <ArrowRight className="h-4 w-4" />
                      </Button>
                    ) : null}

                    <Button
                      data-testid="button-reset"
                      variant="ghost"
                      disabled={busy && progress > 0}
                      onClick={() => {
                        clearAll();
                        setProgress(0);
                        toast({
                          title: "Cleared",
                          description: "You can upload a new resume now.",
                        });
                      }}
                    >
                      Reset
                    </Button>
                  </div>

                  <input
                    ref={inputRef}
                    data-testid="input-resume-file"
                    type="file"
                    accept="application/pdf"
                    className="hidden"
                    onChange={(e) => {
                      const f = e.target.files?.[0];
                      if (f) void handleFile(f);
                    }}
                  />

                  {busy || progress > 0 ? (
                    <div className="pt-2 space-y-2" data-testid="status-upload-progress">
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <span>Analyzing…</span>
                        <span data-testid="text-upload-percent">{progress}%</span>
                      </div>
                      <Progress value={progress} />
                    </div>
                  ) : null}

                  {resumeFileName ? (
                    <div
                      className="mt-2 text-sm text-muted-foreground"
                      data-testid="text-file-name"
                    >
                      Current: <span className="text-foreground">{resumeFileName}</span>
                    </div>
                  ) : null}
                </div>
              </div>

              <div className="grid gap-3 md:grid-cols-3">
                <Card className="ai-card p-4">
                  <div className="text-sm font-medium" data-testid="text-step-1">
                    1) ATS Score
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Weighted sections + keyword coverage.
                  </div>
                </Card>
                <Card className="ai-card p-4">
                  <div className="text-sm font-medium" data-testid="text-step-2">
                    2) Skill Gaps
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Compare to target domains.
                  </div>
                </Card>
                <Card className="ai-card p-4">
                  <div className="text-sm font-medium" data-testid="text-step-3">
                    3) Roadmap
                  </div>
                  <div className="text-sm text-muted-foreground">
                    Courses + projects in a vertical plan.
                  </div>
                </Card>
              </div>
            </div>

            <div className="space-y-4">
              <Card className="ai-card p-5">
                <div className="text-sm font-medium" data-testid="text-tip-title">
                  Demo tips
                </div>
                <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                  <li data-testid="text-tip-1">
                    • Use the sample to demo the full 5-page flow quickly.
                  </li>
                  <li data-testid="text-tip-2">
                    • Upload a PDF with selectable text (not a scanned image).
                  </li>
                  <li data-testid="text-tip-3">
                    • The scoring is rule-based for transparency.
                  </li>
                </ul>
              </Card>

              <Card className="ai-card p-5">
                <div className="text-sm font-medium" data-testid="text-output-title">
                  What you’ll get
                </div>
                <div className="mt-3 grid gap-2 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground">Final scorecard</span>
                    <span className="font-medium" data-testid="text-output-scorecard">
                      Yes
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground">Best-fit domain</span>
                    <span className="font-medium" data-testid="text-output-domain">
                      Yes
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground">Learning roadmap</span>
                    <span className="font-medium" data-testid="text-output-roadmap">
                      Yes
                    </span>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </Card>
      </div>
    </AppShell>
  );
}
