"use client";

import React, { useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useSession } from "next-auth/react";
import { motion } from "framer-motion";
import { CheckCircle2, Crown, Sparkles, ArrowRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import Link from "next/link";
import confetti from "canvas-confetti";

function UpgradeSuccessContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const { data: session } = useSession();
    const planId = searchParams.get("plan") || "pro";
    const orderId = searchParams.get("order_id");

    const planDetails: Record<string, { name: string; features: string[]; limit: number }> = {
        starter: {
            name: "Starter",
            limit: 15,
            features: [
                "15 file analyses per month",
                "Full EDA & correlations",
                "All chart types",
                "CSV & Excel download",
                "Email support",
            ],
        },
        pro: {
            name: "Pro",
            limit: 30,
            features: [
                "30 file analyses per month",
                "AI-powered insights",
                "All charts + Pair plots",
                "CSV, Excel & PDF download",
                "Priority support",
            ],
        },
    };

    const currentPlan = planDetails[planId] || planDetails.pro;

    // Update user plan in database
    useEffect(() => {
        const updateUserPlan = async () => {
            if (session?.user?.email && orderId) {
                try {
                    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/payment/upgrade`, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            email: session.user.email,
                            plan: planId,
                            orderId: orderId,
                            limit: currentPlan.limit,
                        }),
                    });

                    if (response.ok) {
                        console.log("✅ User plan upgraded successfully!");
                    }
                } catch (error) {
                    console.error("Failed to update plan:", error);
                }
            }
        };

        updateUserPlan();
    }, [session, orderId, planId, currentPlan.limit]);

    useEffect(() => {
        // Trigger confetti animation
        const duration = 3 * 1000;
        const animationEnd = Date.now() + duration;
        const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

        function randomInRange(min: number, max: number) {
            return Math.random() * (max - min) + min;
        }

        const interval: ReturnType<typeof setInterval> = setInterval(function () {
            const timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) {
                return clearInterval(interval);
            }

            const particleCount = 50 * (timeLeft / duration);

            confetti({
                ...defaults,
                particleCount,
                origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
                colors: ["#8b5cf6", "#6366f1", "#a855f7", "#f59e0b", "#eab308"],
            });
            confetti({
                ...defaults,
                particleCount,
                origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
                colors: ["#8b5cf6", "#6366f1", "#a855f7", "#f59e0b", "#eab308"],
            });
        }, 250);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="min-h-screen pt-24 pb-16 flex items-center justify-center relative">
            {/* Background */}
            <div className="absolute inset-0 -z-10">
                <div className="absolute inset-0 bg-gradient-to-b from-purple-50 via-white to-white dark:from-gray-900 dark:via-gray-900 dark:to-gray-900" />
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl" />
            </div>

            <div className="section-container">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5 }}
                    className="max-w-lg mx-auto text-center"
                >
                    <Card glass className="p-8 border-amber-500/30">
                        <motion.div
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                            className="w-20 h-20 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center mx-auto mb-6"
                        >
                            <Crown className="w-10 h-10 text-white" />
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.3 }}
                        >
                            <div className="flex items-center justify-center gap-2 mb-4">
                                <CheckCircle2 className="w-6 h-6 text-green-500" />
                                <span className="text-green-600 dark:text-green-400 font-medium">
                                    Payment Successful
                                </span>
                            </div>

                            <h1 className="text-3xl sm:text-4xl font-display font-bold mb-4">
                                Welcome to{" "}
                                <span className="bg-clip-text text-transparent bg-gradient-to-r from-amber-500 to-orange-500">
                                    {currentPlan.name}!
                                </span>
                            </h1>

                            <p className="text-gray-600 dark:text-gray-400 mb-8">
                                You now have access to all {currentPlan.name} features. Start exploring!
                            </p>

                            <div className="space-y-4">
                                <ul className="text-left space-y-3 mb-8">
                                    {currentPlan.features.map((feature, idx) => (
                                        <motion.li
                                            key={idx}
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: 0.4 + idx * 0.1 }}
                                            className="flex items-center gap-3"
                                        >
                                            <div className="w-5 h-5 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                                                <Sparkles className="w-3 h-3 text-green-600 dark:text-green-400" />
                                            </div>
                                            <span className="text-gray-700 dark:text-gray-300">
                                                {feature}
                                            </span>
                                        </motion.li>
                                    ))}
                                </ul>

                                <Link href="/upload">
                                    <Button size="lg" className="w-full group">
                                        Start Uploading
                                        <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                                    </Button>
                                </Link>

                                <Link href="/dashboard">
                                    <Button variant="ghost" size="lg" className="w-full">
                                        Go to Dashboard
                                    </Button>
                                </Link>
                            </div>
                        </motion.div>
                    </Card>
                </motion.div>
            </div>
        </div>
    );
}

export default function UpgradeSuccessPage() {
    return (
        <Suspense
            fallback={
                <div className="min-h-screen pt-24 flex items-center justify-center">
                    <Loader2 className="w-12 h-12 animate-spin text-purple-600" />
                </div>
            }
        >
            <UpgradeSuccessContent />
        </Suspense>
    );
}
