"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface User {
    name: string;
    email: string;
    plan: string;
}

interface AuthContextType {
    user: User | null;
    token: string | null;
    isLoading: boolean;
    login: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
    signup: (name: string, email: string, password: string) => Promise<{ success: boolean; error?: string }>;
    logout: () => void;
    isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Check for existing token on mount
    useEffect(() => {
        const storedToken = localStorage.getItem("kuya_token");
        const storedUser = localStorage.getItem("kuya_user");

        if (storedToken && storedUser) {
            setToken(storedToken);
            setUser(JSON.parse(storedUser));
            // Verify token is still valid
            verifyToken(storedToken);
        } else {
            setIsLoading(false);
        }
    }, []);

    const verifyToken = async (tokenToVerify: string) => {
        try {
            const response = await fetch(`${API_URL}/auth/me`, {
                headers: {
                    Authorization: `Bearer ${tokenToVerify}`,
                },
            });

            if (response.ok) {
                const userData = await response.json();
                setUser(userData);
                setToken(tokenToVerify);
            } else {
                // Token invalid, clear storage
                localStorage.removeItem("kuya_token");
                localStorage.removeItem("kuya_user");
                setToken(null);
                setUser(null);
            }
        } catch (error) {
            console.error("Token verification failed:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (email: string, password: string): Promise<{ success: boolean; error?: string }> => {
        try {
            const response = await fetch(`${API_URL}/auth/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                return { success: false, error: data.detail || "Login failed" };
            }

            // Save token and user
            localStorage.setItem("kuya_token", data.access_token);
            localStorage.setItem("kuya_user", JSON.stringify(data.user));
            setToken(data.access_token);
            setUser(data.user);

            return { success: true };
        } catch (error) {
            console.error("Login error:", error);
            return { success: false, error: "Network error. Please try again." };
        }
    };

    const signup = async (name: string, email: string, password: string): Promise<{ success: boolean; error?: string }> => {
        try {
            const response = await fetch(`${API_URL}/auth/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name, email, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                return { success: false, error: data.detail || "Signup failed" };
            }

            // Save token and user
            localStorage.setItem("kuya_token", data.access_token);
            localStorage.setItem("kuya_user", JSON.stringify(data.user));
            setToken(data.access_token);
            setUser(data.user);

            return { success: true };
        } catch (error) {
            console.error("Signup error:", error);
            return { success: false, error: "Network error. Please try again." };
        }
    };

    const logout = () => {
        localStorage.removeItem("kuya_token");
        localStorage.removeItem("kuya_user");
        setToken(null);
        setUser(null);
    };

    const value = {
        user,
        token,
        isLoading,
        login,
        signup,
        logout,
        isAuthenticated: !!user && !!token,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}
