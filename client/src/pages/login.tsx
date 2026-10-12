import { useState } from "react";
import { useLocation, Link } from "wouter";
import { Compass, Loader2 } from "lucide-react";
import { useAuthStore } from "@/state/auth-store";
import { fetchWithAuth } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

export default function Login() {
  const [, setLocation] = useLocation();
  const { setAuth } = useAuthStore();
  const { toast } = useToast();
  
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const data = await fetchWithAuth("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      setAuth(data.user, data.access_token);
      toast({
        title: "Welcome back!",
        description: "Successfully logged in.",
      });
      setLocation("/dashboard");
    } catch (error: any) {
      toast({
        title: "Login Failed",
        description: error.message || "Invalid credentials",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid place-items-center bg-background p-4 flex-col">
       <div className="w-full max-w-md space-y-6">
          <div className="flex flex-col items-center gap-3">
             <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                <Compass className="h-6 w-6 text-primary" />
             </div>
             <h1 className="text-3xl font-bold ai-title">Welcome back</h1>
             <p className="text-muted-foreground text-center">Login to access your AI career features</p>
          </div>
          
          <Card className="ai-card p-6 md:p-8 shrink-0">
             <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                   <label className="text-sm font-medium">Email address</label>
                   <input 
                      type="email" 
                      required
                      value={email}
                      onChange={e => setEmail(e.target.value)}
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      placeholder="saravanan@example.com"
                   />
                </div>
                
                <div className="space-y-2">
                   <label className="text-sm font-medium">Password</label>
                   <input 
                      type="password" 
                      required
                      value={password}
                      onChange={e => setPassword(e.target.value)}
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      placeholder="••••••••"
                   />
                </div>

                <Button type="submit" className="w-full" disabled={isLoading}>
                   {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                   Sign In
                </Button>
             </form>
             <div className="mt-6 text-center text-sm text-muted-foreground">
                Don't have an account? <Link href="/register"><a className="text-primary hover:underline">Register here</a></Link>
             </div>
          </Card>
       </div>
    </div>
  );
}
