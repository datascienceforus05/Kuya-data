"use client";

import React, { useEffect, useState } from "react";
import {
    Search,
    ArrowUpDown,
    MoreVertical,
    UserPlus,
    Shield,
    Zap,
    Rocket,
    RefreshCcw,
    Mail,
    Calendar,
    Layers,
    Download
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from "@/components/ui/dropdown-menu";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

interface User {
    _id: string;
    email: string;
    plan: string;
    planLimit: number;
    usedThisMonth: number;
    createdAt: string;
    lastLogin?: string;
    paymentId?: string;
}

export default function UserManagementPage() {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");

    const fetchUsers = async () => {
        setLoading(true);
        try {
            const token = localStorage.getItem("admin_token");
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/users`, {
                headers: { "x-admin-token": token || "" }
            });
            if (response.ok) {
                const data = await response.json();
                setUsers(data);
            } else {
                toast.error("Failed to load users");
            }
        } catch (error) {
            toast.error("Error connecting to server");
        } finally {
            setLoading(false);
        }
    };

    const upgradeUser = async (email: string, plan: string, limit?: number) => {
        try {
            const token = localStorage.getItem("admin_token");
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/upgrade-user`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "x-admin-token": token || ""
                },
                body: JSON.stringify({ email, plan, limit })
            });

            if (response.ok) {
                toast.success(`User upgraded to ${plan.toUpperCase()}`);
                fetchUsers();
            } else {
                toast.error("Plan update failed");
            }
        } catch (error) {
            toast.error("Network error during upgrade");
        }
    };

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

    useEffect(() => {
        fetchUsers();
    }, []);

    const filteredUsers = users.filter(user =>
        user.email.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold font-display">User Management</h1>
                    <p className="text-gray-500 text-sm">Monitor and manage user accounts and subscriptions</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => handleExport("users")}>
                        <Download className="w-4 h-4 mr-2" />
                        Export CSV
                    </Button>
                    <Button variant="outline" size="sm" onClick={fetchUsers} disabled={loading}>
                        <RefreshCcw className={loading ? "animate-spin mr-2" : "mr-2"} size={16} />
                        Refresh
                    </Button>
                </div>
            </div>

            <Card className="p-4 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm border-gray-200 dark:border-gray-700">
                <div className="flex items-center gap-3 bg-white dark:bg-gray-900 border rounded-xl px-4 py-2 focus-within:ring-2 ring-purple-500/20 transition-all">
                    <Search className="text-gray-400" size={20} />
                    <input
                        type="text"
                        placeholder="Search users by email..."
                        className="flex-1 bg-transparent border-none outline-none text-sm"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </Card>

            <div className="overflow-x-auto rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
                <table className="w-full text-sm text-left">
                    <thead className="bg-gray-50 dark:bg-gray-900/50 text-gray-500 font-medium">
                        <tr>
                            <th className="px-6 py-4">User Details</th>
                            <th className="px-6 py-4">Subscription</th>
                            <th className="px-6 py-4">Usage</th>
                            <th className="px-6 py-4">Registered</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100 dark:divide-gray-800 bg-white dark:bg-gray-800/50">
                        {loading && users.length === 0 ? (
                            <tr><td colSpan={5} className="py-20 text-center text-gray-400">Loading user database...</td></tr>
                        ) : filteredUsers.length === 0 ? (
                            <tr><td colSpan={5} className="py-20 text-center text-gray-400">No users found match your search</td></tr>
                        ) : (
                            filteredUsers.map((user) => (
                                <tr key={user._id} className="hover:bg-gray-50/50 dark:hover:bg-gray-700/30 transition-colors">
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-3">
                                            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-100 to-indigo-100 dark:from-purple-900/40 dark:to-indigo-900/40 flex items-center justify-center text-purple-600 font-bold">
                                                {user.email[0].toUpperCase()}
                                            </div>
                                            <div className="flex flex-col">
                                                <span className="font-semibold text-gray-900 dark:text-gray-100 truncate max-w-[200px]">{user.email}</span>
                                                <span className="text-xs text-gray-500 flex items-center gap-1">
                                                    <Shield size={10} className="text-gray-400" />
                                                    ID: {user._id.slice(-6)}
                                                </span>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col gap-1">
                                            <Badge className={cn(
                                                "w-fit px-2 py-0 text-[10px] uppercase font-bold",
                                                user.plan === "pro" && "bg-purple-100 text-purple-700 hover:bg-purple-200 border-purple-200",
                                                user.plan === "starter" && "bg-blue-100 text-blue-700 hover:bg-blue-200 border-blue-200",
                                                user.plan === "enterprise" && "bg-amber-100 text-amber-700 hover:bg-amber-200 border-amber-200",
                                                user.plan === "free" && "bg-gray-100 text-gray-700 hover:bg-gray-200 border-gray-200",
                                            )}>
                                                {user.plan}
                                            </Badge>
                                            <span className="text-[10px] text-gray-500 font-mono">Limit: {user.planLimit === 999999 ? "∞" : user.planLimit} reports</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col gap-1">
                                            <div className="flex items-center justify-between gap-4">
                                                <span className="text-xs font-medium text-gray-700 dark:text-gray-300">{user.usedThisMonth} used</span>
                                                <span className="text-[10px] text-gray-400">
                                                    {user.planLimit > 0 ? ((user.usedThisMonth / user.planLimit) * 100).toFixed(0) : 0}%
                                                </span>
                                            </div>
                                            <div className="h-1.5 w-24 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-purple-500"
                                                    style={{ width: `${Math.min(100, (user.usedThisMonth / (user.planLimit || 1)) * 100)}%` }}
                                                />
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex flex-col gap-1">
                                            <span className="text-xs flex items-center gap-1 text-gray-600 dark:text-gray-400">
                                                <Calendar size={12} />
                                                {new Date(user.createdAt).toLocaleDateString()}
                                            </span>
                                            {user.lastLogin && (
                                                <span className="text-[10px] text-gray-400">Active {new Date(user.lastLogin).toLocaleTimeString()}</span>
                                            )}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <DropdownMenu>
                                            <DropdownMenuTrigger asChild>
                                                <Button variant="ghost" size="icon" className="h-8 w-8">
                                                    <MoreVertical size={16} />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end" className="w-48">
                                                <DropdownMenuLabel>Manage Access</DropdownMenuLabel>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem onClick={() => upgradeUser(user.email, "starter")}>
                                                    <Zap size={14} className="mr-2 text-blue-500" />
                                                    Set Starter Plan
                                                </DropdownMenuItem>
                                                <DropdownMenuItem onClick={() => upgradeUser(user.email, "pro")}>
                                                    <Rocket size={14} className="mr-2 text-purple-500" />
                                                    Set Pro Plan
                                                </DropdownMenuItem>
                                                <DropdownMenuItem onClick={() => upgradeUser(user.email, "enterprise")}>
                                                    <Shield size={14} className="mr-2 text-amber-500" />
                                                    Set Enterprise
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem onClick={() => upgradeUser(user.email, "free")}>
                                                    <RefreshCcw size={14} className="mr-2 text-gray-500" />
                                                    Revert to Free
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
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
