"use client";

import React, { useEffect, useState } from "react";
import {
    CreditCard,
    Search,
    RefreshCcw,
    Calendar,
    Filter,
    DollarSign,
    TrendingUp,
    Clock,
    ExternalLink,
    Download
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

interface Payment {
    _id: string;
    email: string;
    paidAt: string;
    paymentId: string;
    orderId: string;
    plan: string;
    amount: number;
}

export default function AdminPaymentsPage() {
    const [payments, setPayments] = useState<Payment[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [timeFilter, setTimeFilter] = useState<"all" | "today" | "month">("all");

    const fetchPayments = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem("admin_token");
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/payments`, {
                headers: { "x-admin-token": token || "" }
            });
            if (response.ok) {
                const data = await response.json();
                setPayments(data);
            }
        } catch (error) {
            toast.error("Failed to fetch payment history");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPayments();
    }, []);

    const filteredPayments = payments.filter(p => {
        const matchesSearch = p.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
            p.paymentId.toLowerCase().includes(searchTerm.toLowerCase());

        if (timeFilter === "all") return matchesSearch;

        const paidDate = new Date(p.paidAt);
        const now = new Date();

        if (timeFilter === "today") {
            return matchesSearch && paidDate.toDateString() === now.toDateString();
        }

        if (timeFilter === "month") {
            return matchesSearch && paidDate.getMonth() === now.getMonth() && paidDate.getFullYear() === now.getFullYear();
        }

        return matchesSearch;
    });

    const totalRevenue = filteredPayments.reduce((acc, p) => acc + p.amount, 0);

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
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold font-display">Financial Logistics</h1>
                    <p className="text-gray-500 text-sm">Track subscriptions and incoming revenue streams</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => handleExport("payments")}>
                        <Download className="w-4 h-4 mr-2" />
                        Export CSV
                    </Button>
                    <Button variant="outline" size="sm" onClick={fetchPayments} disabled={loading}>
                        <RefreshCcw className={loading ? "animate-spin mr-2" : "mr-2"} size={16} />
                        Synchronize
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="p-6 bg-gradient-to-br from-green-500/10 to-emerald-500/10 border-green-200 dark:border-green-900/30">
                    <div className="flex items-center gap-4 mb-2">
                        <div className="p-2 rounded-lg bg-green-100 dark:bg-green-900/40 text-green-600">
                            <DollarSign size={20} />
                        </div>
                        <span className="text-sm font-medium text-gray-500">Filtered Revenue</span>
                    </div>
                    <div className="text-3xl font-bold">₹{totalRevenue.toLocaleString()}</div>
                    <p className="text-xs text-green-600 mt-1 flex items-center gap-1">
                        <TrendingUp size={12} />
                        Based on {filteredPayments.length} transactions
                    </p>
                </Card>

                <Card className="p-6">
                    <div className="flex items-center gap-4 mb-2">
                        <div className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/40 text-blue-600">
                            <Clock size={20} />
                        </div>
                        <span className="text-sm font-medium text-gray-500">Waitlist/Pending</span>
                    </div>
                    <div className="text-3xl font-bold text-gray-400">0</div>
                    <p className="text-xs text-gray-400 mt-1">All transactions cleared</p>
                </Card>

                <Card className="p-6">
                    <div className="flex items-center gap-4 mb-2">
                        <div className="p-2 rounded-lg bg-orange-100 dark:bg-orange-900/40 text-orange-600">
                            <CreditCard size={20} />
                        </div>
                        <span className="text-sm font-medium text-gray-500">Av. Transaction</span>
                    </div>
                    <div className="text-3xl font-bold">₹499</div>
                    <p className="text-xs text-orange-600 mt-1">Standard Pro pricing</p>
                </Card>
            </div>

            <Card className="p-4 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border-gray-200 dark:border-gray-700">
                <div className="flex flex-col md:flex-row gap-4">
                    <div className="flex-1 flex items-center gap-3 bg-white dark:bg-gray-900 border rounded-xl px-4 py-2">
                        <Search className="text-gray-400" size={20} />
                        <input
                            type="text"
                            placeholder="Search by email or transaction ID..."
                            className="flex-1 bg-transparent border-none outline-none text-sm"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="flex gap-2">
                        <Button
                            variant={timeFilter === "all" ? "default" : "outline"}
                            size="sm"
                            onClick={() => setTimeFilter("all")}
                            className="px-4"
                        >
                            All Time
                        </Button>
                        <Button
                            variant={timeFilter === "today" ? "default" : "outline"}
                            size="sm"
                            onClick={() => setTimeFilter("today")}
                            className="px-4"
                        >
                            Today
                        </Button>
                        <Button
                            variant={timeFilter === "month" ? "default" : "outline"}
                            size="sm"
                            onClick={() => setTimeFilter("month")}
                            className="px-4"
                        >
                            This Month
                        </Button>
                    </div>
                </div>
            </Card>

            <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
                <table className="w-full text-sm text-left">
                    <thead className="bg-gray-50 dark:bg-gray-900/50 text-gray-500 font-medium">
                        <tr>
                            <th className="px-6 py-4">Customer</th>
                            <th className="px-6 py-4">Transaction Details</th>
                            <th className="px-6 py-4">Amount</th>
                            <th className="px-6 py-4">Date & Time</th>
                            <th className="px-6 py-4">Status</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 dark:divide-gray-800 bg-white dark:bg-gray-800/50">
                        {loading ? (
                            <tr><td colSpan={5} className="py-20 text-center text-gray-400">Fetching logs...</td></tr>
                        ) : filteredPayments.length === 0 ? (
                            <tr><td colSpan={5} className="py-20 text-center text-gray-400">No payment records found for this period</td></tr>
                        ) : (
                            filteredPayments.map((p) => (
                                <tr key={p._id} className="hover:bg-gray-50/50 dark:hover:bg-gray-700/30 transition-colors">
                                    <td className="px-6 py-4 font-medium">{p.email}</td>
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col">
                                            <span className="text-xs text-gray-400 font-mono">CF-ID: {p.paymentId}</span>
                                            <span className="text-[10px] text-gray-400">Order: {p.orderId}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 font-bold text-green-600 text-lg">
                                        ₹{p.amount}
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col text-xs">
                                            <span>{new Date(p.paidAt).toLocaleDateString()}</span>
                                            <span className="text-gray-400">{new Date(p.paidAt).toLocaleTimeString()}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <Badge className="bg-green-100 text-green-700 border-green-200">
                                            PAID
                                        </Badge>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
