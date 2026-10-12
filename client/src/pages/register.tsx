import { useState } from "react";
import { useLocation, Link } from "wouter";
import { Compass, Loader2 } from "lucide-react";
import { fetchWithAuth } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

export default function Register() {
  const [, setLocation] = useLocation();
  const { toast } = useToast();
  
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      toast({
        title: "Validation Error",
        description: "Passwords do not match.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    try {
      await fetchWithAuth("/auth/register", {
        method: "POST",
        body: JSON.stringify({ name, email, password }),
      });
      toast({
        title: "Registration successful!",
        description: "Please sign in with your new credentials.",
      });
      setLocation("/login");
    } catch (error: any) {
      toast({
        title: "Registration Failed",
        description: error.message || "An error occurred",
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
             <h1 className="text-3xl font-bold ai-title">Create an account</h1>
             <p className="text-muted-foreground text-center">Join Career Compass AI today</p>
          </div>
          
          <Card className="ai-card p-6 md:p-8 shrink-0">
             <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                   <label className="text-sm font-medium">Full Name</label>
                   <input 
                      type="text" 
                      required
                      value={name}
                      onChange={e => setName(e.target.value)}
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      placeholder="Saravanan"
                   />
                </div>

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
                      minLength={6}
                   />
                </div>

                <div className="space-y-2">
                   <label className="text-sm font-medium">Confirm Password</label>
                   <input 
                      type="password" 
                      required
                      value={confirmPassword}
                      onChange={e => setConfirmPassword(e.target.value)}
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      placeholder="••••••••"
                      minLength={6}
                   />
                </div>

                <Button type="submit" className="w-full" disabled={isLoading}>
                   {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                   Register
                </Button>
             </form>
             <div className="mt-6 text-center text-sm text-muted-foreground">
                Already have an account? <Link href="/login"><a className="text-primary hover:underline">Sign In here</a></Link>
             </div>
          </Card>
       </div>
    </div>
  );
}
