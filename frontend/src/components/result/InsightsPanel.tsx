"use client";

import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Lightbulb, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";

interface InsightsPanelProps {
    insights: string[];
}

const getInsightIcon = (insight: string) => {
    const lowerInsight = insight.toLowerCase();
    if (lowerInsight.includes("warning") || lowerInsight.includes("missing")) {
        return AlertTriangle;
    }
    if (lowerInsight.includes("good") || lowerInsight.includes("clean")) {
        return CheckCircle;
    }
    if (lowerInsight.includes("trend") || lowerInsight.includes("correlation")) {
        return TrendingUp;
    }
    return Lightbulb;
};

const getInsightColor = (insight: string) => {
    const lowerInsight = insight.toLowerCase();
    if (lowerInsight.includes("warning") || lowerInsight.includes("missing")) {
        return "text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20";
    }
    if (lowerInsight.includes("good") || lowerInsight.includes("clean")) {
        return "text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20";
    }
    if (lowerInsight.includes("trend") || lowerInsight.includes("correlation")) {
        return "text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20";
    }
    return "text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-900/20";
};

export function InsightsPanel({ insights }: InsightsPanelProps) {
    if (!insights || insights.length === 0) {
        return null;
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
        >
            <Card glass>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Lightbulb className="w-5 h-5 text-purple-500" />
                        AI-Generated Insights
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <ul className="space-y-3">
                        {insights.map((insight, idx) => {
                            const Icon = getInsightIcon(insight);
                            const colorClass = getInsightColor(insight);

                            return (
                                <motion.li
                                    key={idx}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.4 + idx * 0.1 }}
                                    className={`flex items-start gap-3 p-3 rounded-xl ${colorClass}`}
                                >
                                    <Icon className="w-5 h-5 flex-shrink-0 mt-0.5" />
                                    <span className="text-sm">{insight}</span>
                                </motion.li>
                            );
                        })}
                    </ul>
                </CardContent>
            </Card>
        </motion.div>
    );
}
