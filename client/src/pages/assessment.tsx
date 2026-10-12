import { useMemo, useState, useEffect } from "react";
import { useLocation } from "wouter";
import { ArrowRight, CheckCircle2, ClipboardCheck, Info } from "lucide-react";
import { AppShell } from "@/components/app-shell";
import { useResumeStore } from "@/state/resume-store";
import { useJobStore } from "@/state/job-store";
import { useAssessmentStore } from "@/state/assessment-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { selectQuestions, evaluateAssessment } from "@/lib/assessment-engine";
import type { AssessmentQuestion } from "@/lib/assessment-engine";
import { toast } from "@/hooks/use-toast";
import questionsDb from "@/data/questions.json";
import { createAssessmentAttemptApi, getUserAssessmentAttemptsApi } from "@/lib/api";

export default function Assessment() {
  const [, setLocation] = useLocation();
  const { analysis } = useResumeStore();
  const { matchResult, selectedRoleId, selectedRoleTitle } = useJobStore();
  const store = useAssessmentStore();

  const [phase, setPhase] = useState<"setup" | "test" | "result">(
    store.currentQuestionIds.length > 0 ? "test" : "setup"
  );
  const [currentIdx, setCurrentIdx] = useState(0);

  const targetSkills = useMemo(() => {
    const skills = new Set<string>();
    if (matchResult) {
      matchResult.matchingSkills.forEach((s) => skills.add(s));
      matchResult.missingSkills.forEach((s) => skills.add(s));
      matchResult.improvementAreas.forEach((s) => skills.add(s));
    } else if (analysis) {
      analysis.skillsDetected.forEach((s) => skills.add(s));
    }
    return Array.from(skills);
  }, [analysis, matchResult]);

  const missingSkills = matchResult?.missingSkills ?? [];

  const questions: AssessmentQuestion[] = useMemo(() => {
    if (store.currentQuestionIds.length === 0) return [];
    const allQ = (questionsDb as any).questions as AssessmentQuestion[];
    return store.currentQuestionIds
      .map((id) => allQ.find((q) => q.id === id))
      .filter(Boolean) as AssessmentQuestion[];
  }, [store.currentQuestionIds]);

  useEffect(() => {
    getUserAssessmentAttemptsApi()
      .then((attempts) => {
        if (Array.isArray(attempts) && attempts.length > 0) {
          const adaptedAttempts = attempts.map((a: any) => ({
            id: String(a.id),
            date: a.created_at ? new Date(a.created_at).toISOString() : new Date().toISOString(),
            roleId: a.role_id || "general",
            roleTitle: a.role_title || "General",
            overallScore: a.overall_score || 0,
            totalQuestions: a.question_count || 15,
            correctAnswers: Math.round(((a.overall_score || 0) / 100) * (a.question_count || 15)),
            skillScores: Object.entries(a.skill_breakdown || {}).map(([skill, score]: [string, any]) => ({
              skill,
              score: Number(score),
              total: 1,
              correct: Number(score) >= 75 ? 1 : 0
            })),
            answers: {},
            timeTakenSeconds: a.time_taken_seconds || 0,
          }));
          store.setAttempts(adaptedAttempts);
        }
      })
      .catch(() => {});
  }, []);

  function startAssessment() {
    const prevScore = store.attempts.slice(-1)[0]?.overallScore;
    const selected = selectQuestions(
      targetSkills,
      matchResult?.missingRequiredSkills ?? matchResult?.missingSkills ?? [],
      matchResult?.missingPreferredSkills ?? [],
      analysis?.skillsDetected ?? [],
      prevScore,
      30
    );
    if (selected.length === 0) {
      toast({ title: "No questions available", variant: "destructive" });
      return;
    }
    store.setCurrentQuestionIds(selected.map((q) => q.id));
    store.setAssessmentStartTime(Date.now());
    store.setCurrentAnswers({});
    setPhase("test");
    setCurrentIdx(0);
  }

  async function handleSubmit() {
    const reqList = matchResult?.missingRequiredSkills ?? [];
    const timeTaken = Math.round((Date.now() - (store.assessmentStartTime || Date.now())) / 1000);
    const result = evaluateAssessment(
      questions,
      store.currentAnswers,
      selectedRoleId ?? "general",
      selectedRoleTitle ?? "General",
      timeTaken,
      reqList
    );
    store.addAttempt(result);
    store.clearCurrent();

    try {
      await createAssessmentAttemptApi({
        role_id: selectedRoleId ?? "general",
        role_title: selectedRoleTitle ?? "General",
        overall_score: result.overallScore,
        time_taken_seconds: result.timeTakenSeconds,
        question_count: result.totalQuestions,
        skill_breakdown: result.skillScores.reduce((acc, s) => ({ ...acc, [s.skill]: s.score }), {}),
      });
    } catch (e) {
      console.warn("Failed to persist assessment attempt to backend:", e);
    }

    setPhase("result");
    toast({ title: "Assessment complete!", description: `Score: ${result.overallScore}%` });
  }

  if (!analysis) {
    return (
      <AppShell current="assessment">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">No resume analyzed yet</div>
              <div className="text-sm text-muted-foreground">
                Upload a resume and add a job description first.
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

  if (phase === "setup") {
    return (
      <AppShell current="assessment">
        <div className="ai-fade-in space-y-6">
          <div>
            <Badge variant="secondary" className="gap-1 mb-2">
              <ClipboardCheck className="h-3.5 w-3.5" />
              Mock Assessment
            </Badge>
            <h2 className="ai-title text-2xl md:text-3xl font-semibold">
              Role & Skill-Specific Assessment
            </h2>
            <p className="text-muted-foreground max-w-2xl mt-1">
              30 questions selected based on your detected resume skills and target job requirements.
            </p>
          </div>
          <Card className="ai-card p-5">
            <div className="font-medium">Assessment Details</div>
            <div className="mt-3 grid gap-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Target Role</span>
                <span className="font-medium">
                  {selectedRoleTitle ?? "General"}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Questions</span>
                <span className="font-medium text-emerald-600 font-semibold">Exactly 30 MCQs</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Time Limit</span>
                <span className="font-medium text-emerald-600 font-semibold">No Timer — Untimed</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Detected Resume Skills</span>
                <span className="font-medium">
                  {(analysis?.skillsDetected ?? targetSkills).slice(0, 5).join(", ")}
                  {(analysis?.skillsDetected ?? targetSkills).length > 5 ? "..." : ""}
                </span>
              </div>
            </div>
            <Button
              className="mt-5 w-full gap-2"
              size="lg"
              onClick={startAssessment}
            >
              Start 30-Question Assessment <ArrowRight className="h-4 w-4" />
            </Button>
          </Card>

          {store.attempts.length > 0 && (
            <Card className="ai-card p-5">
              <div className="font-medium">Previous Attempts</div>
              <div className="mt-3 space-y-2">
                {store.attempts.slice(-5).reverse().map((a) => (
                  <div
                    key={a.id}
                    className="flex items-center justify-between rounded-xl border p-3 text-sm"
                  >
                    <div>
                      <span className="font-medium">{a.roleTitle}</span>
                      <span className="text-muted-foreground ml-2">
                        {new Date(a.date).toLocaleDateString()}
                      </span>
                    </div>
                    <Badge variant="secondary">{a.overallScore}%</Badge>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      </AppShell>
    );
  }

  if (phase === "result") {
    return (
      <AppShell current="assessment">
        <div className="ai-fade-in space-y-6">
          <Card className="ai-card p-6 text-center">
            <CheckCircle2 className="h-12 w-12 text-emerald-500 mx-auto" />
            <h2 className="ai-title text-2xl font-semibold mt-4">
              Assessment Complete!
            </h2>
            <p className="text-muted-foreground mt-2">
              View your skill-wise results and track progress.
            </p>
            <div className="mt-5 flex gap-3 justify-center">
              <Button
                onClick={() => setLocation("/analytics")}
                className="gap-2"
              >
                View Analytics <ArrowRight className="h-4 w-4" />
              </Button>
              <Button
                variant="secondary"
                onClick={() => setPhase("setup")}
              >
                Take Again
              </Button>
            </div>
          </Card>
        </div>
      </AppShell>
    );
  }

  // Test phase
  const q = questions[currentIdx];
  if (!q) return null;
  const answered = Object.keys(store.currentAnswers).length;
  const progress =
    questions.length > 0
      ? Math.round((answered / questions.length) * 100)
      : 0;

  return (
    <AppShell current="assessment">
      <div className="ai-fade-in space-y-6">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Badge variant="secondary" className="gap-1">
              <ClipboardCheck className="h-3.5 w-3.5" />
              Question {currentIdx + 1}/{questions.length}
            </Badge>
            <Badge variant="outline" className="text-emerald-600 border-emerald-500/30">
              Untimed Assessment
            </Badge>
          </div>
          <div className="text-sm text-muted-foreground">
            {answered}/{questions.length} answered
          </div>
        </div>
        <Progress value={progress} />

        <Card className="ai-card p-5 md:p-6">
          <Badge variant="outline" className="mb-3">
            {q.skill} • {q.difficulty}
          </Badge>
          <h3 className="text-lg font-medium">{q.text}</h3>
          <div className="mt-4 grid gap-3">
            {q.options.map((opt, optIdx) => {
              const sel = store.currentAnswers[q.id] === optIdx;
              return (
                <Card
                  key={optIdx}
                  className={`p-4 cursor-pointer transition-all hover:shadow-sm ${
                    sel ? "ring-2 ring-primary bg-primary/5" : ""
                  }`}
                  onClick={() => store.setCurrentAnswer(q.id, optIdx)}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`h-8 w-8 rounded-lg grid place-items-center text-sm font-medium shrink-0 ${
                        sel
                          ? "bg-primary text-primary-foreground"
                          : "bg-muted text-muted-foreground"
                      }`}
                    >
                      {String.fromCharCode(65 + optIdx)}
                    </div>
                    <span className="text-sm">{opt}</span>
                  </div>
                </Card>
              );
            })}
          </div>
        </Card>

        <div className="flex items-center justify-between gap-3">
          <Button
            variant="secondary"
            disabled={currentIdx === 0}
            onClick={() => setCurrentIdx((i) => i - 1)}
          >
            Previous
          </Button>
          <div className="flex gap-1.5 overflow-x-auto py-1">
            {questions.map((_, i) => (
              <button
                key={i}
                className={`h-7 w-7 rounded-md text-xs font-medium transition-colors ${
                  i === currentIdx
                    ? "bg-primary text-primary-foreground"
                    : store.currentAnswers[questions[i].id] !== undefined
                      ? "bg-emerald-500/10 text-emerald-600 border"
                      : "bg-muted text-muted-foreground"
                }`}
                onClick={() => setCurrentIdx(i)}
              >
                {i + 1}
              </button>
            ))}
          </div>
          {currentIdx < questions.length - 1 ? (
            <Button onClick={() => setCurrentIdx((i) => i + 1)}>Next</Button>
          ) : (
            <Button
              onClick={handleSubmit}
              className="gap-2"
              disabled={answered < questions.length}
            >
              Submit <CheckCircle2 className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>
    </AppShell>
  );
}

