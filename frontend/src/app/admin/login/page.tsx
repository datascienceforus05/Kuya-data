"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Lock, User, ShieldAlert, Rocket } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { toast } from "sonner";

export default function AdminLoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                localStorage.setItem("admin_token", data.token);
                toast.success("Welcome back, Captain!");
                router.push("/admin");
            } else {
                toast.error(data.detail || "Invalid credentials");
            }
        } catch (error) {
            toast.error("Connection failed. Is the backend running?");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
            <div className="absolute inset-0 -z-10 overflow-hidden">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-pulse delay-700" />
            </div>

            <Card className="w-full max-w-md p-8 border-t-4 border-t-purple-600 shadow-2xl bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-2xl flex items-center justify-center mx-auto mb-4">
                        <Rocket className="w-8 h-8 text-purple-600" />
                    </div>
                    <h1 className="text-2xl font-bold font-display">Kuya Command Center</h1>
                    <p className="text-gray-500 dark:text-gray-400 mt-2">Enter your credentials to access the bridge</p>
                </div>

                <form onSubmit={handleLogin} className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-sm font-medium flex items-center gap-2">
                            <User className="w-4 h-4 text-purple-600" />
                            Username
                        </label>
                        <Input
                            type="text"
                            placeholder="Admin ID"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="bg-white/50 dark:bg-gray-900/50"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm font-medium flex items-center gap-2">
                            <Lock className="w-4 h-4 text-purple-600" />
                            Security Key
                        </label>
                        <Input
                            type="password"
                            placeholder="••••••••"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="bg-white/50 dark:bg-gray-900/50"
                            required
                        />
                    </div>

                    <Button
                        type="submit"
                        className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white py-6 rounded-xl shadow-lg shadow-purple-500/20"
                        disabled={isLoading}
                    >
                        {isLoading ? "Synchronizing..." : "Initialize Control Panel"}
                    </Button>
                </form>

                <div className="mt-8 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-800 flex items-start gap-3">
                    <ShieldAlert className="w-5 h-5 text-red-600 mt-0.5" />
                    <p className="text-xs text-red-800 dark:text-red-400 font-medium">
                        Unauthorized access is strictly monitored. All attempts are logged with IP and location data.
                    </p>
                </div>
            </Card>
        </div>
    );
}
