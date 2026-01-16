"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
    Wand2,
    ArrowRight,
    Check,
    Sparkles,
    Upload,
    BarChart3,
    FileCheck,
    Download,
    Zap,
    Shield,
    Brain,
    Layers,
    Target,
    TrendingUp,
    Clock,
    Users,
    ChevronRight,
    FlaskConical,
    Briefcase,
    GraduationCap,
    Rocket,
    LineChart
} from "lucide-react";
import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// Animation Variants
const fadeUp = {
    hidden: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
};

const staggerContainer = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.15 } }
};

export function HowItWorksSection() {
    const steps = [
        {
            icon: Upload,
            title: "Upload Your Data",
            desc: "Drag and drop your CSV or Excel file. We support files up to 100MB with millions of rows.",
            color: "from-purple-500 to-indigo-500"
        },
        {
            icon: Wand2,
            title: "Magic Happens",
            desc: "Our AI engine cleans your data, detects patterns, fixes missing values, and runs complete EDA.",
            color: "from-indigo-500 to-blue-500"
        },
        {
            icon: BarChart3,
            title: "View Insights",
            desc: "Explore interactive charts, heatmaps, distributions, and AI-powered recommendations.",
            color: "from-blue-500 to-cyan-500"
        },
        {
            icon: Download,
            title: "Export Results",
            desc: "Download professional PDF reports, cleaned datasets, and share with your team instantly.",
            color: "from-cyan-500 to-teal-500"
        },
    ];

    return (
        <section className="py-28 bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-950 relative overflow-hidden">
            <div className="absolute inset-0 opacity-30">
                <div className="absolute top-1/2 left-1/4 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl" />
                <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl" />
            </div>

            <div className="section-container relative z-10">
                <motion.div
                    className="text-center mb-20"
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true }}
                    variants={fadeUp}
                >
                    <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 text-sm font-medium mb-6">
                        <Clock className="w-4 h-4" />
                        Get Started in 60 Seconds
                    </span>
                    <h2 className="text-4xl lg:text-5xl font-display font-bold mb-4">
                        How <span className="gradient-text">Kuya Cloud</span> Works
                    </h2>
                    <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                        From raw messy data to professional analysis in just 4 simple steps. No coding required.
                    </p>
                </motion.div>

                <motion.div
                    className="grid md:grid-cols-2 lg:grid-cols-4 gap-8"
                    variants={staggerContainer}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true }}
                >
                    {steps.map((step, idx) => (
                        <motion.div key={idx} variants={fadeUp}>
                            <Card className="p-6 h-full bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-gray-200 dark:border-gray-700 group hover:scale-105 hover:shadow-2xl transition-all duration-500">
                                <div className="relative mb-6">
                                    <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${step.color} flex items-center justify-center shadow-lg group-hover:scale-110 group-hover:rotate-3 transition-all duration-300`}>
                                        <step.icon className="w-7 h-7 text-white" />
                                    </div>
                                    <span className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-purple-600 text-white font-bold text-sm flex items-center justify-center shadow-lg">
                                        {idx + 1}
                                    </span>
                                </div>
                                <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                                <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">{step.desc}</p>
                            </Card>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </section>
    );
}

export function TrustedBySection() {
    const [hoveredIdx, setHoveredIdx] = useState<number | null>(null);

    const professionals = [
        {
            name: "Data Scientists",
            icon: FlaskConical,
            preview: "Skip tedious data cleaning. Get ML-ready datasets with automated feature engineering, outlier detection, and quality scoring.",
            color: "purple"
        },
        {
            name: "Business Analysts",
            icon: Briefcase,
            preview: "Generate beautiful charts and PDF reports in seconds. Impress stakeholders with professional visualizations.",
            color: "blue"
        },
        {
            name: "Researchers",
            icon: Brain,
            preview: "Transform survey and experimental data into publication-ready analysis. Statistical summaries made easy.",
            color: "indigo"
        },
        {
            name: "Students",
            icon: GraduationCap,
            preview: "Learn data analysis by doing. Perfect for assignments, thesis projects, and building your portfolio.",
            color: "teal"
        },
        {
            name: "Startups",
            icon: Rocket,
            preview: "Make data-driven decisions without hiring a data team. Affordable insights for growing businesses.",
            color: "orange"
        },
    ];

    return (
        <section className="py-20 bg-white dark:bg-gray-950 border-y border-gray-100 dark:border-gray-800">
            <div className="section-container">
                <motion.div
                    className="text-center"
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    viewport={{ once: true }}
                >
                    <p className="text-sm text-gray-500 uppercase tracking-widest mb-12">Trusted by data professionals worldwide</p>
                    <div className="flex flex-wrap justify-center items-start gap-6 md:gap-10">
                        {professionals.map((prof, idx) => (
                            <div
                                key={idx}
                                className="relative cursor-pointer"
                                onMouseEnter={() => setHoveredIdx(idx)}
                                onMouseLeave={() => setHoveredIdx(null)}
                            >
                                <motion.div
                                    className={`flex items-center gap-2 px-4 py-2 rounded-xl transition-all duration-300 ${hoveredIdx === idx
                                            ? 'bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400'
                                            : 'text-gray-400 hover:text-gray-600'
                                        }`}
                                    whileHover={{ scale: 1.05 }}
                                >
                                    <prof.icon className="w-5 h-5" />
                                    <span className="text-lg font-display font-bold">{prof.name}</span>
                                </motion.div>

                                <AnimatePresence>
                                    {hoveredIdx === idx && (
                                        <motion.div
                                            initial={{ opacity: 0, y: -10, height: 0 }}
                                            animate={{ opacity: 1, y: 0, height: 'auto' }}
                                            exit={{ opacity: 0, y: -10, height: 0 }}
                                            transition={{ duration: 0.3 }}
                                            className="absolute left-1/2 -translate-x-1/2 mt-3 w-72 z-50"
                                        >
                                            <div className="p-4 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-purple-100 dark:border-purple-800/30">
                                                <div className="flex items-start gap-3">
                                                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center flex-shrink-0">
                                                        <prof.icon className="w-5 h-5 text-white" />
                                                    </div>
                                                    <div>
                                                        <p className="text-sm font-medium text-gray-900 dark:text-white mb-1">{prof.name}</p>
                                                        <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">{prof.preview}</p>
                                                    </div>
                                                </div>
                                                <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-white dark:bg-gray-800 border-l border-t border-purple-100 dark:border-purple-800/30 rotate-45" />
                                            </div>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        ))}
                    </div>
                </motion.div>
            </div>
        </section>
    );
}

export function UseCasesSection() {
    const useCases = [
        {
            title: "Data Scientists",
            desc: "Skip hours of tedious cleaning. Go straight to modeling with pre-processed datasets.",
            bullets: ["Auto feature engineering", "ML readiness reports", "Outlier analysis"],
            color: "purple"
        },
        {
            title: "Business Analysts",
            desc: "Generate professional reports in seconds. Impress stakeholders with beautiful charts.",
            bullets: ["One-click PDF exports", "Executive summaries", "Interactive visuals"],
            color: "indigo"
        },
        {
            title: "Researchers & Students",
            desc: "Turn raw survey data into publication-ready analysis without writing code.",
            bullets: ["Statistical summaries", "Distribution plots", "Correlation heatmaps"],
            color: "blue"
        },
    ];

    return (
        <section className="py-28 bg-gradient-to-b from-white to-purple-50 dark:from-gray-950 dark:to-gray-900 relative overflow-hidden">
            <div className="absolute inset-0 opacity-20">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-purple-500/10 rounded-full blur-3xl" />
                <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-indigo-500/10 rounded-full blur-3xl" />
            </div>

            <div className="section-container relative z-10">
                <motion.div
                    className="text-center mb-20"
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true }}
                    variants={fadeUp}
                >
                    <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-sm font-medium mb-6">
                        <Users className="w-4 h-4" />
                        Built For Everyone
                    </span>
                    <h2 className="text-4xl lg:text-5xl font-display font-bold mb-4">
                        Who Uses <span className="gradient-text">Kuya Cloud</span>?
                    </h2>
                </motion.div>

                <motion.div
                    className="grid md:grid-cols-3 gap-8"
                    variants={staggerContainer}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true }}
                >
                    {useCases.map((useCase, idx) => (
                        <motion.div key={idx} variants={fadeUp}>
                            <Card className={`p-8 h-full bg-white dark:bg-gray-800 border-t-4 border-t-${useCase.color}-500 hover:shadow-2xl transition-all duration-300 group`}>
                                <h3 className="text-2xl font-bold mb-4 group-hover:text-purple-600 transition-colors">{useCase.title}</h3>
                                <p className="text-gray-600 dark:text-gray-400 mb-6">{useCase.desc}</p>
                                <ul className="space-y-3">
                                    {useCase.bullets.map((bullet, i) => (
                                        <li key={i} className="flex items-center gap-3 text-sm">
                                            <div className={`w-5 h-5 rounded-full bg-${useCase.color}-100 dark:bg-${useCase.color}-900/30 flex items-center justify-center`}>
                                                <Check className={`w-3 h-3 text-${useCase.color}-600`} />
                                            </div>
                                            {bullet}
                                        </li>
                                    ))}
                                </ul>
                            </Card>
                        </motion.div>
                    ))}
                </motion.div>
            </div>
        </section>
    );
}

export function CTASection() {
    return (
        <section className="py-28 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-600 via-indigo-600 to-blue-600" />
            <div className="absolute inset-0 opacity-30" style={{ backgroundImage: "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")" }} />

            <div className="section-container relative z-10">
                <motion.div
                    className="text-center max-w-3xl mx-auto"
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true }}
                    variants={fadeUp}
                >
                    <h2 className="text-4xl lg:text-5xl font-display font-bold text-white mb-6">
                        Ready to Transform Your Data?
                    </h2>
                    <p className="text-xl text-white/80 mb-10">
                        Join thousands of analysts, scientists, and students who save hours every week with automated data analysis.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Link href="/upload">
                            <Button size="xl" className="bg-white text-purple-600 hover:bg-gray-100 shadow-2xl group px-8">
                                Start Free Analysis
                                <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" />
                            </Button>
                        </Link>
                        <Link href="/pricing">
                            <Button size="xl" className="bg-white/20 border-2 border-white text-white hover:bg-white hover:text-purple-600 transition-all px-8">
                                View Plans
                            </Button>
                        </Link>
                    </div>

                    <motion.div
                        className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8"
                        variants={staggerContainer}
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                    >
                        {[
                            { value: "50K+", label: "Files Analyzed" },
                            { value: "99.9%", label: "Uptime" },
                            { value: "5 sec", label: "Avg Speed" },
                            { value: "Free", label: "To Start" }
                        ].map((stat, idx) => (
                            <motion.div key={idx} variants={fadeUp} className="text-center">
                                <div className="text-3xl font-bold text-white mb-1">{stat.value}</div>
                                <div className="text-sm text-white/60">{stat.label}</div>
                            </motion.div>
                        ))}
                    </motion.div>
                </motion.div>
            </div>
        </section>
    );
}
