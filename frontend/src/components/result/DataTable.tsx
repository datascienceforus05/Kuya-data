"use client";

import React from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table } from "lucide-react";

interface DataTableProps {
    data: Record<string, unknown>[];
    title?: string;
}

export function DataTable({ data, title = "Cleaned Data Preview" }: DataTableProps) {
    if (!data || data.length === 0) {
        return null;
    }

    const columns = Object.keys(data[0]);

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
        >
            <Card glass>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Table className="w-5 h-5 text-purple-500" />
                        {title}
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700">
                                    {columns.map((col) => (
                                        <th
                                            key={col}
                                            className="px-4 py-3 text-left font-semibold text-gray-700 dark:text-gray-300 whitespace-nowrap"
                                        >
                                            {col}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {data.map((row, idx) => (
                                    <tr
                                        key={idx}
                                        className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/30 transition-colors"
                                    >
                                        {columns.map((col) => (
                                            <td
                                                key={col}
                                                className="px-4 py-3 text-gray-600 dark:text-gray-400 whitespace-nowrap"
                                            >
                                                {row[col] !== null && row[col] !== undefined
                                                    ? String(row[col])
                                                    : "-"}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <p className="mt-3 text-sm text-gray-500 dark:text-gray-400 text-center">
                        Showing first {data.length} rows of cleaned data
                    </p>
                </CardContent>
            </Card>
        </motion.div>
    );
}
