"use client";

import React, { useEffect, useState } from "react";
import { useSession, signIn } from "next-auth/react";
import { motion } from "framer-motion";
import Link from "next/link";
import {
    LayoutDashboard,
    Upload,
    FileText,
    Crown,
    Loader2,
    ArrowRight,
    Calendar,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatDate } from "@/lib/utils";

interface Report {
    _id: string;
    reportId: string;
    fileName: string;
    createdAt: string;
}

interface UserData {
    plan: string;
    planLimit: number;
    usedThisMonth: number;
}

export default function DashboardPage() {
    const { data: session, status } = useSession();
    const [reports, setReports] = useState<Report[]>([]);
    const [loading, setLoading] = useState(true);
    const [userData, setUserData] = useState<UserData>({ plan: "free", planLimit: 3, usedThisMonth: 0 });

    useEffect(() => {
        if (status === "unauthenticated") {
            signIn("google");
            return;
        }

        if (session?.user?.email) {
            const fetchData = async () => {
                try {
                    // Fetch user data from API
                    const userRes = await fetch(
                        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/user/${encodeURIComponent(session.user!.email!)}`
                    );
                    if (userRes.ok) {
                        const user = await userRes.json();
                        setUserData({
                            plan: user.plan || "free",
                            planLimit: user.planLimit || 3,
                            usedThisMonth: user.usedThisMonth || 0,
                        });
                    }

                    // Fetch user reports from API
                    const reportsRes = await fetch(
                        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/report/user/${encodeURIComponent(session.user!.email!)}`
                    );
                    if (reportsRes.ok) {
                        const reportsData = await reportsRes.json();
                        setReports(reportsData.reports || []);
                    }
                } catch (error) {
                    console.error("Failed to fetch data:", error);
                } finally {
                    setLoading(false);
                }
            };

            fetchData();
        }
    }, [session, status]);

    if (status === "loading" || loading) {
        return (
            <div className="min-h-screen pt-24 flex items-center justify-center">
                <Loader2 className="w-12 h-12 animate-spin text-purple-600" />
            </div>
        );
    }

    if (!session) {
        return null;
    }

    return (
        <div className="min-h-screen pt-24 pb-16 relative">
            {/* Background */}
            <div className="absolute inset-0 -z-10">
                <div className="absolute inset-0 bg-gradient-to-b from-purple-50 via-white to-white dark:from-gray-900 dark:via-gray-900 dark:to-gray-900" />
            </div>

            <div className="section-container">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-12"
                >
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                        <div>
                            <h1 className="text-3xl sm:text-4xl font-display font-bold mb-2">
                                Welcome back,{" "}
                                <span className="gradient-text">
                                    {session.user?.name?.split(" ")[0]}
                                </span>
                            </h1>
                            <p className="text-gray-600 dark:text-gray-400">
                                Manage your data analysis reports and account
                            </p>
                        </div>
                        <Link href="/upload">
                            <Button size="lg">
                                <Upload className="w-4 h-4 mr-2" />
                                New Upload
                            </Button>
                        </Link>
                    </div>
                </motion.div>

                {/* Plan Status */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.1 }}
                    className="mb-8"
                >
                    <Card
                        glass
                        className={`overflow-hidden ${userData.plan !== "free" ? "border-amber-500/50" : ""
                            }`}
                    >
                        <div
                            className={`p-6 ${userData.plan !== "free"
                                ? "bg-gradient-to-r from-amber-500/10 via-orange-500/10 to-yellow-500/10"
                                : ""
                                }`}
                        >
                            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                                <div className="flex items-center gap-4">
                                    <div
                                        className={`w-14 h-14 rounded-xl flex items-center justify-center ${userData.plan !== "free"
                                            ? "bg-gradient-to-br from-amber-500 to-orange-500"
                                            : "bg-gradient-to-br from-purple-500 to-indigo-500"
                                            }`}
                                    >
                                        {userData.plan !== "free" ? (
                                            <Crown className="w-7 h-7 text-white" />
                                        ) : (
                                            <LayoutDashboard className="w-7 h-7 text-white" />
                                        )}
                                    </div>
                                    <div>
                                        <div className="flex items-center gap-2 mb-1">
                                            <h3 className="text-xl font-display font-bold capitalize">
                                                {userData.plan} Plan
                                            </h3>
                                            <Badge variant={userData.plan !== "free" ? "pro" : "default"}>
                                                {userData.plan.toUpperCase()}
                                            </Badge>
                                        </div>
                                        <p className="text-gray-600 dark:text-gray-400">
                                            {userData.planLimit >= 999999
                                                ? "Unlimited uploads and all premium features"
                                                : `${userData.planLimit} analyses/month • ${userData.usedThisMonth} used`}
                                        </p>
                                    </div>
                                </div>

                                {userData.plan === "free" && (
                                    <Link href="/pricing">
                                        <Button className="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600">
                                            <Crown className="w-4 h-4 mr-2" />
                                            Upgrade
                                        </Button>
                                    </Link>
                                )}
                            </div>
                        </div>
                    </Card>
                </motion.div>

                {/* Quick Stats */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8"
                >
                    {[
                        { label: "Total Reports", value: reports.length, icon: FileText },
                        { label: "Used This Month", value: userData.usedThisMonth, icon: Calendar },
                        {
                            label: "Remaining",
                            value: userData.planLimit >= 999999 ? "∞" : (userData.planLimit - userData.usedThisMonth),
                            icon: Upload,
                        },
                    ].map((stat, idx) => (
                        <Card key={idx} glass className="p-6">
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                                    <stat.icon className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                                </div>
                                <div>
                                    <p className="text-sm text-gray-500 dark:text-gray-400">
                                        {stat.label}
                                    </p>
                                    <p className="text-2xl font-display font-bold">
                                        {stat.value}
                                    </p>
                                </div>
                            </div>
                        </Card>
                    ))}
                </motion.div>

                {/* Recent Reports */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                >
                    <Card glass>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <FileText className="w-5 h-5 text-purple-500" />
                                Recent Reports
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            {reports.length === 0 ? (
                                <div className="text-center py-12">
                                    <FileText className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                                    <p className="text-gray-500 dark:text-gray-400 mb-4">
                                        No reports yet. Upload your first file!
                                    </p>
                                    <Link href="/upload">
                                        <Button>
                                            <Upload className="w-4 h-4 mr-2" />
                                            Upload Data
                                        </Button>
                                    </Link>
                                </div>
                            ) : (
                                <div className="space-y-3">
                                    {reports.map((report, idx) => (
                                        <motion.div
                                            key={report._id}
                                            initial={{ opacity: 0, x: -20 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            transition={{ delay: 0.4 + idx * 0.1 }}
                                        >
                                            <Link href={`/result?id=${report.reportId}`}>
                                                <div className="flex items-center justify-between p-4 rounded-xl border border-gray-200 dark:border-gray-700 hover:border-purple-500/50 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-all group">
                                                    <div className="flex items-center gap-4">
                                                        <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                                                            <FileText className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                                                        </div>
                                                        <div>
                                                            <p className="font-medium text-gray-900 dark:text-white">
                                                                {report.fileName}
                                                            </p>
                                                            <p className="text-sm text-gray-500 dark:text-gray-400">
                                                                {formatDate(report.createdAt)}
                                                            </p>
                                                        </div>
                                                    </div>
                                                    <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-purple-500 group-hover:translate-x-1 transition-all" />
                                                </div>
                                            </Link>
                                        </motion.div>
                                    ))}
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </motion.div>
            </div>
        </div>
    );
}
