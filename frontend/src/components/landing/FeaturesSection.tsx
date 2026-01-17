"use client";

import React from "react";
import { motion } from "framer-motion";
import {
    Sparkles,
    BarChart3,
    FileDown,
    Shield,
    Zap,
    PieChart,
} from "lucide-react";
import { Card } from "@/components/ui/card";

const features = [
    {
        icon: Sparkles,
        title: "Smart Cleaning with Warnings",
        description:
            "Automatically handle missing values, fix data types, and get clear warnings about what was changed and why.",
        gradient: "from-purple-500 to-indigo-500",
    },
    {
        icon: BarChart3,
        title: "EDA with Context & Priority",
        description:
            "Get prioritized insights that matter most. We highlight what's important, not just everything.",
        gradient: "from-indigo-500 to-blue-500",
    },
    {
        icon: PieChart,
        title: "Charts That Tell Stories",
        description:
            "Visualizations with explanations. Each chart comes with context about what you're seeing.",
        gradient: "from-blue-500 to-cyan-500",
    },
    {
        icon: FileDown,
        title: "Decision-Ready Reports",
        description:
            "Download reports that guide decisions, not just display numbers. Share confidently with stakeholders.",
        gradient: "from-cyan-500 to-teal-500",
    },
    {
        icon: Zap,
        title: "ML Intelligence Built-In",
        description:
            "Get model recommendations, preprocessing advice, and deployment readiness checks automatically.",
        gradient: "from-teal-500 to-green-500",
    },
    {
        icon: Shield,
        title: "Secure & Private",
        description:
            "Your data is encrypted, processed securely, and never shared. Delete anytime.",
        gradient: "from-green-500 to-emerald-500",
    },
];

const container = {
    hidden: { opacity: 0 },
    show: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1,
        },
    },
};

const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 },
};

export function FeaturesSection() {
    return (
        <section className="py-24 relative overflow-hidden">
            {/* Background */}
            <div className="absolute inset-0 bg-white dark:bg-gray-900 -z-10" />
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-6xl h-px bg-gradient-to-r from-transparent via-purple-500/20 to-transparent" />

            <div className="section-container">
                {/* Header */}
                <div className="text-center max-w-3xl mx-auto mb-16">
                    <motion.span
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-sm font-medium mb-6"
                    >
                        <Sparkles className="w-4 h-4" />
                        Beyond Auto-EDA
                    </motion.span>
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.1 }}
                        className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold mb-6"
                    >
                        Everything You Need to Make{" "}
                        <span className="gradient-text">the Right Decisions</span>
                    </motion.h2>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.2 }}
                        className="text-lg text-gray-600 dark:text-gray-400"
                    >
                        Kuya doesn't just analyze data — it tells you what to do next.
                        Think of it as having a senior analyst on your team.
                    </motion.p>
                </div>

                {/* Features Grid */}
                <motion.div
                    variants={container}
                    initial="hidden"
                    whileInView="show"
                    viewport={{ once: true }}
                    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                >
                    {features.map((feature, idx) => (
                        <motion.div key={idx} variants={item}>
                            <Card
                                glass
                                className="p-6 h-full group hover:border-purple-500/30 hover:shadow-glow transition-all duration-300"
                            >
                                <div
                                    className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}
                                >
                                    <feature.icon className="w-6 h-6 text-white" />
                                </div>
                                <h3 className="text-xl font-display font-semibold mb-2">
                                    {feature.title}
                                </h3>
                                <p className="text-gray-600 dark:text-gray-400">
                                    {feature.description}
                                </p>
                            </Card>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </section>
    );
}
