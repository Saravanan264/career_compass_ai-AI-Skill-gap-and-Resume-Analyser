import { useMemo } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ResumeAnalysis } from "@/state/resume-store";

export function AtsScoreBreakdownChart({ analysis }: { analysis: ResumeAnalysis }) {
  const data = useMemo(() => {
    const s = analysis.ats.sectionScores;
    return [
      { name: "Format", score: s.format, fill: "hsl(var(--chart-1))" },
      { name: "Experience", score: s.experience, fill: "hsl(var(--chart-2))" },
      { name: "Skills", score: s.skills, fill: "hsl(var(--chart-3))" },
      { name: "Education", score: s.education, fill: "hsl(var(--chart-4))" },
      { name: "Impact", score: s.impact, fill: "hsl(var(--chart-5))" },
    ];
  }, [analysis]);

  return (
    <div className="h-[280px] w-full" data-testid="chart-ats-container">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ left: 6, right: 6, top: 10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
          <XAxis
            dataKey="name"
            tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }}
            axisLine={{ stroke: "hsl(var(--border))" }}
            tickLine={{ stroke: "hsl(var(--border))" }}
          />
          <YAxis
            domain={[0, 100]}
            tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }}
            axisLine={{ stroke: "hsl(var(--border))" }}
            tickLine={{ stroke: "hsl(var(--border))" }}
          />
          <Tooltip
            cursor={{ fill: "hsl(var(--muted))" }}
            contentStyle={{
              borderRadius: 12,
              border: "1px solid hsl(var(--border))",
              background: "hsl(var(--card))",
              color: "hsl(var(--foreground))",
              boxShadow: "var(--shadow-sm)",
            }}
          />
          <Bar dataKey="score" radius={[10, 10, 0, 0]}>
            {data.map((d, idx) => (
              <Cell key={idx} fill={d.fill} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
