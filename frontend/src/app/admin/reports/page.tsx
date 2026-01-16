"use client";

import React, { useEffect, useState } from "react";
import {
    FileText,
    Search,
    RefreshCcw,
    User,
    ExternalLink,
    Download,
    Trash2,
    Database
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

interface Report {
    _id: string;
    filename: string;
    userEmail: string;
    createdAt: string;
    fileSize: number;
    summary?: {
        rows: number;
        columns: number;
    };
}

export default function AdminReportsPage() {
    const [reports, setReports] = useState<Report[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");

    const fetchReports = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem("admin_token");
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/reports/recent`, {
                headers: { "x-admin-token": token || "" }
            });
            if (response.ok) {
                const data = await response.json();
                setReports(data);
            }
        } catch (error) {
            toast.error("Failed to fetch reports");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchReports();
    }, []);

    const filteredReports = reports.filter(r =>
        (r?.filename || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
        (r?.userEmail || "").toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleExport = async (target: string) => {
        try {
            const token = localStorage.getItem("admin_token");
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/export/${target}`, {
                headers: { "x-admin-token": token || "" }
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `kuya_${target}_${new Date().toISOString().split('T')[0]}.csv`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                toast.success("Data exported successfully!");
            } else {
                toast.error("Export failed");
            }
        } catch (error) {
            toast.error("Failed to export data");
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold font-display">Recent Reports</h1>
                    <p className="text-gray-500 text-sm">Review data analysis activity across the platform</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => handleExport("reports")}>
                        <Download className="w-4 h-4 mr-2" />
                        Export CSV
                    </Button>
                    <Button variant="outline" size="sm" onClick={fetchReports} disabled={loading}>
                        <RefreshCcw className={loading ? "animate-spin mr-2" : "mr-2"} size={16} />
                        Refresh
                    </Button>
                </div>
            </div>

            <Card className="p-4 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm">
                <div className="flex items-center gap-3 bg-white dark:bg-gray-900 border rounded-xl px-4 py-2">
                    <Search className="text-gray-400" size={20} />
                    <input
                        type="text"
                        placeholder="Search reports by filename or user..."
                        className="flex-1 bg-transparent border-none outline-none text-sm"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </Card>

            <div className="grid gap-4">
                {loading && reports.length === 0 ? (
                    <div className="py-20 text-center text-gray-400">Loading system activity...</div>
                ) : filteredReports.map((report) => (
                    <Card key={report._id} className="p-4 hover:shadow-md transition-shadow">
                        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                            <div className="flex items-start gap-4">
                                <div className="p-3 rounded-lg bg-purple-50 dark:bg-purple-900/20 text-purple-600">
                                    <FileText size={24} />
                                </div>
                                <div>
                                    <h4 className="font-bold text-gray-900 dark:text-gray-100">{report.filename}</h4>
                                    <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-1">
                                        <span className="text-xs text-blue-600 flex items-center gap-1">
                                            <User size={12} />
                                            {report.userEmail}
                                        </span>
                                        <span className="text-xs text-gray-400">
                                            {(report.fileSize / 1024).toFixed(1)} KB
                                        </span>
                                        <span className="text-xs text-gray-400 flex items-center gap-1">
                                            <Database size={12} />
                                            {report.summary?.rows || 0} rows × {report.summary?.columns || 0} cols
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div className="flex items-center gap-2">
                                <div className="text-right mr-4 hidden md:block">
                                    <div className="text-xs font-medium text-gray-500">
                                        {new Date(report.createdAt).toLocaleDateString()}
                                    </div>
                                    <div className="text-[10px] text-gray-400 uppercase">
                                        {new Date(report.createdAt).toLocaleTimeString()}
                                    </div>
                                </div>
                                <Badge variant="outline" className="bg-green-50 text-green-700 border-green-100 h-6">
                                    Success
                                </Badge>
                            </div>
                        </div>
                    </Card>
                ))}
            </div>
        </div>
    );
}
