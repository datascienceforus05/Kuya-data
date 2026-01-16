"use client";

import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import {
    Upload,
    FileSpreadsheet,
    X,
    CheckCircle2,
    AlertCircle,
    Loader2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Card } from "@/components/ui/card";
import { formatFileSize } from "@/lib/utils";

interface FileUploadProps {
    onUploadComplete: (reportId: string) => void;
    userEmail?: string;
}

export function FileUpload({ onUploadComplete, userEmail }: FileUploadProps) {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState<string | null>(null);
    const [status, setStatus] = useState<"idle" | "uploading" | "processing" | "success" | "error">("idle");

    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 0) {
            setFile(acceptedFiles[0]);
            setError(null);
            setStatus("idle");
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
        onDrop,
        accept: {
            "text/csv": [".csv"],
            "application/vnd.ms-excel": [".xls"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
        },
        maxFiles: 1,
        maxSize: 10 * 1024 * 1024, // 10MB
        onDropRejected: (rejections) => {
            const rejection = rejections[0];
            if (rejection.errors[0].code === "file-too-large") {
                setError("File is too large. Maximum size is 10MB.");
            } else if (rejection.errors[0].code === "file-invalid-type") {
                setError("Invalid file type. Please upload a CSV or Excel file.");
            } else {
                setError("Could not upload file. Please try again.");
            }
        },
    });

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setProgress(0);
        setStatus("uploading");
        setError(null);

        const formData = new FormData();
        formData.append("file", file);
        if (userEmail) {
            formData.append("email", userEmail);
        }

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

            setStatus("uploading");

            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/upload`,
                {
                    method: "POST",
                    body: formData,
                }
            );

            clearInterval(progressInterval);
            setProgress(100);
            setStatus("processing");

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || "Upload failed");
            }

            const data = await response.json();
            setStatus("success");

            // Small delay to show success state
            setTimeout(() => {
                onUploadComplete(data.reportId);
            }, 1000);
        } catch (err) {
            setStatus("error");
            setError(err instanceof Error ? err.message : "Upload failed. Please try again.");
        } finally {
            setUploading(false);
        }
    };

    const removeFile = () => {
        setFile(null);
        setError(null);
        setStatus("idle");
        setProgress(0);
    };

    return (
        <div className="w-full max-w-2xl mx-auto">
            <AnimatePresence mode="wait">
                {!file ? (
                    <motion.div
                        key="dropzone"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                    >
                        <div
                            {...getRootProps()}
                            className={`
                relative p-12 border-2 border-dashed rounded-2xl cursor-pointer transition-all duration-300
                ${isDragActive && !isDragReject
                                    ? "border-purple-500 bg-purple-50 dark:bg-purple-900/20"
                                    : isDragReject
                                        ? "border-red-500 bg-red-50 dark:bg-red-900/20"
                                        : "border-gray-300 dark:border-gray-700 hover:border-purple-500/50 hover:bg-gray-50 dark:hover:bg-gray-800/50"
                                }
              `}
                        >
                            <input {...getInputProps()} />

                            <div className="flex flex-col items-center text-center">
                                <motion.div
                                    animate={{
                                        y: isDragActive ? -5 : 0,
                                        scale: isDragActive ? 1.1 : 1,
                                    }}
                                    className={`
                    w-16 h-16 rounded-2xl flex items-center justify-center mb-4
                    ${isDragActive
                                            ? "bg-purple-500 text-white"
                                            : "bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400"
                                        }
                  `}
                                >
                                    <Upload className="w-8 h-8" />
                                </motion.div>

                                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                                    {isDragActive ? "Drop your file here" : "Drag & drop your file"}
                                </h3>
                                <p className="text-gray-500 dark:text-gray-400 mb-4">
                                    or click to browse from your computer
                                </p>
                                <p className="text-sm text-gray-400 dark:text-gray-500">
                                    Supports CSV, XLS, XLSX (max 10MB)
                                </p>
                            </div>
                        </div>
                    </motion.div>
                ) : (
                    <motion.div
                        key="file-preview"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                    >
                        <Card glass className="p-6">
                            <div className="flex items-start gap-4">
                                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center flex-shrink-0">
                                    <FileSpreadsheet className="w-7 h-7 text-white" />
                                </div>

                                <div className="flex-1 min-w-0">
                                    <div className="flex items-start justify-between gap-4">
                                        <div className="min-w-0">
                                            <h4 className="font-semibold text-gray-900 dark:text-white truncate">
                                                {file.name}
                                            </h4>
                                            <p className="text-sm text-gray-500 dark:text-gray-400">
                                                {formatFileSize(file.size)}
                                            </p>
                                        </div>

                                        {status === "idle" && (
                                            <button
                                                onClick={removeFile}
                                                className="p-1 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 transition-colors"
                                            >
                                                <X className="w-5 h-5" />
                                            </button>
                                        )}
                                    </div>

                                    {/* Status Indicator */}
                                    <div className="mt-4">
                                        {status === "idle" && (
                                            <Button onClick={handleUpload} className="w-full">
                                                <Upload className="w-4 h-4 mr-2" />
                                                Upload & Analyze
                                            </Button>
                                        )}

                                        {(status === "uploading" || status === "processing") && (
                                            <div className="space-y-3">
                                                <Progress value={progress} />
                                                <div className="flex items-center gap-2 text-sm text-purple-600 dark:text-purple-400">
                                                    <Loader2 className="w-4 h-4 animate-spin" />
                                                    {status === "uploading"
                                                        ? "Uploading file..."
                                                        : "Processing and analyzing data..."}
                                                </div>
                                            </div>
                                        )}

                                        {status === "success" && (
                                            <div className="flex items-center gap-2 text-sm text-green-600 dark:text-green-400">
                                                <CheckCircle2 className="w-5 h-5" />
                                                <span>Analysis complete! Redirecting...</span>
                                            </div>
                                        )}

                                        {status === "error" && (
                                            <div className="space-y-3">
                                                <div className="flex items-center gap-2 text-sm text-red-600 dark:text-red-400">
                                                    <AlertCircle className="w-5 h-5" />
                                                    <span>{error}</span>
                                                </div>
                                                <Button onClick={handleUpload} variant="outline" className="w-full">
                                                    Try Again
                                                </Button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </Card>
                    </motion.div>
                )}
            </AnimatePresence>

            {error && !file && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 p-4 rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800"
                >
                    <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
                        <AlertCircle className="w-5 h-5 flex-shrink-0" />
                        <span className="text-sm">{error}</span>
                    </div>
                </motion.div>
            )}
        </div>
    );
}
