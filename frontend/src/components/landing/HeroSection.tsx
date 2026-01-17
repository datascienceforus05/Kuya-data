"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

export function HeroSection() {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
            {/* Animated Background */}
            <div className="absolute inset-0 -z-10">
                <div className="absolute inset-0 bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-purple-900/20 dark:to-gray-900" />

                {/* Floating Orbs */}
                <motion.div
                    animate={{
                        scale: [1, 1.2, 1],
                        opacity: [0.3, 0.5, 0.3],
                    }}
                    transition={{
                        duration: 8,
                        repeat: Infinity,
                        ease: "easeInOut",
                    }}
                    className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"
                />
                <motion.div
                    animate={{
                        scale: [1.2, 1, 1.2],
                        opacity: [0.3, 0.5, 0.3],
                    }}
                    transition={{
                        duration: 10,
                        repeat: Infinity,
                        ease: "easeInOut",
                    }}
                    className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl"
                />
                <motion.div
                    animate={{
                        scale: [1, 1.3, 1],
                        opacity: [0.2, 0.4, 0.2],
                    }}
                    transition={{
                        duration: 12,
                        repeat: Infinity,
                        ease: "easeInOut",
                    }}
                    className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-pink-500/10 rounded-full blur-3xl"
                />

                {/* Grid Pattern */}
                <div
                    className="absolute inset-0 opacity-[0.02] dark:opacity-[0.05]"
                    style={{
                        backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.4'%3E%3Ccircle cx='30' cy='30' r='1.5'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
                    }}
                />
            </div>

            <div className="section-container">
                <div className="max-w-4xl mx-auto text-center">
                    {/* Badge */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                    >
                        <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-sm font-medium mb-8">
                            <Sparkles className="w-4 h-4" />
                            AI-Powered Data Decision Assistant
                        </span>
                    </motion.div>

                    {/* Heading */}
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                        className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-display font-bold tracking-tight mb-6"
                    >
                        Think Like a Senior Data Analyst{" "}
                        <span className="relative">
                            <span className="relative z-10 gradient-text">Instantly</span>
                            <motion.span
                                initial={{ width: "0%" }}
                                animate={{ width: "100%" }}
                                transition={{ duration: 0.8, delay: 0.5 }}
                                className="absolute bottom-2 left-0 h-3 bg-purple-200 dark:bg-purple-800/50 -z-10 rounded"
                            />
                        </span>
                    </motion.h1>

                    {/* Description */}
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="text-lg sm:text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-10"
                    >
                        Upload your data and get clear recommendations, risk warnings, and ML-ready insights
                        — explained in plain English. No code required.
                    </motion.p>

                    {/* CTA Buttons */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.3 }}
                        className="flex flex-col sm:flex-row items-center justify-center gap-4"
                    >
                        <Link href="/upload">
                            <Button size="xl" className="group">
                                Analyze My Data
                                <ArrowRight className="ml-2 w-5 h-5 transition-transform group-hover:translate-x-1" />
                            </Button>
                        </Link>
                        <Link href="/pricing">
                            <Button variant="glass" size="xl">
                                View Pricing
                            </Button>
                        </Link>
                    </motion.div>

                    {/* Stats */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.4 }}
                        className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto"
                    >
                        {[
                            { value: "10K+", label: "Analyses Completed" },
                            { value: "5hrs", label: "Saved Per Week" },
                            { value: "3", label: "Tiers for Everyone" },
                            { value: "4.9\u2605", label: "User Rating" },
                        ].map((stat, idx) => (
                            <div key={idx} className="text-center">
                                <div className="text-2xl sm:text-3xl font-display font-bold gradient-text">
                                    {stat.value}
                                </div>
                                <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                                    {stat.label}
                                </div>
                            </div>
                        ))}
                    </motion.div>
                </div>

                {/* Dashboard Preview */}
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.7, delay: 0.5 }}
                    className="mt-20 relative"
                >
                    <div className="relative mx-auto max-w-5xl">
                        {/* Glow Effect */}
                        <div className="absolute -inset-4 bg-gradient-to-r from-purple-500 via-indigo-500 to-pink-500 rounded-3xl blur-2xl opacity-20" />

                        {/* Dashboard Image Container */}
                        <div className="relative bg-white dark:bg-gray-900 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                            {/* Browser Header */}
                            <div className="flex items-center gap-2 px-4 py-3 bg-gray-100 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
                                <div className="flex gap-2">
                                    <div className="w-3 h-3 rounded-full bg-red-400" />
                                    <div className="w-3 h-3 rounded-full bg-yellow-400" />
                                    <div className="w-3 h-3 rounded-full bg-green-400" />
                                </div>
                                <div className="flex-1 flex justify-center">
                                    <div className="px-4 py-1 rounded-lg bg-white dark:bg-gray-700 text-xs text-gray-500 dark:text-gray-400">
                                        app.kuyacloud.com/result
                                    </div>
                                </div>
                            </div>

                            {/* Dashboard Content Mockup */}
                            <div className="p-6 bg-gray-50 dark:bg-gray-900/50 min-h-[400px]">
                                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                                    {/* Stats Cards */}
                                    <div className="p-4 rounded-xl bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700">
                                        <p className="text-xs text-gray-500 mb-1">Total Rows</p>
                                        <p className="text-2xl font-bold text-gray-900 dark:text-white">12,458</p>
                                    </div>
                                    <div className="p-4 rounded-xl bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700">
                                        <p className="text-xs text-gray-500 mb-1">Missing Values</p>
                                        <p className="text-2xl font-bold text-amber-600">23</p>
                                    </div>
                                    <div className="p-4 rounded-xl bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700">
                                        <p className="text-xs text-gray-500 mb-1">Columns</p>
                                        <p className="text-2xl font-bold text-gray-900 dark:text-white">15</p>
                                    </div>
                                    <div className="p-4 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 shadow-sm">
                                        <p className="text-xs text-white/80 mb-1">ML Ready</p>
                                        <p className="text-2xl font-bold text-white">92%</p>
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    {/* Bar Chart Visual */}
                                    <div className="p-4 rounded-xl bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700">
                                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">Distribution Analysis</p>
                                        <div className="flex items-end gap-2 h-32">
                                            {[65, 85, 45, 90, 70, 55, 80, 60, 75, 95].map((h, i) => (
                                                <motion.div
                                                    key={i}
                                                    className="flex-1 bg-gradient-to-t from-purple-600 to-indigo-400 rounded-t-sm"
                                                    initial={{ height: 0 }}
                                                    animate={{ height: `${h}%` }}
                                                    transition={{ delay: 0.5 + i * 0.05, duration: 0.5 }}
                                                />
                                            ))}
                                        </div>
                                    </div>

                                    {/* Correlation Heatmap Visual */}
                                    <div className="p-4 rounded-xl bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700">
                                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">Correlation Heatmap</p>
                                        <div className="grid grid-cols-5 gap-1 h-32">
                                            {Array.from({ length: 25 }).map((_, i) => {
                                                const colors = ["bg-purple-200", "bg-purple-400", "bg-purple-600", "bg-indigo-300", "bg-indigo-500", "bg-blue-400", "bg-pink-300"];
                                                return (
                                                    <motion.div
                                                        key={i}
                                                        className={`rounded-sm ${colors[i % colors.length]}`}
                                                        initial={{ opacity: 0 }}
                                                        animate={{ opacity: 1 }}
                                                        transition={{ delay: 0.8 + i * 0.02 }}
                                                    />
                                                );
                                            })}
                                        </div>
                                    </div>
                                </div>

                                {/* AI Recommendation Bar */}
                                <div className="mt-4 p-4 rounded-xl bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/20 dark:to-indigo-900/20 border border-purple-100 dark:border-purple-800/30">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center">
                                            <Sparkles className="w-4 h-4 text-white" />
                                        </div>
                                        <div>
                                            <p className="text-sm font-medium text-purple-800 dark:text-purple-300">AI Recommendation</p>
                                            <p className="text-xs text-purple-600 dark:text-purple-400">Apply StandardScaler to 'Age' and 'Income' columns for better model performance</p>
                                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 italic">Why: Improves linear models; tree-based models unaffected.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </div>
        </section>
    );
}
