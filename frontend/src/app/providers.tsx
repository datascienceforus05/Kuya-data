"use client";

import { ReactNode } from "react";
import { Toaster } from "sonner";
import { ScrollProgress } from "@/components/ui/ScrollProgress";
import { AuthProvider } from "@/contexts/AuthContext";

export function Providers({ children }: { children: ReactNode }) {
    return (
        <AuthProvider>
            <ScrollProgress />
            {children}
            <Toaster position="top-center" richColors />
        </AuthProvider>
    );
}
