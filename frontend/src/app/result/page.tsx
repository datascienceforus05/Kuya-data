"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
    BarChart3,
    Lock,
    Loader2,
    Download,
    FileText,
    Table,
    Lightbulb,
    AlertTriangle,
    CheckCircle,
    Info,
    Shield,
    Sparkles,
    FileSpreadsheet,
    Code,
    Globe,
    Copy,
    Zap,
    Target,
    Settings2,
    X,
    Brush,
    PieChart,
    ScatterChart,
    Box,
    Wand2,
    Search
} from "lucide-react";
import { ChartDisplay } from "@/components/result/ChartDisplay";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../components/ui/select";

// Define available features (Same as upload page)
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
    { id: "insights", name: "Automated Insights", icon: Sparkles, description: "Key trends & patterns" },
    { id: "magic", name: "Magic Analysis", icon: Wand2, description: "AI recommendations" },
];

interface ReportData {
    success: boolean;
    reportId: string;
    fileName?: string;
    summary: {
        rows: number;
        columns: number;
        numericColumns: string[];
        categoricalColumns?: string[];
        datetimeColumns?: string[];
        missingValues: Record<string, number>;
        missingByColumn?: Record<string, number>;
        totalMissing?: number;
        missingPercentage?: number;
        statistics?: Record<string, any>;
        categoricalStats?: Record<string, any>;
    };
    correlation: Record<string, Record<string, number>>;
    graphs: Array<{ type: string; title: string; image: string; tier?: string }>;
    cleanedDataHead: Array<Record<string, any>>;
    insights: string[];
    qualityScore?: {
        overall_score: number;
        grade: string;
        status: string;
        details: {
            completeness: number;
            uniqueness: number;
            consistency: number;
            validity: number;
        };
    };
    health?: {
        size: { rows: number; columns: number; memory_mb: number };
        completeness: { total_missing: number; complete_rows: number };
        duplicates: { count: number; percentage: number };
        overall_health: number;
    };
    cleaningReport?: {
        operations: string[];
        total_operations: number;
        original_shape: [number, number];
        final_shape: [number, number];
    };
    columnMapping?: Record<string, string>;
    columnTypes?: {
        numeric: any[];
        categorical: any[];
        datetime: any[];
        boolean: any[];
    };
    outliers?: Record<string, number>;
    duplicates?: {
        total_duplicates: number;
        duplicate_percentage: number;
    };
    featureImportance?: Record<string, number>;
    recommendations?: Array<{
        type: string;
        title: string;
        description: string;
        action?: string;
    }>;
    selectedFeatures?: string[];
    // 🔥 THE 5 UNIQUE PILLARS
    columnAnalysis?: Record<string, {
        type: string;
        importance: string;
        action: string;
        reason: string;
        unique_values: number;
        missing: number;
        missing_pct: number;
        outliers: number;
        quality_score: number;
        issues: string[];
    }>;
    healthScore?: {
        score: number;
        grade: string;
        status: string;
        color: string;
        breakdown: Record<string, { score: number; max: number; label: string }>;
        issues: { missing_cells: number; duplicate_rows: number; total_columns: number; numeric_columns: number };
    };
    engineeringSuggestions?: Array<{
        column: string;
        action: string;
        method: string;
        reason: string;
        priority: string;
        icon: string;
    }>;
    mlReadiness?: {
        score: number;
        verdict: string;
        verdict_color: string;
        checks: Array<{ check: string; status: string; message: string }>;
        recommended_models: Array<{ name: string; reason: string }>;
    };
    targetAnalysis?: {
        target_column?: string;
        task_type?: string;
        target_stats?: Record<string, number>;
        feature_correlations?: Record<string, number>;
        leakage_warnings?: Array<{ column: string; correlation: number; warning: string }>;
        class_distribution?: Record<string, number>;
        feature_importance_estimate?: Record<string, { correlation: number; importance: string }>;
        imbalance_warning?: string;
        target_warning?: string;
    };
}

function ResultContent() {
    const searchParams = useSearchParams();
    const reportId = searchParams.get("id");
    const { data: session } = useSession();
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState<ReportData | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState("overview");
    const [userPlan, setUserPlan] = useState<string>("free");

    // Fetch user plan
    useEffect(() => {
        if (session?.user?.email) {
            fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/user/${encodeURIComponent(session.user.email)}`)
                .then(res => res.json())
                .then(u => { if (u.plan) setUserPlan(u.plan); })
                .catch(err => console.error(err));
        }
    }, [session]);
    const [exporting, setExporting] = useState<string | null>(null);

    // Re-analysis state
    const [showCustomize, setShowCustomize] = useState(false);
    const [selectedFeatures, setSelectedFeatures] = useState<string[]>([]);
    const [reanalyzing, setReanalyzing] = useState(false);

    useEffect(() => {
        if (!reportId) {
            setError("No report ID provided");
            setLoading(false);
            return;
        }

        const storedData = sessionStorage.getItem(`report-${reportId}`);
        if (storedData) {
            try {
                setData(JSON.parse(storedData));
                setLoading(false);
                return;
            } catch {
                // Continue to fetch
            }
        }

        const fetchReport = async () => {
            try {
                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/report/${reportId}/data`
                );
                if (!response.ok) throw new Error("Failed to fetch report");
                const reportData = await response.json();
                setData(reportData);
                if (reportData.selectedFeatures && Array.isArray(reportData.selectedFeatures)) {
                    setSelectedFeatures(reportData.selectedFeatures);
                }
            } catch (err) {
                console.error("Error fetching report:", err);
                setError("Failed to load report. Please try uploading again.");
            } finally {
                setLoading(false);
            }
        };

        fetchReport();
    }, [reportId]);

    const handleExport = async (format: string) => {
        setExporting(format);
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/report/${reportId}/export/${format}`;
            window.open(url, "_blank");
        } catch (err) {
            console.error(`Export error:`, err);
        }
        setTimeout(() => setExporting(null), 1000);
    };

    const toggleFeature = (featureId: string) => {
        setSelectedFeatures((prev) => {
            if (prev.includes(featureId)) {
                return prev.filter((f) => f !== featureId);
            } else {
                return [...prev, featureId];
            }
        });
    };

    const [customizeError, setCustomizeError] = useState<string | null>(null);
    const [rowsLimit, setRowsLimit] = useState("20");

    const executeReanalysis = async (featuresToRun: string[]) => {
        if (featuresToRun.length === 0) return;
        setReanalyzing(true);
        setCustomizeError(null);
        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/report/${reportId}/reanalyze`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ features: featuresToRun }),
                }
            );

            if (response.status === 404) {
                throw new Error("Original file not found. Please upload your file again to use this feature.");
            }

            if (!response.ok) throw new Error("Re-analysis failed");
            const newData = await response.json();

            // Merge with existing data
            setData((prev) => ({ ...prev, ...newData }));
            try {
                sessionStorage.setItem(`report-${reportId}`, JSON.stringify(newData));
            } catch (e) {
                console.warn("Cache quota exceeded", e);
            }
            setShowCustomize(false);

            // Update selected features state to match result
            if (newData.selectedFeatures) setSelectedFeatures(newData.selectedFeatures);

        } catch (err: any) {
            console.error("Re-analysis error:", err);
            setCustomizeError(err.message || "Failed to update analysis");
        } finally {
            setReanalyzing(false);
        }
    };

    const handleReanalyze = () => executeReanalysis(selectedFeatures);

    const handleRemoveFeature = (featureId: string) => {
        if (!data?.selectedFeatures) return;
        const newFeatures = data.selectedFeatures.filter(f => f !== featureId);
        executeReanalysis(newFeatures);
    };

    if (loading) {
        return (
            <div className="min-h-screen pt-24 flex items-center justify-center">
                <div className="text-center">
                    <Loader2 className="w-12 h-12 animate-spin text-purple-600 mx-auto mb-4" />
                    <p className="text-lg text-gray-600 dark:text-gray-400">Loading your analysis...</p>
                </div>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="min-h-screen pt-24 flex items-center justify-center">
                <Card glass className="p-8 text-center max-w-md">
                    <AlertTriangle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
                    <h2 className="text-xl font-bold mb-2">Report Not Found</h2>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">{error}</p>
                    <Button onClick={() => window.location.href = "/upload"}>Upload New File</Button>
                </Card>
            </div>
        );
    }

    const tabs = [
        { id: "overview", label: "Overview", icon: BarChart3 },
        { id: "intelligence", label: "Intelligence", icon: Sparkles },
        { id: "engineering", label: "Engineering", icon: Zap },
        { id: "charts", label: "Charts", icon: PieChart },
        { id: "insights", label: "AI Insights", icon: Lightbulb },
        { id: "data", label: "Data", icon: Table },
        { id: "export", label: "Export", icon: Download },
    ];

    return (
        <div className="min-h-screen pt-24 pb-16 relative">
            <div className="absolute inset-0 -z-10">
                <div className="absolute inset-0 bg-gradient-to-b from-purple-50 via-white to-white dark:from-gray-900 dark:via-gray-900 dark:to-gray-900" />
            </div>

            <div className="section-container">
                {/* Header */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8 relative">
                    <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-sm font-medium mb-4">
                        <CheckCircle className="w-4 h-4" />
                        Analysis Complete
                    </span>
                    <h1 className="text-3xl sm:text-4xl font-display font-bold mb-2">
                        Your Data <span className="gradient-text">Insights</span>
                    </h1>
                    <p className="text-gray-600 dark:text-gray-400 mb-6">{data.fileName || `Report ID: ${reportId}`}</p>

                    <Button
                        onClick={() => {
                            setSelectedFeatures([]); // Start fresh or predefined? 'all' might be safer
                            setShowCustomize(true);
                        }}
                        className="gap-2"
                        variant="outline"
                    >
                        <Settings2 className="w-4 h-4" />
                        Customize Analysis
                    </Button>
                </motion.div>

                {/* Customize Modal */}
                {showCustomize && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-sm">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="w-full max-w-2xl max-h-[90vh] overflow-y-auto"
                        >
                            <Card className="p-6 bg-white dark:bg-gray-900 relative">
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="absolute top-2 right-2"
                                    onClick={() => setShowCustomize(false)}
                                >
                                    <X className="w-4 h-4" />
                                </Button>

                                <h2 className="text-2xl font-bold mb-6">Select Features</h2>

                                {customizeError && (
                                    <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg text-sm flex items-center gap-2">
                                        <AlertTriangle className="w-4 h-4" />
                                        {customizeError}
                                    </div>
                                )}

                                <div className="grid grid-cols-2 gap-3 mb-8">
                                    {AVAILABLE_FEATURES.map((feature) => {
                                        const isSelected = selectedFeatures.includes(feature.id);
                                        const Icon = feature.icon;
                                        const isPreSelected = (data.selectedFeatures || []).includes(feature.id);
                                        return (
                                            <button
                                                key={feature.id}
                                                onClick={() => !isPreSelected && toggleFeature(feature.id)}
                                                disabled={isPreSelected}
                                                className={cn(
                                                    "p-3 rounded-xl border text-left transition-all duration-200 flex items-center gap-3",
                                                    isSelected
                                                        ? "border-purple-500 bg-purple-50 dark:bg-purple-900/20"
                                                        : "border-gray-200 dark:border-gray-700 hover:border-purple-300",
                                                    isPreSelected && "opacity-60 cursor-not-allowed ring-0 hover:border-purple-500/50"
                                                )}
                                            >
                                                <div className={cn("p-2 rounded-lg", isSelected ? "bg-purple-100 text-purple-600" : "bg-gray-100 text-gray-500")}>
                                                    <Icon className="w-4 h-4" />
                                                </div>
                                                <div>
                                                    <div className={cn("font-medium text-sm", isSelected ? "text-purple-700 dark:text-purple-300" : "text-gray-700 dark:text-gray-300")}>
                                                        {feature.name}
                                                    </div>
                                                    <div className="text-xs text-gray-400 line-clamp-1">{feature.description}</div>
                                                </div>
                                            </button>
                                        );
                                    })}
                                </div>

                                <div className="flex justify-end gap-3">
                                    <Button variant="outline" onClick={() => setShowCustomize(false)}>Cancel</Button>
                                    <Button onClick={handleReanalyze} disabled={reanalyzing || selectedFeatures.length === 0}>
                                        {reanalyzing ? (
                                            <>
                                                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                                Updating...
                                            </>
                                        ) : (
                                            <>
                                                <Zap className="w-4 h-4 mr-2" />
                                                Update Analysis
                                            </>
                                        )}
                                    </Button>
                                </div>
                            </Card>
                        </motion.div>
                    </div>
                )}

                {/* Quality Score + Health */}
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="grid md:grid-cols-2 gap-4 mb-8">
                    {data.qualityScore && data.qualityScore.overall_score !== undefined && (
                        <Card glass className="p-6">
                            <div className="flex items-center gap-4">
                                <div className={cn(
                                    "w-16 h-16 rounded-2xl flex items-center justify-center text-2xl font-bold",
                                    data.qualityScore.grade === "A" && "bg-green-100 text-green-600",
                                    data.qualityScore.grade === "B" && "bg-blue-100 text-blue-600",
                                    data.qualityScore.grade === "C" && "bg-amber-100 text-amber-600",
                                    data.qualityScore.grade === "D" && "bg-orange-100 text-orange-600",
                                    data.qualityScore.grade === "F" && "bg-red-100 text-red-600",
                                    !data.qualityScore.grade && "bg-gray-100 text-gray-600",
                                )}>
                                    {data.qualityScore.grade || "?"}
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold">Data Quality Score</h3>
                                    <p className="text-gray-600 dark:text-gray-400">
                                        {(data.qualityScore.overall_score || 0).toFixed(0)}/100 - {data.qualityScore.status || "Unknown"}
                                    </p>
                                </div>
                            </div>
                            {data.qualityScore.details && (
                                <div className="grid grid-cols-4 gap-2 mt-4">
                                    {Object.entries(data.qualityScore.details).map(([key, value]) => (
                                        <div key={key} className="text-center p-2 rounded-lg bg-gray-50 dark:bg-gray-800">
                                            <div className={cn("text-lg font-bold", (value as number) >= 80 && "text-green-600", (value as number) >= 60 && (value as number) < 80 && "text-amber-600", (value as number) < 60 && "text-red-600")}>
                                                {typeof value === "number" ? value.toFixed(0) : value}%
                                            </div>
                                            <div className="text-xs text-gray-500 capitalize">{key}</div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </Card>
                    )}

                    {data.health && data.health.overall_health !== undefined && (
                        <Card glass className="p-6">
                            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                <Shield className="w-5 h-5 text-purple-600" />
                                Dataset Health
                            </h3>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="text-center p-3 rounded-lg bg-purple-50 dark:bg-purple-900/20">
                                    <div className="text-2xl font-bold text-purple-600">{(data.health.overall_health || 0).toFixed(0)}%</div>
                                    <div className="text-xs text-gray-500">Overall Health</div>
                                </div>
                                <div className="text-center p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                                    <div className="text-2xl font-bold text-blue-600">{(data.health.size?.memory_mb || 0).toFixed(1)} MB</div>
                                    <div className="text-xs text-gray-500">Memory Usage</div>
                                </div>
                                <div className="text-center p-3 rounded-lg bg-green-50 dark:bg-green-900/20">
                                    <div className="text-2xl font-bold text-green-600">{data.health.completeness?.complete_rows || 0}</div>
                                    <div className="text-xs text-gray-500">Complete Rows</div>
                                </div>
                                <div className="text-center p-3 rounded-lg bg-amber-50 dark:bg-amber-900/20">
                                    <div className="text-2xl font-bold text-amber-600">{data.health.duplicates?.count || 0}</div>
                                    <div className="text-xs text-gray-500">Duplicates</div>
                                </div>
                            </div>
                        </Card>
                    )}
                </motion.div>

                {/* Summary Stats */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
                    <Card glass className="p-4 text-center">
                        <div className="text-2xl font-bold gradient-text">{(data.summary?.rows || 0).toLocaleString()}</div>
                        <div className="text-sm text-gray-500">Rows</div>
                    </Card>
                    <Card glass className="p-4 text-center">
                        <div className="text-2xl font-bold gradient-text">{data.summary?.columns || 0}</div>
                        <div className="text-sm text-gray-500">Columns</div>
                    </Card>
                    <Card glass className="p-4 text-center">
                        <div className="text-2xl font-bold gradient-text">{data.summary.numericColumns?.length || 0}</div>
                        <div className="text-sm text-gray-500">Numeric</div>
                    </Card>
                    <Card glass className="p-4 text-center">
                        <div className="text-2xl font-bold gradient-text">{data.summary.categoricalColumns?.length || 0}</div>
                        <div className="text-sm text-gray-500">Categorical</div>
                    </Card>
                    <Card glass className="p-4 text-center">
                        <div className="text-2xl font-bold gradient-text">{(data.summary.missingPercentage || 0).toFixed(1)}%</div>
                        <div className="text-sm text-gray-500">Missing</div>
                    </Card>
                </motion.div>

                {/* Tabs */}
                <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
                    {tabs.map((tab) => (
                        <Button
                            key={tab.id}
                            variant={activeTab === tab.id ? "default" : "outline"}
                            size="sm"
                            onClick={() => setActiveTab(tab.id)}
                            className="whitespace-nowrap relative group"
                        >
                            <tab.icon className="w-4 h-4 mr-2" />
                            {tab.label}
                            {["intelligence", "engineering", "insights"].includes(tab.id) && (userPlan === "free" || userPlan === "starter") && (
                                <Lock className="w-3 h-3 ml-2 text-amber-500" />
                            )}
                        </Button>
                    ))}
                </div>

                {/* Tab Content */}
                <div className="space-y-6">
                    {/* Overview */}
                    {activeTab === "overview" && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                            {/* Recommendations */}
                            {data.recommendations && data.recommendations.length > 0 && (
                                <Card glass className="p-6">
                                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                        <Sparkles className="w-5 h-5 text-purple-600" />
                                        AI Recommendations
                                    </h3>
                                    <div className="space-y-3">
                                        {data.recommendations.map((rec, idx) => (
                                            <div key={idx} className={cn(
                                                "p-4 rounded-lg border-l-4",
                                                rec.type === "warning" && "bg-amber-50 dark:bg-amber-900/20 border-amber-500",
                                                rec.type === "info" && "bg-blue-50 dark:bg-blue-900/20 border-blue-500",
                                                rec.type === "error" && "bg-red-50 dark:bg-red-900/20 border-red-500",
                                            )}>
                                                <div className="flex items-center gap-2 mb-1">
                                                    {rec.type === "warning" && <AlertTriangle className="w-4 h-4 text-amber-600" />}
                                                    {rec.type === "info" && <Info className="w-4 h-4 text-blue-600" />}
                                                    <span className="font-semibold">{rec.title}</span>
                                                </div>
                                                <p className="text-sm text-gray-600 dark:text-gray-400">{rec.description}</p>
                                                {rec.action && (
                                                    <code className="text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded mt-2 inline-block">
                                                        {rec.action}
                                                    </code>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </Card>
                            )}

                            {/* Feature Importance */}
                            {data.featureImportance && Object.keys(data.featureImportance).length > 0 && (
                                <Card glass className="p-6">
                                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                        <Zap className="w-5 h-5 text-amber-500" />
                                        Feature Importance
                                    </h3>
                                    <div className="space-y-2">
                                        {Object.entries(data.featureImportance).slice(0, 8).map(([col, score]) => (
                                            <div key={col} className="flex items-center gap-3">
                                                <div className="w-24 text-sm font-medium truncate">{col}</div>
                                                <div className="flex-1 h-4 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                                                    <div
                                                        className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full"
                                                        style={{ width: `${score * 100}%` }}
                                                    />
                                                </div>
                                                <div className="w-12 text-sm text-right">{(score * 100).toFixed(0)}%</div>
                                            </div>
                                        ))}
                                    </div>
                                </Card>
                            )}

                            {/* Target Analysis */}
                            {data.targetAnalysis && data.targetAnalysis.target_column && (
                                <Card glass className="p-6">
                                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                        <Target className="w-5 h-5 text-red-500" />
                                        Target Analysis: {data.targetAnalysis.target_column}
                                    </h3>
                                    <div className="flex flex-wrap gap-3 mb-4">
                                        <Badge>{data.targetAnalysis.task_type}</Badge>
                                        {data.targetAnalysis.imbalance_warning && (
                                            <Badge variant="outline" className="text-amber-600 border-amber-600">
                                                {data.targetAnalysis.imbalance_warning}
                                            </Badge>
                                        )}
                                        {data.targetAnalysis.target_warning && (
                                            <Badge variant="outline" className="text-blue-600 border-blue-600">
                                                {data.targetAnalysis.target_warning}
                                            </Badge>
                                        )}
                                    </div>
                                    {data.targetAnalysis.leakage_warnings && data.targetAnalysis.leakage_warnings.length > 0 && (
                                        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                                            <h4 className="font-bold text-red-700 dark:text-red-400 mb-2">🚨 Leakage Warnings</h4>
                                            {data.targetAnalysis.leakage_warnings.map((warn, idx) => (
                                                <p key={idx} className="text-sm text-red-600 dark:text-red-300">{warn.warning}</p>
                                            ))}
                                        </div>
                                    )}
                                    {data.targetAnalysis.class_distribution && (
                                        <div className="flex flex-wrap gap-2">
                                            {Object.entries(data.targetAnalysis.class_distribution).map(([cls, count]) => (
                                                <Badge key={cls} variant="outline">
                                                    {cls}: {count}
                                                </Badge>
                                            ))}
                                        </div>
                                    )}
                                </Card>
                            )}

                            {/* Outliers & Duplicates */}
                            <div className="grid md:grid-cols-2 gap-4">
                                {data.outliers && Object.keys(data.outliers).length > 0 && (
                                    <Card glass className="p-6">
                                        <h3 className="text-lg font-bold mb-4">🔍 Outliers Detected</h3>
                                        <div className="flex flex-wrap gap-2">
                                            {Object.entries(data.outliers).map(([col, count]) => (
                                                <Badge key={col} variant="outline">
                                                    {col}: <span className="font-bold ml-1">{count}</span>
                                                </Badge>
                                            ))}
                                        </div>
                                    </Card>
                                )}

                                {data.duplicates && data.duplicates.total_duplicates > 0 && (
                                    <Card glass className="p-6">
                                        <h3 className="text-lg font-bold mb-4">📋 Duplicates Found</h3>
                                        <div className="text-3xl font-bold text-amber-600">{data.duplicates.total_duplicates}</div>
                                        <p className="text-sm text-gray-500">{data.duplicates.duplicate_percentage.toFixed(1)}% of rows</p>
                                    </Card>
                                )}
                            </div>

                            {/* Stats Table */}
                            {data.summary.statistics && Object.keys(data.summary.statistics).length > 0 && (
                                <Card glass className="p-6 overflow-x-auto">
                                    <h3 className="text-lg font-bold mb-4">📊 Column Statistics</h3>
                                    <table className="w-full text-sm">
                                        <thead>
                                            <tr className="border-b dark:border-gray-700">
                                                <th className="text-left py-2 font-semibold">Column</th>
                                                <th className="text-right py-2">Mean</th>
                                                <th className="text-right py-2">Std</th>
                                                <th className="text-right py-2">Min</th>
                                                <th className="text-right py-2">Max</th>
                                                <th className="text-right py-2">Skewness</th>
                                                <th className="text-right py-2">Kurtosis</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {Object.entries(data.summary.statistics).map(([col, stats]: [string, any]) => (
                                                <tr key={col} className="border-b dark:border-gray-800">
                                                    <td className="py-2 font-medium">{col}</td>
                                                    <td className="text-right">{stats.mean?.toFixed(2)}</td>
                                                    <td className="text-right">{stats.std?.toFixed(2)}</td>
                                                    <td className="text-right">{stats.min?.toFixed(2)}</td>
                                                    <td className="text-right">{stats.max?.toFixed(2)}</td>
                                                    <td className={cn("text-right", Math.abs(stats.skewness) > 2 && "text-amber-600 font-bold")}>
                                                        {stats.skewness?.toFixed(2)}
                                                    </td>
                                                    <td className="text-right">{stats.kurtosis?.toFixed(2)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </Card>
                            )}
                        </motion.div>
                    )}

                    {/* Intelligence Tab */}
                    {activeTab === "intelligence" && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                            {(userPlan === "free" || userPlan === "starter") ? (
                                <Card glass className="p-12 text-center border-amber-200 dark:border-amber-800">
                                    <div className="w-20 h-20 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl shadow-purple-500/20">
                                        <Shield className="w-10 h-10 text-white" />
                                    </div>
                                    <h3 className="text-2xl font-bold mb-3">Dataset Intelligence (Pro)</h3>
                                    <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-8 text-lg">
                                        <strong>Why it matters:</strong> Raw data is rarely ready for analysis.
                                        Our Intelligence engine runs 50+ diagnostic checks to give you a <strong>Health Score</strong>
                                        and <strong>ML Readiness</strong> verdict. It catches data leakage, class imbalance, and
                                        validity issues before they ruin your models.
                                    </p>
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 text-left max-w-4xl mx-auto">
                                        <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl border border-purple-100 dark:border-purple-900/30">
                                            <div className="font-bold text-purple-600 mb-1">Health Score</div>
                                            <p className="text-xs text-gray-500">Comprehensiveness, Validity, and Consistency metrics.</p>
                                        </div>
                                        <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl border border-purple-100 dark:border-purple-900/30">
                                            <div className="font-bold text-purple-600 mb-1">ML Readiness</div>
                                            <p className="text-xs text-gray-500">Know exactly if your data is ready for Random Forest, XGBoost, etc.</p>
                                        </div>
                                        <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl border border-purple-100 dark:border-purple-900/30">
                                            <div className="font-bold text-purple-600 mb-1">Drift Detection</div>
                                            <p className="text-xs text-gray-500">Identify patterns that might cause model failure.</p>
                                        </div>
                                    </div>
                                    <Link href="/pricing">
                                        <Button size="lg" className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 px-8 py-6 text-lg rounded-xl">
                                            <Zap className="w-5 h-5 mr-2" />
                                            Upgrade to Pro
                                        </Button>
                                    </Link>
                                </Card>
                            ) : (
                                <>
                                    {(!data.mlReadiness && !data.healthScore) && (
                                        <Card glass className="p-12 text-center border-dashed border-gray-300 dark:border-gray-700">
                                            <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                                                <Wand2 className="w-8 h-8 text-gray-400" />
                                            </div>
                                            <h3 className="text-xl font-bold mb-2">Advanced Intelligence Not Available</h3>
                                            <p className="text-gray-500 max-w-md mx-auto mb-6">
                                                This report was generated with an older version of Kuya or without Intelligence features.
                                                Please re-analyze your data to unlock ML Readiness, Health Score, and Target-Aware analysis.
                                            </p>
                                            <Button onClick={() => setShowCustomize(true)} variant="outline" className="gap-2">
                                                <Settings2 className="w-4 h-4" />
                                                Re-analyze Now
                                            </Button>
                                        </Card>
                                    )}

                                    {/* ML Readiness */}
                                    {data.mlReadiness && (
                                        <Card glass className="p-6 mb-6">
                                            <div className="flex items-center justify-between mb-6">
                                                <h3 className="text-xl font-bold flex items-center gap-2">
                                                    <Wand2 className="w-6 h-6 text-purple-600" />
                                                    ML Readiness Check
                                                </h3>
                                                <Badge className={cn(
                                                    "text-lg px-4 py-1",
                                                    data.mlReadiness.verdict_color === "green" ? "bg-green-100 text-green-700" :
                                                        data.mlReadiness.verdict_color === "yellow" ? "bg-amber-100 text-amber-700" :
                                                            "bg-red-100 text-red-700"
                                                )}>
                                                    {data.mlReadiness.verdict}
                                                </Badge>
                                            </div>

                                            <div className="grid md:grid-cols-2 gap-8">
                                                <div className="space-y-4">
                                                    {data.mlReadiness.checks?.map((check, idx) => (
                                                        <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                                                            <span className="font-medium text-sm">{check.check}</span>
                                                            <span className={cn(
                                                                "text-xs font-semibold",
                                                                check.status === "pass" ? "text-green-600" :
                                                                    check.status === "warning" ? "text-amber-600" : "text-red-600"
                                                            )}>
                                                                {check.message}
                                                            </span>
                                                        </div>
                                                    ))}
                                                </div>
                                                <div>
                                                    <h4 className="font-semibold mb-3 text-gray-700 dark:text-gray-300 text-sm">Recommended Models</h4>
                                                    <div className="grid gap-3">
                                                        {data.mlReadiness.recommended_models?.map((model, idx) => (
                                                            <div key={idx} className="p-3 border rounded-lg border-purple-100 dark:border-gray-700 bg-purple-50/50 dark:bg-gray-800/30">
                                                                <div className="font-bold text-sm text-purple-700 dark:text-purple-400">{model.name}</div>
                                                                <div className="text-[10px] text-gray-500 leading-tight">{model.reason}</div>
                                                            </div>
                                                        ))}
                                                    </div>
                                                </div>
                                            </div>
                                        </Card>
                                    )}

                                    {/* Health Score Breakdown */}
                                    {data.healthScore && (
                                        <Card glass className="p-6">
                                            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                                                <Shield className="w-6 h-6 text-blue-600" />
                                                Health Score Breakdown
                                            </h3>
                                            <div className="space-y-4">
                                                {Object.entries(data.healthScore.breakdown || {}).map(([key, item]) => (
                                                    <div key={key}>
                                                        <div className="flex justify-between text-sm mb-1">
                                                            <span className="font-medium text-gray-700 dark:text-gray-300">{item.label}</span>
                                                            <span className="text-gray-500 font-mono text-xs">{item.score}/{item.max}</span>
                                                        </div>
                                                        <div className="h-2 w-full bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                                                            <div
                                                                className={cn("h-full rounded-full transition-all duration-1000",
                                                                    (item.score / item.max) > 0.8 ? "bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.3)]" :
                                                                        (item.score / item.max) > 0.5 ? "bg-amber-500 shadow-[0_0_10px_rgba(245,158,11,0.3)]" : "bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.3)]"
                                                                )}
                                                                style={{ width: `${(item.score / item.max) * 100}%` }}
                                                            />
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                            {data.healthScore.issues && (
                                                <div className="mt-8 pt-6 border-t dark:border-gray-800 grid grid-cols-2 md:grid-cols-4 gap-4">
                                                    <div className="text-center">
                                                        <div className="text-xs text-gray-500 mb-1">Missing Cells</div>
                                                        <div className="font-bold">{data.healthScore.issues.missing_cells}</div>
                                                    </div>
                                                    <div className="text-center">
                                                        <div className="text-xs text-gray-500 mb-1">Duplicates</div>
                                                        <div className="font-bold">{data.healthScore.issues.duplicate_rows}</div>
                                                    </div>
                                                    <div className="text-center">
                                                        <div className="text-xs text-gray-500 mb-1">Features</div>
                                                        <div className="font-bold">{data.healthScore.issues.total_columns}</div>
                                                    </div>
                                                    <div className="text-center">
                                                        <div className="text-xs text-gray-500 mb-1">Numeric</div>
                                                        <div className="font-bold">{data.healthScore.issues.numeric_columns}</div>
                                                    </div>
                                                </div>
                                            )}
                                        </Card>
                                    )}
                                </>
                            )}
                        </motion.div>
                    )}

                    {/* Engineering Tab */}
                    {activeTab === "engineering" && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                            {(userPlan === "free" || userPlan === "starter") ? (
                                <Card glass className="p-12 text-center border-amber-200 dark:border-amber-800">
                                    <div className="w-20 h-20 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl shadow-red-500/20">
                                        <Zap className="w-10 h-10 text-white" />
                                    </div>
                                    <h3 className="text-2xl font-bold mb-3">Auto Feature Engineering (Pro)</h3>
                                    <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-8 text-lg">
                                        <strong>Why it matters:</strong> Feature engineering is the secret sauce of top data scientists.
                                        Our engine automatically finds the best transformations for your data—reducing
                                        skewness, handling outliers, and creating powerful interaction features.
                                    </p>
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 text-left max-w-4xl mx-auto">
                                        <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl border border-orange-100 dark:border-orange-900/30">
                                            <div className="font-bold text-orange-600 mb-1">Smart Scaling</div>
                                            <p className="text-xs text-gray-500">Automatically chooses between Standard, Robust, or MinMax scaling.</p>
                                        </div>
                                        <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl border border-orange-100 dark:border-orange-900/30">
                                            <div className="font-bold text-orange-600 mb-1">Encoding Logic</div>
                                            <p className="text-xs text-gray-500">Detects high-cardinality features and suggests Target or Hashing encoding.</p>
                                        </div>
                                        <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl border border-orange-100 dark:border-orange-900/30">
                                            <div className="font-bold text-orange-600 mb-1">Deep Analysis</div>
                                            <p className="text-xs text-gray-500">Column-by-column quality profile and recommended cleaning actions.</p>
                                        </div>
                                    </div>
                                    <Link href="/pricing">
                                        <Button size="lg" className="bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 px-8 py-6 text-lg rounded-xl">
                                            <Sparkles className="w-5 h-5 mr-2" />
                                            Upgrade now
                                        </Button>
                                    </Link>
                                </Card>
                            ) : (
                                <>
                                    {(!data.engineeringSuggestions && !data.columnAnalysis) && (
                                        <Card glass className="p-12 text-center border-dashed border-gray-300 dark:border-gray-700">
                                            <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                                                <Zap className="w-8 h-8 text-gray-400" />
                                            </div>
                                            <h3 className="text-xl font-bold mb-2">Deep Engineering Not Available</h3>
                                            <p className="text-gray-500 max-w-md mx-auto mb-6">
                                                This report does not contain advanced engineering data.
                                                Please re-analyze your data to unlock Feature Engineering suggestions and Deep Column Analysis.
                                            </p>
                                            <Button onClick={() => setShowCustomize(true)} variant="outline" className="gap-2">
                                                <Settings2 className="w-4 h-4" />
                                                Re-analyze Now
                                            </Button>
                                        </Card>
                                    )}

                                    {/* Feature Engineering Suggestions */}
                                    {data.engineeringSuggestions && data.engineeringSuggestions.length > 0 && (
                                        <Card glass className="p-6 mb-6">
                                            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                                                <Zap className="w-6 h-6 text-amber-500" />
                                                Auto Feature Engineering
                                            </h3>
                                            <div className="grid gap-4">
                                                {data.engineeringSuggestions.map((sugg, idx) => (
                                                    <div key={idx} className="flex flex-col md:flex-row md:items-center justify-between p-4 border rounded-xl hover:shadow-md transition-all bg-white dark:bg-gray-800/50">
                                                        <div className="flex items-start gap-4 mb-4 md:mb-0">
                                                            <div className="text-2xl">{sugg.icon}</div>
                                                            <div>
                                                                <div className="flex items-center gap-2 mb-1">
                                                                    <span className="font-bold text-gray-800 dark:text-gray-100">{sugg.action}</span>
                                                                    <Badge variant="outline" className="text-xs">{sugg.column}</Badge>
                                                                    {sugg.priority === "high" && (
                                                                        <Badge className="bg-red-100 text-red-600 hover:bg-red-200 border-none">High Priority</Badge>
                                                                    )}
                                                                </div>
                                                                <p className="text-sm text-gray-600 dark:text-gray-400">{sugg.reason}</p>
                                                            </div>
                                                        </div>
                                                        <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg font-mono text-xs text-purple-600 dark:text-purple-400 overflow-x-auto whitespace-nowrap border border-gray-100 dark:border-gray-800">
                                                            {sugg.method}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </Card>
                                    )}

                                    {/* Smart Column Analysis */}
                                    {data.columnAnalysis && (
                                        <Card glass className="p-6">
                                            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                                                <Search className="w-6 h-6 text-blue-500" />
                                                Deep Column Analysis
                                            </h3>
                                            <div className="overflow-x-auto">
                                                <table className="w-full text-sm">
                                                    <thead>
                                                        <tr className="border-b dark:border-gray-700 text-left">
                                                            <th className="py-3 px-4">Column</th>
                                                            <th className="py-3 px-4">Type</th>
                                                            <th className="py-3 px-4">Quality</th>
                                                            <th className="py-3 px-4">Rec. Action</th>
                                                            <th className="py-3 px-4">Issues</th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        {Object.entries(data.columnAnalysis || {}).map(([col, info]) => (
                                                            <tr key={col} className="border-b dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                                                                <td className="py-3 px-4 font-medium">{col}</td>
                                                                <td className="py-3 px-4">
                                                                    <Badge variant="secondary" className="capitalize text-[10px]">{info.type}</Badge>
                                                                </td>
                                                                <td className="py-3 px-4 text-xs">
                                                                    <div className="flex items-center gap-2">
                                                                        <div className={cn("w-2 h-2 rounded-full", info.quality_score > 80 ? "bg-green-500" : info.quality_score > 50 ? "bg-amber-500" : "bg-red-500")} />
                                                                        {info.quality_score}%
                                                                    </div>
                                                                </td>
                                                                <td className="py-3 px-4 font-mono text-[10px] text-gray-600 dark:text-gray-400">
                                                                    {info.action !== "none" ? info.action : "-"}
                                                                </td>
                                                                <td className="py-3 px-4">
                                                                    <div className="flex flex-wrap gap-1">
                                                                        {info.issues?.map((issue, i) => (
                                                                            <Badge key={i} variant="outline" className="text-[10px] text-red-500 border-red-200 bg-red-50 dark:bg-red-900/10 h-5">
                                                                                {issue}
                                                                            </Badge>
                                                                        ))}
                                                                        {info.issues?.length === 0 && <span className="text-green-500 text-xs">Ready</span>}
                                                                    </div>
                                                                </td>
                                                            </tr>
                                                        ))}
                                                    </tbody>
                                                </table>
                                            </div>
                                        </Card>
                                    )}
                                </>
                            )}
                        </motion.div>
                    )}

                    {/* Charts */}
                    {activeTab === "charts" && (
                        <div className="space-y-4">
                            <div className="flex flex-wrap gap-2 mb-4 p-3 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-100 dark:border-gray-800">
                                <span className="text-sm font-medium text-gray-500 flex items-center mr-2">Active Analysis:</span>
                                {(data.selectedFeatures || []).map((fid: string) => {
                                    const feature = AVAILABLE_FEATURES.find((f) => f.id === fid);
                                    if (!feature) return null;
                                    const Icon = feature.icon;
                                    return (
                                        <Badge key={fid} variant="secondary" className="flex items-center gap-2 px-3 py-1.5 bg-white dark:bg-gray-700 border border-purple-200 dark:border-gray-600 shadow-sm text-gray-700 dark:text-gray-200 text-sm rounded-lg pr-1.5 group transition-all hover:shadow-md">
                                            <Icon className="w-4 h-4 text-purple-600" />
                                            {feature.name}
                                            <button
                                                onClick={(e) => { e.stopPropagation(); handleRemoveFeature(fid); }}
                                                className="ml-2 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full p-0.5 transition-colors"
                                            >
                                                <X className="w-3.5 h-3.5 text-gray-400 group-hover:text-red-500" />
                                            </button>
                                        </Badge>
                                    );
                                })}
                                {(data.graphs || []).length === 0 && (
                                    <span className="text-sm text-gray-400 italic">No visualizations generated.</span>
                                )}
                            </div>
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                {(data.graphs || []).map((graph, idx) => (
                                    <ChartDisplay
                                        key={idx}
                                        title={graph.title}
                                        image={graph.image}
                                        delay={idx * 0.1}
                                    />
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Insights */}
                    {activeTab === "insights" && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                            {/* Feature Gate */}
                            {(userPlan === "free" || userPlan === "starter") ? (
                                <Card glass className="p-12 text-center border-amber-200 dark:border-amber-800">
                                    <div className="w-20 h-20 bg-gradient-to-br from-amber-400 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl shadow-amber-500/20">
                                        <Sparkles className="w-10 h-10 text-white" />
                                    </div>
                                    <h3 className="text-2xl font-bold mb-3">Automated AI Insights (Pro)</h3>
                                    <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-8 text-lg">
                                        <strong>Why it matters:</strong> Manual analysis takes hours and often misses subtle trends.
                                        Our AI engine scans your entire dataset to find <strong>hidden correlations</strong>,
                                        <strong>anomalies</strong>, and <strong>actionable patterns</strong> instantly.
                                    </p>
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 text-left max-w-4xl mx-auto">
                                        <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl border border-amber-100 dark:border-amber-900/30">
                                            <div className="font-bold text-amber-600 mb-1">Pattern Mining</div>
                                            <p className="text-xs text-gray-500">Find relationships between features that manual plotting might miss.</p>
                                        </div>
                                        <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl border border-amber-100 dark:border-amber-900/30">
                                            <div className="font-bold text-amber-600 mb-1">Anomaly Detection</div>
                                            <p className="text-xs text-gray-500">Identify outlier groups and clusters that signal risky or unique data points.</p>
                                        </div>
                                        <div className="p-4 bg-white/50 dark:bg-gray-800/50 rounded-xl border border-amber-100 dark:border-amber-900/30">
                                            <div className="font-bold text-amber-600 mb-1">Natural Language</div>
                                            <p className="text-xs text-gray-500">Receive insights in plain English that you can directly paste into reports.</p>
                                        </div>
                                    </div>
                                    <Link href="/pricing">
                                        <Button size="lg" className="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 shadow-lg shadow-orange-500/20 px-8 py-6 text-lg rounded-xl">
                                            <Zap className="w-5 h-5 mr-2" />
                                            Unlock AI Engine
                                        </Button>
                                    </Link>
                                </Card>
                            ) : (
                                <Card glass className="p-6">
                                    <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                        <Sparkles className="w-5 h-5 text-amber-500" />
                                        AI-Generated Insights
                                    </h3>
                                    <div className="space-y-3">
                                        {(!data.insights || data.insights.length === 0) && (
                                            <div className="p-8 text-center text-gray-500 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-dashed border-gray-200 dark:border-gray-700">
                                                <Sparkles className="w-10 h-10 mx-auto mb-3 text-gray-300" />
                                                <p className="font-medium">No insights generated yet</p>
                                                <p className="text-sm mt-1">Select <span className="font-semibold text-purple-600">Automated Insights</span> or <span className="font-semibold text-purple-600">Magic Analysis</span> to see AI findings.</p>
                                            </div>
                                        )}
                                        {(data.insights || []).map((insight, idx) => {
                                            const isGood = insight.includes("✅") || insight.includes("Good") || insight.includes("Excellent");
                                            const isWarning = insight.includes("⚠️") || insight.includes("Warning");
                                            const isAlert = insight.includes("🚨") || insight.includes("Alert");
                                            const isInfo = insight.includes("📊") || insight.includes("🔗") || insight.includes("📈");

                                            return (
                                                <div key={idx} className={cn(
                                                    "p-4 rounded-lg border-l-4",
                                                    isGood && "bg-green-50 dark:bg-green-900/20 border-green-500",
                                                    isWarning && "bg-amber-50 dark:bg-amber-900/20 border-amber-500",
                                                    isAlert && "bg-red-50 dark:bg-red-900/20 border-red-500",
                                                    isInfo && "bg-blue-50 dark:bg-blue-900/20 border-blue-500",
                                                    !isGood && !isWarning && !isAlert && !isInfo && "bg-gray-50 dark:bg-gray-800 border-gray-300"
                                                )}>
                                                    <p className="text-gray-700 dark:text-gray-300" dangerouslySetInnerHTML={{ __html: insight.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }} />
                                                </div>
                                            );
                                        })}
                                    </div>
                                </Card>
                            )}
                        </motion.div>
                    )}

                    {/* Data Preview */}
                    {activeTab === "data" && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                            <Card glass className="p-6 overflow-x-auto">
                                <div className="flex items-center justify-between mb-4">
                                    <h3 className="text-lg font-bold flex items-center gap-2">
                                        <Table className="w-5 h-5 text-purple-600" />
                                        Cleaned Data Preview
                                    </h3>
                                    <div className="flex items-center gap-3">
                                        <span className="text-sm text-gray-500">Rows:</span>
                                        <Select value={rowsLimit} onValueChange={setRowsLimit}>
                                            <SelectTrigger className="w-[110px] h-8 bg-white dark:bg-gray-800">
                                                <SelectValue placeholder="Limit" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="10">10</SelectItem>
                                                <SelectItem value="20">20</SelectItem>
                                                <SelectItem value="50">50</SelectItem>
                                                <SelectItem value="100">100</SelectItem>
                                                <SelectItem value="1000">1000</SelectItem>
                                                <SelectItem value="10000">All (Max)</SelectItem>
                                            </SelectContent>
                                        </Select>

                                        <div className="flex flex-col sm:flex-row items-end sm:items-center gap-2">
                                            <Badge variant="outline" className="hidden sm:inline-flex whitespace-nowrap">
                                                {Math.min(data.cleanedDataHead.length, parseInt(rowsLimit))} / {data.cleanedDataHead.length} loaded
                                            </Badge>
                                            {parseInt(rowsLimit) > data.cleanedDataHead.length && data.cleanedDataHead.length < 1000 && (
                                                <div className="text-xs text-amber-500 flex items-center gap-1 bg-amber-50 dark:bg-amber-900/20 px-2 py-1 rounded border border-amber-200 dark:border-amber-800">
                                                    <AlertTriangle className="w-3 h-3" />
                                                    <span>Data cached. Update Analysis to fetch more.</span>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                                <div className="max-h-[600px] overflow-auto border rounded-md">
                                    <table className="w-full text-sm relative">
                                        <thead className="sticky top-0 z-10">
                                            <tr className="border-b dark:border-gray-700 shadow-sm">
                                                {data.cleanedDataHead.length > 0 && Object.keys(data.cleanedDataHead[0]).map((key) => (
                                                    <th key={key} className="text-left py-2 px-3 font-semibold whitespace-nowrap bg-gray-50 dark:bg-gray-800 border-b">
                                                        {key}
                                                    </th>
                                                ))}
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {data.cleanedDataHead.slice(0, parseInt(rowsLimit)).map((row, idx) => (
                                                <tr key={idx} className="border-b dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                                                    {Object.values(row).map((val: any, vidx) => (
                                                        <td key={vidx} className="py-2 px-3 whitespace-nowrap">
                                                            {typeof val === "number" ? val.toLocaleString() : String(val).substring(0, 50)}
                                                        </td>
                                                    ))}
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </Card>

                            {/* Column Mapping */}
                            {data.columnMapping && Object.keys(data.columnMapping).length > 0 && (
                                <Card glass className="p-6 mt-6">
                                    <h3 className="text-lg font-bold mb-4">✏️ Column Renaming</h3>
                                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                                        {Object.entries(data.columnMapping).filter(([k, v]) => k !== v).map(([original, renamed]) => (
                                            <div key={original} className="text-sm bg-gray-50 dark:bg-gray-800 p-2 rounded">
                                                <span className="text-gray-500 line-through">{original}</span>
                                                <span className="mx-2">→</span>
                                                <span className="font-medium text-green-600">{renamed}</span>
                                            </div>
                                        ))}
                                    </div>
                                </Card>
                            )}
                        </motion.div>
                    )}

                    {/* Export */}
                    {activeTab === "export" && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                            <Card glass className="p-6">
                                <h3 className="text-lg font-bold mb-6">📥 Export Options</h3>
                                <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                                    <Button variant="outline" size="lg" className="h-auto py-6 flex-col" onClick={() => handleExport("csv")} disabled={exporting === "csv"}>
                                        {exporting === "csv" ? <Loader2 className="w-6 h-6 mb-2 animate-spin" /> : <FileText className="w-6 h-6 mb-2 text-green-600" />}
                                        <span className="font-semibold">CSV</span>
                                        <span className="text-xs text-gray-500">Cleaned Data</span>
                                    </Button>
                                    <Button variant="outline" size="lg" className="h-auto py-6 flex-col" onClick={() => handleExport("excel")} disabled={exporting === "excel"}>
                                        {exporting === "excel" ? <Loader2 className="w-6 h-6 mb-2 animate-spin" /> : <FileSpreadsheet className="w-6 h-6 mb-2 text-emerald-600" />}
                                        <span className="font-semibold">Excel</span>
                                        <span className="text-xs text-gray-500">With Summary</span>
                                    </Button>
                                    <Button variant="outline" size="lg" className="h-auto py-6 flex-col" onClick={() => window.open(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/report/${reportId}`, "_blank")}>
                                        <FileText className="w-6 h-6 mb-2 text-red-600" />
                                        <span className="font-semibold">PDF</span>
                                        <span className="text-xs text-gray-500">Full Report</span>
                                    </Button>
                                    <Button variant="outline" size="lg" className="h-auto py-6 flex-col" onClick={() => handleExport("html")} disabled={exporting === "html"}>
                                        {exporting === "html" ? <Loader2 className="w-6 h-6 mb-2 animate-spin" /> : <Globe className="w-6 h-6 mb-2 text-blue-600" />}
                                        <span className="font-semibold">HTML</span>
                                        <span className="text-xs text-gray-500">Interactive</span>
                                    </Button>
                                    <Button variant="outline" size="lg" className="h-auto py-6 flex-col" onClick={() => handleExport("json")} disabled={exporting === "json"}>
                                        {exporting === "json" ? <Loader2 className="w-6 h-6 mb-2 animate-spin" /> : <Code className="w-6 h-6 mb-2 text-purple-600" />}
                                        <span className="font-semibold">JSON</span>
                                        <span className="text-xs text-gray-500">API Format</span>
                                    </Button>
                                    <Button variant="outline" size="lg" className="h-auto py-6 flex-col" onClick={() => window.open(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/report/${reportId}/view`, "_blank")}>
                                        <Globe className="w-6 h-6 mb-2 text-indigo-600" />
                                        <span className="font-semibold">View HTML</span>
                                        <span className="text-xs text-gray-500">In Browser</span>
                                    </Button>
                                </div>
                            </Card>
                        </motion.div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default function ResultPage() {
    return (
        <Suspense fallback={<div className="min-h-screen pt-24 flex items-center justify-center"><Loader2 className="w-12 h-12 animate-spin text-purple-600" /></div>}>
            <ResultContent />
        </Suspense>
    );
}
