"use client";

import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Database, Columns, AlertTriangle, Hash } from "lucide-react";
import { DataSummary } from "@/types";

interface SummaryCardsProps {
    summary: DataSummary;
}

export function SummaryCards({ summary }: SummaryCardsProps) {
    const cards = [
        {
            title: "Total Rows",
            value: summary.rows.toLocaleString(),
            icon: Database,
            gradient: "from-purple-500 to-indigo-500",
        },
        {
            title: "Columns",
            value: summary.columns.toString(),
            icon: Columns,
            gradient: "from-indigo-500 to-blue-500",
        },
        {
            title: "Numeric Columns",
            value: summary.numericColumns.length.toString(),
            icon: Hash,
            gradient: "from-blue-500 to-cyan-500",
        },
        {
            title: "Missing Values",
            value: Object.values(summary.missingValues)
                .reduce((a, b) => a + b, 0)
                .toLocaleString(),
            icon: AlertTriangle,
            gradient: "from-orange-500 to-amber-500",
        },
    ];

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {cards.map((card, idx) => (
                <motion.div
                    key={card.title}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.1 }}
                >
                    <Card glass className="hover:shadow-glow transition-all duration-300">
                        <CardContent className="p-6">
                            <div className="flex items-center gap-4">
                                <div
                                    className={`w-12 h-12 rounded-xl bg-gradient-to-br ${card.gradient} flex items-center justify-center`}
                                >
                                    <card.icon className="w-6 h-6 text-white" />
                                </div>
                                <div>
                                    <p className="text-sm text-gray-500 dark:text-gray-400">
                                        {card.title}
                                    </p>
                                    <p className="text-2xl font-display font-bold text-gray-900 dark:text-white">
                                        {card.value}
                                    </p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </motion.div>
            ))}
        </div>
    );
}
