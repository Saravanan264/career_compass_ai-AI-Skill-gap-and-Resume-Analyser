import { Route, Switch, useLocation } from "wouter";
import { QueryClientProvider } from "@tanstack/react-query";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Toaster } from "@/components/ui/toaster";
import { queryClient } from "./lib/queryClient";

import NotFound from "@/pages/not-found";
import ResumeUpload from "@/pages/resume-upload";
import AtsDashboard from "@/pages/ats-dashboard";
import SkillGapAnalysis from "@/pages/skill-gap-analysis";
import LearningRoadmap from "@/pages/learning-roadmap";
import CareerInsights from "@/pages/career-insights";

function RedirectToUpload() {
  const [, setLocation] = useLocation();
  setLocation("/upload");
  return null;
}

function Router() {
  return (
    <Switch>
      <Route path="/" component={RedirectToUpload} />
      <Route path="/upload" component={ResumeUpload} />
      <Route path="/ats" component={AtsDashboard} />
      <Route path="/skills" component={SkillGapAnalysis} />
      <Route path="/roadmap" component={LearningRoadmap} />
      <Route path="/insights" component={CareerInsights} />
      <Route component={NotFound} />
    </Switch>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Router />
      </TooltipProvider>
    </QueryClientProvider>
  );
}
