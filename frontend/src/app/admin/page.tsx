"use client";

import React, { useEffect, useState } from "react";
import {
    Users,
    FileText,
    TrendingUp,
    DollarSign,
    Activity,
    ArrowUpRight,
    RefreshCcw,
    Clock
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { motion } from "framer-motion";

interface Stats {
    users: {
        total: number;
        pro: number;
        starter: number;
        enterprise: number;
        free: number;
    };
    reports: {
        total: number;
        recent30Days: number;
    };
    revenue: {
        estimatedTotal: number;
        paidUsersCount: number;
    };
}

export default function AdminDashboard() {
    const [stats, setStats] = useState<Stats | null>(null);
    const [loading, setLoading] = useState(true);

    const fetchStats = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem("admin_token");
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/stats`, {
                headers: { "x-admin-token": token || "" }
            });
            if (response.ok) {
                const data = await response.json();
                setStats(data);
            } else {
                toast.error("Failed to fetch statistics");
            }
        } catch (error) {
            toast.error("API error occurred");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStats();
    }, []);

    if (loading && !stats) return <div className="flex items-center justify-center h-full"><RefreshCcw className="animate-spin text-purple-600" /></div>;

    const cards = [
        {
            title: "Total Users",
            value: stats?.users.total || 0,
            sub: `${stats?.users.pro} Pro, ${stats?.users.starter} Starter`,
            icon: Users,
            color: "blue"
        },
        {
            title: "Reports Generated",
            value: stats?.reports.total || 0,
            sub: `${stats?.reports.recent30Days} in last 30 days`,
            icon: FileText,
            color: "purple"
        },
        {
            title: "Est. Revenue",
            value: `₹${(stats?.revenue.estimatedTotal || 0).toLocaleString()}`,
            sub: "Based on Pro subscriptions",
            icon: DollarSign,
            color: "green"
        },
        {
            title: "Paid Conversions",
            value: stats?.revenue.paidUsersCount || 0,
            sub: `${(((stats?.revenue.paidUsersCount || 0) / (stats?.users.total || 1)) * 100).toFixed(1)}% conversion rate`,
            icon: TrendingUp,
            color: "amber"
        }
    ];

    return (
        <div className="space-y-8 pb-12">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold font-display">System Overview</h1>
                    <p className="text-gray-500 text-sm">Real-time health and performance metrics</p>
                </div>
                <Button variant="outline" size="sm" onClick={fetchStats} disabled={loading}>
                    <RefreshCcw className={loading ? "animate-spin mr-2" : "mr-2"} size={16} />
                    Refresh Data
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {cards.map((card, idx) => (
                    <motion.div
                        key={card.title}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.1 }}
                    >
                        <Card className="p-6 relative overflow-hidden group hover:shadow-xl transition-all duration-300">
                            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                                <card.icon size={80} />
                            </div>
                            <div className="flex items-center gap-4 mb-4">
                                <div className={`p-2 rounded-lg bg-${card.color}-100 dark:bg-${card.color}-900/30 text-${card.color}-600`}>
                                    <card.icon size={24} />
                                </div>
                                <span className="text-sm font-medium text-gray-500">{card.title}</span>
                            </div>
                            <div className="text-3xl font-bold mb-1">{card.value}</div>
                            <div className="text-xs text-gray-400 font-medium flex items-center gap-1">
                                {card.sub}
                            </div>
                        </Card>
                    </motion.div>
                ))}
            </div>

            <div className="grid lg:grid-cols-3 gap-6">
                <Card className="lg:col-span-2 p-6">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="font-bold flex items-center gap-2">
                            <Activity className="text-purple-600" />
                            Recent System Activity
                        </h3>
                        <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">Live</span>
                    </div>

                    <div className="space-y-4">
                        {/* Placeholder for real activity log */}
                        {[
                            "New Enterprise user direct upgrade by Admin",
                            "Payment webhook received from order_x92k",
                            "Automated report cleanup completed",
                            "System backup successfully verified"
                        ].map((text, i) => (
                            <div key={i} className="flex items-center gap-4 p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700/50">
                                <div className="w-2 h-2 rounded-full bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.5)]" />
                                <div className="flex-1 text-sm font-medium">{text}</div>
                                <div className="text-xs text-gray-400">Just now</div>
                            </div>
                        ))}
                    </div>
                </Card>

                <Card className="p-6">
                    <h3 className="font-bold mb-6 flex items-center gap-2">
                        <Clock className="text-indigo-600" />
                        Plan Distribution
                    </h3>
                    <div className="space-y-4">
                        {[
                            { label: "Pro", count: stats?.users.pro || 0, color: "purple" },
                            { label: "Starter", count: stats?.users.starter || 0, color: "blue" },
                            { label: "Enterprise", count: stats?.users.enterprise || 0, color: "amber" },
                            { label: "Free", count: stats?.users.free || 0, color: "gray" },
                        ].map((plan) => (
                            <div key={plan.label}>
                                <div className="flex justify-between text-sm mb-1">
                                    <span className="font-medium">{plan.label}</span>
                                    <span className="text-gray-500">{plan.count}</span>
                                </div>
                                <div className="h-2 w-full bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                                    <div
                                        className={`h-full bg-${plan.color}-500`}
                                        style={{ width: `${((plan.count / (stats?.users.total || 1)) * 100)}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </Card>
            </div>
        </div>
    );
}
