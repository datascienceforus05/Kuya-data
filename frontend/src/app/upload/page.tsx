"use client";

import React, { useState, useCallback, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { motion, AnimatePresence } from "framer-motion";
import {
    Upload,
    FileSpreadsheet,
    CheckCircle,
    XCircle,
    Loader2,
    Sparkles,
    Zap,
    BarChart3,
    PieChart,
    ScatterChart,
    Box,
    Wand2,
    Shield,
    Search,
    Brush,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

// Define available features
const AVAILABLE_FEATURES = [
    { id: "cleaning", name: "Data Cleaning", icon: Brush, description: "Auto missing values & type fixes" },
    { id: "eda", name: "Summary Stats", icon: BarChart3, description: "Mean, median, quartiles" },
    { id: "correlation", name: "Correlation", icon: PieChart, description: "Correlation matrix & heatmap" },
    { id: "distribution", name: "Distributions", icon: BarChart3, description: "Histograms with KDE" },
    { id: "boxplot", name: "Box Plots", icon: Box, description: "Outlier visualization" },
    { id: "bar", name: "Bar Charts", icon: BarChart3, description: "Categorical analysis" },
    { id: "pairplot", name: "Pair Plot", icon: ScatterChart, description: "All numeric pairs" },
    { id: "scatter", name: "Scatter Plots", icon: ScatterChart, description: "Correlated columns" },
    { id: "quality", name: "Quality Score", icon: Shield, description: "Data quality analysis" },
    { id: "outliers", name: "Outliers", icon: Search, description: "Outlier detection" },
    { id: "magic", name: "Magic Analysis", icon: Wand2, description: "AI recommendations" },
];

type UploadStatus = "idle" | "uploading" | "processing" | "success" | "error";

export default function UploadPage() {
    const router = useRouter();
    const { user, isAuthenticated } = useAuth();
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<UploadStatus>("idle");
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState<string | null>(null);
    const [isDragOver, setIsDragOver] = useState(false);
    const [selectedFeatures, setSelectedFeatures] = useState<string[]>(["all"]);
    const [selectAll, setSelectAll] = useState(true);

    // Toggle feature selection
    const toggleFeature = (featureId: string) => {
        if (selectAll) {
            // If "all" was selected, switch to individual selection
            setSelectAll(false);
            setSelectedFeatures([featureId]);
        } else {
            setSelectedFeatures((prev) => {
                if (prev.includes(featureId)) {
                    const newFeatures = prev.filter((f) => f !== featureId);
                    return newFeatures.length === 0 ? ["all"] : newFeatures;
                } else {
                    return [...prev, featureId];
                }
            });
        }
    };

    const toggleSelectAll = () => {
        if (selectAll) {
            setSelectAll(false);
            setSelectedFeatures([]);
        } else {
            setSelectAll(true);
            setSelectedFeatures(["all"]);
        }
    };

    // Handle file selection
    const handleFileSelect = useCallback((selectedFile: File) => {
        if (!isAuthenticated) {
            router.push("/login");
            return;
        }

        const validTypes = [
            "text/csv",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ];

        const extension = selectedFile.name.split(".").pop()?.toLowerCase();
        const isValidExtension = ["csv", "xls", "xlsx"].includes(extension || "");

        if (!validTypes.includes(selectedFile.type) && !isValidExtension) {
            setError("Please upload a CSV or Excel file");
            return;
        }

        if (selectedFile.size > 10 * 1024 * 1024) {
            setError("File size must be less than 10MB");
            return;
        }

        setFile(selectedFile);
        setError(null);
    }, [isAuthenticated, router]);

    // Handle drag and drop
    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragOver(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragOver(false);
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragOver(false);

        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            handleFileSelect(droppedFile);
        }
    }, [handleFileSelect]);

    // Handle file input change
    const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile) {
            handleFileSelect(selectedFile);
        }
    }, [handleFileSelect]);

    // Upload file
    const uploadFile = async () => {
        if (!file) return;

        setStatus("uploading");
        setProgress(0);
        setError(null);

        try {
            // Simulate progress
            const progressInterval = setInterval(() => {
                setProgress((prev) => {
                    if (prev >= 90) {
                        clearInterval(progressInterval);
                        return 90;
                    }
                    return prev + 10;
                });
            }, 200);

            const formData = new FormData();
            formData.append("file", file);
            formData.append("features", selectAll ? "all" : JSON.stringify(selectedFeatures));
            if (user?.email) {
                formData.append("email", user.email);
            }

            setStatus("processing");

            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/upload`,
                {
                    method: "POST",
                    body: formData,
                }
            );

            clearInterval(progressInterval);
            setProgress(100);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Upload failed");
            }

            const data = await response.json();

            // Store in sessionStorage for immediate access
            try {
                sessionStorage.setItem(`report-${data.reportId}`, JSON.stringify(data));
            } catch (e) {
                console.warn("Storage quota exceeded, skipping local cache:", e);
            }

            setStatus("success");

            // Redirect to results after brief delay
            setTimeout(() => {
                router.push(`/result?id=${data.reportId}`);
            }, 1000);

        } catch (err) {
            setStatus("error");
            setError(err instanceof Error ? err.message : "Upload failed");
        }
    };

    // Reset upload
    const resetUpload = () => {
        setFile(null);
        setStatus("idle");
        setProgress(0);
        setError(null);
    };

    return (
        <div className="min-h-screen pt-24 pb-16 relative">
            {/* Background */}
            <div className="absolute inset-0 -z-10">
                <div className="absolute inset-0 bg-gradient-to-b from-purple-50 via-white to-white dark:from-gray-900 dark:via-gray-900 dark:to-gray-900" />
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl" />
            </div>

            <div className="section-container">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center max-w-3xl mx-auto mb-12"
                >
                    <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-sm font-medium mb-6">
                        <Sparkles className="w-4 h-4" />
                        Kuya Data Analysis
                    </span>
                    <h1 className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold mb-6">
                        Upload Your{" "}
                        <span className="gradient-text">Data File</span>
                    </h1>
                    <p className="text-lg text-gray-600 dark:text-gray-400">
                        Drop your CSV or Excel file and select the analyses you want
                    </p>
                </motion.div>

                <div className="max-w-5xl mx-auto grid lg:grid-cols-2 gap-8">
                    {/* Upload Area */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1 }}
                    >
                        <Card glass className="p-8">
                            <h2 className="text-xl font-display font-semibold mb-6 flex items-center gap-2">
                                <Upload className="w-5 h-5 text-purple-600" />
                                Upload File
                            </h2>

                            {/* Drop Zone */}
                            <div
                                className={cn(
                                    "relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 cursor-pointer",
                                    isDragOver
                                        ? "border-purple-500 bg-purple-50 dark:bg-purple-900/20"
                                        : "border-gray-300 dark:border-gray-700 hover:border-purple-400",
                                    status === "success" && "border-green-500 bg-green-50 dark:bg-green-900/20",
                                    status === "error" && "border-red-500 bg-red-50 dark:bg-red-900/20"
                                )}
                                onDragOver={handleDragOver}
                                onDragLeave={handleDragLeave}
                                onDrop={handleDrop}
                                onClick={() => document.getElementById("file-input")?.click()}
                            >
                                <input
                                    id="file-input"
                                    type="file"
                                    accept=".csv,.xls,.xlsx"
                                    onChange={handleInputChange}
                                    className="hidden"
                                />

                                <AnimatePresence mode="wait">
                                    {status === "idle" && !file && (
                                        <motion.div
                                            key="idle"
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            exit={{ opacity: 0 }}
                                        >
                                            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                                                <FileSpreadsheet className="w-8 h-8 text-purple-600" />
                                            </div>
                                            <p className="text-lg font-medium mb-2">
                                                Drop your file here or click to browse
                                            </p>
                                            <p className="text-sm text-gray-500">
                                                Supports CSV, XLS, XLSX (max 10MB)
                                            </p>
                                        </motion.div>
                                    )}

                                    {file && status === "idle" && (
                                        <motion.div
                                            key="file-selected"
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            exit={{ opacity: 0 }}
                                        >
                                            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                                                <CheckCircle className="w-8 h-8 text-green-600" />
                                            </div>
                                            <p className="text-lg font-medium mb-1">{file.name}</p>
                                            <p className="text-sm text-gray-500">
                                                {(file.size / 1024).toFixed(1)} KB
                                            </p>
                                        </motion.div>
                                    )}

                                    {(status === "uploading" || status === "processing") && (
                                        <motion.div
                                            key="uploading"
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            exit={{ opacity: 0 }}
                                        >
                                            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                                                <Loader2 className="w-8 h-8 text-purple-600 animate-spin" />
                                            </div>
                                            <p className="text-lg font-medium mb-2">
                                                {status === "uploading" ? "Uploading..." : "Analyzing with Kuya..."}
                                            </p>
                                            <div className="w-full max-w-xs mx-auto bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                                                <div
                                                    className="bg-gradient-to-r from-purple-600 to-indigo-600 h-2 rounded-full transition-all duration-300"
                                                    style={{ width: `${progress}%` }}
                                                />
                                            </div>
                                        </motion.div>
                                    )}

                                    {status === "success" && (
                                        <motion.div
                                            key="success"
                                            initial={{ opacity: 0, scale: 0.9 }}
                                            animate={{ opacity: 1, scale: 1 }}
                                            exit={{ opacity: 0 }}
                                        >
                                            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                                                <CheckCircle className="w-8 h-8 text-green-600" />
                                            </div>
                                            <p className="text-lg font-medium text-green-600">
                                                Analysis Complete!
                                            </p>
                                            <p className="text-sm text-gray-500">
                                                Redirecting to results...
                                            </p>
                                        </motion.div>
                                    )}

                                    {status === "error" && (
                                        <motion.div
                                            key="error"
                                            initial={{ opacity: 0, scale: 0.9 }}
                                            animate={{ opacity: 1, scale: 1 }}
                                            exit={{ opacity: 0 }}
                                        >
                                            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
                                                <XCircle className="w-8 h-8 text-red-600" />
                                            </div>
                                            <p className="text-lg font-medium text-red-600 mb-1">
                                                Upload Failed
                                            </p>
                                            <p className="text-sm text-red-500">{error}</p>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>

                            {/* Action Buttons */}
                            <div className="mt-6 flex gap-4">
                                {status === "idle" && file && (
                                    <>
                                        <Button
                                            size="lg"
                                            className="flex-1"
                                            onClick={uploadFile}
                                        >
                                            <Zap className="w-4 h-4 mr-2" />
                                            Analyze Now
                                        </Button>
                                        <Button
                                            variant="outline"
                                            size="lg"
                                            onClick={resetUpload}
                                        >
                                            Change File
                                        </Button>
                                    </>
                                )}

                                {status === "error" && (
                                    <Button
                                        size="lg"
                                        className="w-full"
                                        onClick={resetUpload}
                                    >
                                        Try Again
                                    </Button>
                                )}
                            </div>
                        </Card>
                    </motion.div>

                    {/* Feature Selection */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <Card glass className="p-8">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-xl font-display font-semibold flex items-center gap-2">
                                    <Wand2 className="w-5 h-5 text-purple-600" />
                                    Select Features
                                </h2>
                                <Button
                                    variant={selectAll ? "default" : "outline"}
                                    size="sm"
                                    onClick={toggleSelectAll}
                                >
                                    {selectAll ? "Select Individual" : "Select All"}
                                </Button>
                            </div>

                            <div className="grid grid-cols-2 gap-3">
                                {AVAILABLE_FEATURES.map((feature) => {
                                    const isSelected = selectAll || selectedFeatures.includes(feature.id);
                                    const Icon = feature.icon;

                                    return (
                                        <motion.button
                                            key={feature.id}
                                            whileHover={{ scale: 1.02 }}
                                            whileTap={{ scale: 0.98 }}
                                            onClick={() => toggleFeature(feature.id)}
                                            className={cn(
                                                "p-3 rounded-xl border text-left transition-all duration-200",
                                                isSelected
                                                    ? "border-purple-500 bg-purple-50 dark:bg-purple-900/20"
                                                    : "border-gray-200 dark:border-gray-700 hover:border-purple-300"
                                            )}
                                        >
                                            <div className="flex items-center gap-2 mb-1">
                                                <Icon className={cn(
                                                    "w-4 h-4",
                                                    isSelected ? "text-purple-600" : "text-gray-400"
                                                )} />
                                                <span className={cn(
                                                    "font-medium text-sm",
                                                    isSelected ? "text-purple-700 dark:text-purple-300" : "text-gray-600 dark:text-gray-400"
                                                )}>
                                                    {feature.name}
                                                </span>
                                            </div>
                                            <p className="text-xs text-gray-500 dark:text-gray-500">
                                                {feature.description}
                                            </p>
                                        </motion.button>
                                    );
                                })}
                            </div>

                            <div className="mt-6 p-4 rounded-xl bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/20 dark:to-indigo-900/20">
                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                    <strong className="text-purple-600">Tip:</strong> Select &quot;All&quot; for comprehensive analysis or pick specific features for faster processing.
                                </p>
                            </div>
                        </Card>
                    </motion.div>
                </div>

                {/* Features Overview */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="mt-12 max-w-5xl mx-auto"
                >
                    <h2 className="text-2xl font-display font-bold text-center mb-8">
                        Powered by <span className="gradient-text">Kuya Data</span>
                    </h2>
                    <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        {[
                            { icon: Brush, title: "Smart Cleaning", desc: "Auto-fix missing values, types, outliers" },
                            { icon: BarChart3, title: "Deep EDA", desc: "Stats, distributions, correlations" },
                            { icon: ScatterChart, title: "Visualizations", desc: "Charts, plots, heatmaps" },
                            { icon: Wand2, title: "Magic Insights", desc: "AI-powered recommendations" },
                        ].map((item, idx) => (
                            <Card key={idx} glass className="p-4 text-center">
                                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center mx-auto mb-3">
                                    <item.icon className="w-5 h-5 text-white" />
                                </div>
                                <h3 className="font-semibold mb-1">{item.title}</h3>
                                <p className="text-sm text-gray-500">{item.desc}</p>
                            </Card>
                        ))}
                    </div>
                </motion.div>
            </div>
        </div>
    );
}
