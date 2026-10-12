import { Route, Switch, useLocation } from "wouter";
import { QueryClientProvider } from "@tanstack/react-query";
import { TooltipProvider } from "@/components/ui/tooltip";
import { Toaster } from "@/components/ui/toaster";
import { queryClient } from "./lib/queryClient";

import NotFound from "@/pages/not-found";
import Dashboard from "@/pages/dashboard";
import ResumeUpload from "@/pages/resume-upload";
import AtsDashboard from "@/pages/ats-dashboard";
import JobAnalysis from "@/pages/job-analysis";
import SkillGapAnalysis from "@/pages/skill-gap-analysis";
import Projects from "@/pages/projects";
import JobRoles from "@/pages/job-roles";
import Assessment from "@/pages/assessment";
import Analytics from "@/pages/analytics";
import LearningRoadmap from "@/pages/learning-roadmap";
import Readiness from "@/pages/readiness";
import CareerInsights from "@/pages/career-insights";
import Login from "@/pages/login";
import Register from "@/pages/register";

function RedirectToDashboard() {
  const [, setLocation] = useLocation();
  setLocation("/dashboard");
  return null;
}

function Router() {
  return (
    <Switch>
      <Route path="/" component={RedirectToDashboard} />
      <Route path="/login" component={Login} />
      <Route path="/register" component={Register} />
      <Route path="/dashboard" component={Dashboard} />
      <Route path="/upload" component={ResumeUpload} />
      <Route path="/ats" component={AtsDashboard} />
      <Route path="/job-analysis" component={JobAnalysis} />
      <Route path="/skills" component={SkillGapAnalysis} />
      <Route path="/projects" component={Projects} />
      <Route path="/job-roles" component={JobRoles} />
      <Route path="/assessment" component={Assessment} />
      <Route path="/analytics" component={Analytics} />
      <Route path="/roadmap" component={LearningRoadmap} />
      <Route path="/readiness" component={Readiness} />
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
