"use client";

import { SessionProvider } from "next-auth/react";
import { ReactNode } from "react";
import { Toaster } from "sonner";
import { ScrollProgress } from "@/components/ui/ScrollProgress";

export function Providers({ children }: { children: ReactNode }) {
    return (
        <SessionProvider>
            <ScrollProgress />
            {children}
            <Toaster position="top-center" richColors />
        </SessionProvider>
    );
}
