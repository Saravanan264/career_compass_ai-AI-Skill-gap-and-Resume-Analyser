import { useMemo } from "react";
import { useLocation } from "wouter";
import { ArrowRight, Info, LineChart, TrendingDown, TrendingUp, Minus } from "lucide-react";
import { ResponsiveContainer, LineChart as ReLineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar, Cell } from "recharts";
import { AppShell } from "@/components/app-shell";
import { useAssessmentStore } from "@/state/assessment-store";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { computeAnalytics } from "@/lib/analytics-engine";

export default function Analytics() {
  const [, setLocation] = useLocation();
  const { attempts } = useAssessmentStore();
  const analytics = useMemo(() => computeAnalytics(attempts), [attempts]);

  if (analytics.totalAttempts === 0) {
    return (
      <AppShell current="analytics">
        <Card className="ai-card p-6">
          <div className="flex items-start gap-3">
            <Info className="h-5 w-5 mt-0.5 text-muted-foreground" />
            <div>
              <div className="font-medium">No assessment history</div>
              <div className="text-sm text-muted-foreground">Complete your first assessment to start tracking skill improvement.</div>
              <Button className="mt-4" onClick={() => setLocation("/assessment")}>Start Assessment</Button>
            </div>
          </div>
        </Card>
      </AppShell>
    );
  }

  const overallData = attempts.map((a, i) => ({ attempt: `#${i + 1}`, score: a.overallScore }));
  const latestAttempt = attempts[attempts.length - 1];
  const trendIcon = (trend: string) => {
    if (trend === "improving") return <TrendingUp className="h-4 w-4 text-emerald-500" />;
    if (trend === "declining") return <TrendingDown className="h-4 w-4 text-rose-500" />;
    return <Minus className="h-4 w-4 text-muted-foreground" />;
  };

  return (
    <AppShell current="analytics">
      <div className="ai-fade-in space-y-6">
        <div>
          <Badge variant="secondary" className="gap-1 mb-2"><LineChart className="h-3.5 w-3.5" />Skill Analytics</Badge>
          <h2 className="ai-title text-2xl md:text-3xl font-semibold">Your Skill Progress</h2>
          <p className="text-muted-foreground max-w-2xl mt-1">Track how your skills improve across multiple assessment attempts.</p>
        </div>

        {/* Summary Cards */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Card className="ai-card p-4"><div className="text-xs text-muted-foreground">Total Attempts</div><div className="ai-title text-2xl font-semibold mt-1">{analytics.totalAttempts}</div></Card>
          <Card className="ai-card p-4"><div className="text-xs text-muted-foreground">Latest Score</div><div className="ai-title text-2xl font-semibold mt-1">{analytics.latestScore}%</div></Card>
          <Card className="ai-card p-4"><div className="text-xs text-muted-foreground">Best Score</div><div className="ai-title text-2xl font-semibold mt-1">{analytics.bestScore}%</div></Card>
          <Card className="ai-card p-4">
            <div className="text-xs text-muted-foreground">Improvement</div>
            <div className="ai-title text-2xl font-semibold mt-1 flex items-center gap-1">
              {analytics.overallImprovement > 0 ? "+" : ""}{analytics.overallImprovement}%
              {analytics.overallImprovement > 0 && <TrendingUp className="h-4 w-4 text-emerald-500" />}
            </div>
          </Card>
        </div>

        {/* Overall Progress Chart */}
        {attempts.length >= 2 && (
          <Card className="ai-card p-5">
            <div className="font-medium">Overall Score Progression</div>
            <div className="h-[250px] mt-4">
              <ResponsiveContainer width="100%" height="100%">
                <ReLineChart data={overallData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis dataKey="attempt" tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }} />
                  <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid hsl(var(--border))", background: "hsl(var(--card))", color: "hsl(var(--foreground))" }} />
                  <Line type="monotone" dataKey="score" stroke="hsl(var(--primary))" strokeWidth={2} dot={{ fill: "hsl(var(--primary))", r: 5 }} />
                </ReLineChart>
              </ResponsiveContainer>
            </div>
          </Card>
        )}

        {/* Latest Skill-wise Scores */}
        <Card className="ai-card p-5">
          <div className="font-medium">Skill-wise Performance (Latest)</div>
          <div className="text-sm text-muted-foreground mt-1">From attempt #{analytics.totalAttempts}</div>
          <div className="h-[300px] mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={latestAttempt.skillScores} layout="vertical" margin={{ left: 80 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis type="number" domain={[0, 100]} tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }} />
                <YAxis type="category" dataKey="skill" tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }} width={80} />
                <Tooltip contentStyle={{ borderRadius: 12, border: "1px solid hsl(var(--border))", background: "hsl(var(--card))", color: "hsl(var(--foreground))" }} />
                <Bar dataKey="score" radius={[0, 6, 6, 0]}>
                  {latestAttempt.skillScores.map((s, i) => (
                    <Cell key={i} fill={s.score >= 70 ? "hsl(var(--chart-5))" : s.score >= 40 ? "hsl(var(--chart-4))" : "hsl(var(--destructive))"} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Skill Progress Table */}
        <Card className="ai-card p-5">
          <div className="font-medium mb-4">Longitudinal Skill Progress Tracking</div>
          <div className="space-y-3">
            {analytics.skillProgress.map((sp) => (
              <div key={sp.skill} className="rounded-xl border p-3">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    {trendIcon(sp.trend)}
                    <span className="text-sm font-medium">{sp.skill}</span>
                    <Badge variant={sp.status === "Strong" ? "default" : sp.status === "Developing" ? "secondary" : "outline"} className="text-[10px]">
                      {sp.status}
                    </Badge>
                  </div>
                  <div className="flex flex-wrap items-center gap-3 text-xs md:text-sm">
                    <span className="text-muted-foreground">{sp.attemptCount} Attempt{sp.attemptCount > 1 ? "s" : ""}</span>
                    {sp.previousScore !== null && <span className="text-muted-foreground">Prev: {sp.previousScore}%</span>}
                    <span className="font-medium">Latest: {sp.latestScore}%</span>
                    {sp.improvement !== null && (
                      <Badge variant={sp.improvement > 0 ? "default" : "secondary"} className="text-xs">
                        {sp.improvement > 0 ? "+" : ""}{sp.improvement}%
                      </Badge>
                    )}
                  </div>
                </div>
                <Progress value={sp.latestScore} className="mt-2" />
              </div>
            ))}
          </div>
        </Card>

        <div className="flex gap-3">
          <Button onClick={() => setLocation("/roadmap")} className="gap-2">View Roadmap <ArrowRight className="h-4 w-4" /></Button>
          <Button variant="secondary" onClick={() => setLocation("/assessment")}>Take Again</Button>
        </div>
      </div>
    </AppShell>
  );
}
