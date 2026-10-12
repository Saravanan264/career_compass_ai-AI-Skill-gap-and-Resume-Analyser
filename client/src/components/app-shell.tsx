import { PropsWithChildren } from "react";
import { Link, useLocation } from "wouter";
import { useAuthStore } from "@/state/auth-store";
import {
  BarChart3,
  BookOpen,
  BriefcaseBusiness,
  Briefcase,
  ClipboardCheck,
  Compass,
  FileText,
  FileUp,
  LayoutDashboard,
  MapPinned,
  Rocket,
  ShieldCheck,
  Target,
  TrendingUp,
} from "lucide-react";

type NavKey =
  | "dashboard"
  | "upload"
  | "ats"
  | "job-analysis"
  | "skills"
  | "projects"
  | "job-roles"
  | "assessment"
  | "analytics"
  | "roadmap"
  | "readiness"
  | "insights";

const navItems: {
  key: NavKey;
  href: string;
  icon: React.ElementType;
  label: string;
}[] = [
  { key: "dashboard", href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { key: "upload", href: "/upload", icon: FileUp, label: "Resume Upload" },
  { key: "ats", href: "/ats", icon: BarChart3, label: "Resume Analysis" },
  { key: "job-analysis", href: "/job-analysis", icon: BriefcaseBusiness, label: "Job Analysis" },
  { key: "skills", href: "/skills", icon: Target, label: "Skill Gap" },
  { key: "projects", href: "/projects", icon: Rocket, label: "Projects" },
  { key: "job-roles", href: "/job-roles", icon: Briefcase, label: "Job Roles" },
  { key: "assessment", href: "/assessment", icon: ClipboardCheck, label: "Assessment" },
  { key: "analytics", href: "/analytics", icon: TrendingUp, label: "Skill Analytics" },
  { key: "roadmap", href: "/roadmap", icon: MapPinned, label: "Career Roadmap" },
  { key: "readiness", href: "/readiness", icon: ShieldCheck, label: "Readiness" },
];

function NavItem({
  href,
  active,
  icon: Icon,
  label,
}: {
  href: string;
  active: boolean;
  icon: React.ElementType;
  label: string;
}) {
  return (
    <Link href={href}>
      <div
        className={
          "cc-nav-item" + (active ? " cc-nav-active" : "")
        }
      >
        <Icon className="cc-nav-icon" />
        <span>{label}</span>
      </div>
    </Link>
  );
}

export function AppShell({
  children,
  current,
}: PropsWithChildren<{ current: NavKey }>) {
  const { user, isAuthenticated, logout } = useAuthStore();
  const [, setLocation] = useLocation();

  const handleLogout = () => {
    logout();
    setLocation("/login");
  };

  return (
    <div className="cc-shell">
      {/* ─── Sidebar ─── */}
      <aside className="cc-sidebar">
        {/* Brand */}
        <div className="cc-sidebar-brand">
          <Link href="/dashboard">
            <div className="cc-brand-link">
              <div className="cc-brand-icon">
                <Compass className="h-5 w-5" />
              </div>
              <div className="cc-brand-text">
                <span className="cc-brand-name">Career Compass AI</span>
                <span className="cc-brand-sub">
                  Employability Assessment
                  <br />
                  &amp; Career Readiness
                </span>
              </div>
            </div>
          </Link>
        </div>

        {/* Navigation (scrollable middle) */}
        <nav className="cc-sidebar-nav">
          {navItems.map((item) => (
            <NavItem
              key={item.key}
              href={item.href}
              active={current === item.key}
              icon={item.icon}
              label={item.label}
            />
          ))}
        </nav>

        {/* Profile (anchored bottom) */}
        <div className="cc-sidebar-profile relative group">
          <div className="cc-profile-avatar">
            {isAuthenticated ? user?.name.substring(0, 2).toUpperCase() : "SA"}
          </div>
          <div className="cc-profile-info">
            <span className="cc-profile-name">{isAuthenticated ? user?.name : "Saravanan"}</span>
            <span className="cc-profile-plan">{isAuthenticated ? user?.plan : "Free"}</span>
          </div>
          {isAuthenticated ? (
            <button 
              onClick={handleLogout} 
              className="absolute right-4 text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity text-destructive hover:underline"
            >
              Logout
            </button>
          ) : (
            <Link href="/login">
              <span className="absolute right-4 text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity text-primary hover:underline">
                Sign In
              </span>
            </Link>
          )}
        </div>
      </aside>

      {/* ─── Main content ─── */}
      <main className="cc-main">
        <div className="cc-main-inner">{children}</div>
      </main>
    </div>
  );
}
