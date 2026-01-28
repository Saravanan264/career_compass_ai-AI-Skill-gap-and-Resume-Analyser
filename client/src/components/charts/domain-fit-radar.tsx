import { useMemo } from "react";
import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

import type { ResumeAnalysis } from "@/state/resume-store";

export function DomainFitRadarChart({ analysis }: { analysis: ResumeAnalysis }) {
  const data = useMemo(() => {
    return Object.entries(analysis.domains).map(([name, d]) => ({
      domain: name,
      fit: d.fitScore,
    }));
  }, [analysis]);

  return (
    <div className="h-[320px] w-full" data-testid="chart-domain-container">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data} outerRadius="80%">
          <PolarGrid stroke="hsl(var(--border))" />
          <PolarAngleAxis
            dataKey="domain"
            tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 12 }}
          />
          <PolarRadiusAxis
            angle={30}
            domain={[0, 100]}
            tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
            axisLine={{ stroke: "hsl(var(--border))" }}
          />
          <Tooltip
            contentStyle={{
              borderRadius: 12,
              border: "1px solid hsl(var(--border))",
              background: "hsl(var(--card))",
              color: "hsl(var(--foreground))",
              boxShadow: "var(--shadow-sm)",
            }}
          />
          <Radar
            name="Fit"
            dataKey="fit"
            stroke="hsl(var(--primary))"
            fill="hsl(var(--primary))"
            fillOpacity={0.15}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
