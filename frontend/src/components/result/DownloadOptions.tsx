"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { Download, FileText, FileSpreadsheet, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface DownloadOptionsProps {
    reportId: string;
    onDownloadCSV?: () => void;
}

export function DownloadOptions({ reportId, onDownloadCSV }: DownloadOptionsProps) {
    const [downloadingPDF, setDownloadingPDF] = useState(false);
    const [downloadingCSV, setDownloadingCSV] = useState(false);

    const handlePDFDownload = async () => {
        setDownloadingPDF(true);
        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/report/${reportId}`
            );

            if (!response.ok) throw new Error("Failed to download PDF");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `report-${reportId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error("PDF download error:", error);
        } finally {
            setDownloadingPDF(false);
        }
    };

    const handleCSVDownload = async () => {
        setDownloadingCSV(true);
        try {
            if (onDownloadCSV) {
                onDownloadCSV();
            }
        } finally {
            setTimeout(() => setDownloadingCSV(false), 1000);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
        >
            <Card glass>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Download className="w-5 h-5 text-purple-500" />
                        Download Options
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <Button
                            variant="outline"
                            size="lg"
                            className="h-auto py-4 flex-col gap-2"
                            onClick={handleCSVDownload}
                            disabled={downloadingCSV}
                        >
                            {downloadingCSV ? (
                                <Loader2 className="w-6 h-6 animate-spin" />
                            ) : (
                                <FileSpreadsheet className="w-6 h-6 text-green-600" />
                            )}
                            <div className="text-center">
                                <p className="font-semibold">Download CSV</p>
                                <p className="text-xs text-gray-500">Cleaned data file</p>
                            </div>
                        </Button>

                        <Button
                            size="lg"
                            className="h-auto py-4 flex-col gap-2"
                            onClick={handlePDFDownload}
                            disabled={downloadingPDF}
                        >
                            {downloadingPDF ? (
                                <Loader2 className="w-6 h-6 animate-spin" />
                            ) : (
                                <FileText className="w-6 h-6" />
                            )}
                            <div className="text-center">
                                <p className="font-semibold">Download PDF</p>
                                <p className="text-xs text-purple-200">Full analysis report</p>
                            </div>
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </motion.div>
    );
}
