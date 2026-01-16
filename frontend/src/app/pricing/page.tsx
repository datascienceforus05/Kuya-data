"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useSession, signIn } from "next-auth/react";
import {
    Check,
    Sparkles,
    Zap,
    Shield,
    Crown,
    Loader2,
    X,
    Building2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { load } from "@cashfreepayments/cashfree-js";

const plans = [
    {
        id: "free",
        name: "Free",
        description: "Perfect for trying out Kuya Cloud",
        price: "₹0",
        amount: 0,
        period: "forever",
        dataLimit: "3 analyses/month",
        features: [
            { text: "3 file analyses per month", included: true },
            { text: "Basic data cleaning", included: true },
            { text: "Summary statistics", included: true },
            { text: "Missing values analysis", included: true },
            { text: "CSV download only", included: true },
            { text: "Max 5MB file size", included: true },
            { text: "Advanced charts", included: false },
            { text: "PDF reports", included: false },
            { text: "AI insights", included: false },
        ],
        cta: "Current Plan",
        popular: false,
    },
    {
        id: "starter",
        name: "Starter",
        description: "For individuals & freelancers",
        price: "₹199",
        amount: 199,
        period: "/month",
        dataLimit: "15 analyses/month",
        features: [
            { text: "15 file analyses per month", included: true },
            { text: "Advanced data cleaning", included: true },
            { text: "Full EDA & correlations", included: true },
            { text: "All chart types", included: true },
            { text: "CSV & Excel download", included: true },
            { text: "Max 25MB file size", included: true },
            { text: "Quality score & health", included: true },
            { text: "Email support", included: true },
            { text: "AI insights", included: false },
        ],
        cta: "Get Starter",
        popular: false,
    },
    {
        id: "pro",
        name: "Pro",
        description: "For professionals & teams",
        price: "₹399",
        amount: 399,
        period: "/month",
        dataLimit: "30 analyses/month",
        features: [
            { text: "30 file analyses per month", included: true },
            { text: "Advanced data cleaning", included: true },
            { text: "Full EDA & correlations", included: true },
            { text: "All charts + Pair plots", included: true },
            { text: "CSV, Excel & PDF download", included: true },
            { text: "Max 50MB file size", included: true },
            { text: "AI-powered insights", included: true },
            { text: "Feature importance", included: true },
            { text: "Priority support", included: true },
        ],
        cta: "Upgrade to Pro",
        popular: true,
    },
    {
        id: "enterprise",
        name: "Enterprise",
        description: "For large teams & organizations",
        price: "Custom",
        amount: 0,
        period: "",
        dataLimit: "Unlimited analyses",
        features: [
            { text: "Unlimited file analyses", included: true },
            { text: "Everything in Pro", included: true },
            { text: "No file size limit", included: true },
            { text: "Custom integrations", included: true },
            { text: "API access", included: true },
            { text: "Dedicated support", included: true },
            { text: "Custom branding", included: true },
            { text: "SLA guarantee", included: true },
            { text: "Training & onboarding", included: true },
        ],
        cta: "Contact Sales",
        popular: false,
        isEnterprise: true,
    },
];

const faqs = [
    {
        question: "Can I cancel anytime?",
        answer:
            "Yes, you can cancel your subscription at any time. You will retain access until the end of your billing period.",
    },
    {
        question: "What payment methods do you accept?",
        answer:
            "We accept all major credit cards, debit cards, UPI, net banking, and wallets through Cashfree Payments.",
    },
    {
        question: "Is my data secure?",
        answer:
            "Absolutely. All data is encrypted in transit and at rest. We never share your data with third parties.",
    },
    {
        question: "Do you offer refunds?",
        answer:
            "Yes, we offer a 7-day money-back guarantee if you're not satisfied.",
    },
    {
        question: "What's the difference between plans?",
        answer:
            "Each plan offers more analyses per month and additional features. Free: 3/month, Starter: 15/month, Pro: 30/month with AI insights.",
    },
];

export default function PricingPage() {
    const { data: session } = useSession();
    const [loading, setLoading] = useState<string | null>(null);
    const [showPhoneModal, setShowPhoneModal] = useState(false);
    const [phoneNumber, setPhoneNumber] = useState("");
    const [selectedPlan, setSelectedPlan] = useState<typeof plans[0] | null>(null);
    const [cashfree, setCashfree] = useState<any>(null);
    const [error, setError] = useState<string | null>(null);
    const [userPlan, setUserPlan] = useState<string>("free");

    useEffect(() => {
        if (session?.user?.email) {
            fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/user/${encodeURIComponent(session.user.email)}`)
                .then(res => res.json())
                .then(data => {
                    if (data.plan) setUserPlan(data.plan);
                })
                .catch(err => console.error("Failed to fetch user plan:", err));
        }
    }, [session]);

    // Initialize Cashfree SDK
    useEffect(() => {
        const initCashfree = async () => {
            try {
                const mode = process.env.NEXT_PUBLIC_CASHFREE_MODE === "production" ? "production" : "sandbox";
                const cf = await load({
                    mode: mode,
                });
                setCashfree(cf);
            } catch (err) {
                console.error("Failed to load Cashfree:", err);
            }
        };
        initCashfree();
    }, []);

    const handleUpgrade = async (plan: typeof plans[0]) => {
        if (!session) {
            signIn("google");
            return;
        }

        if (plan.id === "free") return;

        if (plan.isEnterprise) {
            window.location.href = "mailto:mebishnusahu0595@gmail.com?subject=Kuya%20Cloud%20Enterprise%20Inquiry";
            return;
        }

        setSelectedPlan(plan);
        setShowPhoneModal(true);
    };

    const handlePayment = async () => {
        if (!phoneNumber || phoneNumber.length < 10 || !selectedPlan) {
            setError("Please enter a valid phone number");
            return;
        }

        setLoading(selectedPlan.id);
        setError(null);

        try {
            const response = await fetch("/api/payment/create-order", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    customerEmail: session?.user?.email,
                    customerName: session?.user?.name,
                    customerPhone: phoneNumber.startsWith("+91") ? phoneNumber : `+91${phoneNumber}`,
                    amount: selectedPlan.amount,
                    planId: selectedPlan.id,
                    planName: selectedPlan.name,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Failed to create order");
            }

            // Open Cashfree checkout
            if (cashfree && data.paymentSessionId) {
                const checkoutOptions = {
                    paymentSessionId: data.paymentSessionId,
                    redirectTarget: "_modal",
                };

                cashfree.checkout(checkoutOptions).then((result: any) => {
                    if (result.error) {
                        setError(result.error.message);
                    }
                    if (result.paymentDetails) {
                        console.log("Payment successful:", result.paymentDetails);
                        window.location.href = `/upgrade-success?order_id=${data.orderId}&plan=${selectedPlan.id}`;
                    }
                });
            }
        } catch (err) {
            console.error("Payment error:", err);
            setError(err instanceof Error ? err.message : "Payment failed");
        } finally {
            setLoading(null);
        }
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
                        Simple & Transparent Pricing
                    </span>
                    <h1 className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold mb-6">
                        Choose Your{" "}
                        <span className="gradient-text">Plan</span>
                    </h1>
                    <p className="text-lg text-gray-600 dark:text-gray-400">
                        Start free with 3 analyses per month. Upgrade when you need more power.
                    </p>
                </motion.div>

                {/* Pricing Cards */}
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto mb-16">
                    {plans.map((plan, idx) => (
                        <motion.div
                            key={plan.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 * idx }}
                        >
                            <Card
                                glass
                                className={cn(
                                    "p-6 h-full relative transition-all duration-300 flex flex-col",
                                    plan.popular
                                        ? "border-purple-500 shadow-glow scale-105 z-10"
                                        : "hover:border-purple-500/30",
                                    plan.isEnterprise && "border-amber-500/50"
                                )}
                            >
                                {plan.popular && (
                                    <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                                        <Badge variant="pro" className="flex items-center gap-1">
                                            <Zap className="w-3 h-3" />
                                            Most Popular
                                        </Badge>
                                    </div>
                                )}

                                {plan.isEnterprise && (
                                    <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                                        <Badge className="flex items-center gap-1 bg-amber-500 text-white">
                                            <Building2 className="w-3 h-3" />
                                            Enterprise
                                        </Badge>
                                    </div>
                                )}

                                <div className="text-center mb-6">
                                    <h3 className="text-xl font-display font-bold mb-1">
                                        {plan.name}
                                    </h3>
                                    <p className="text-gray-600 dark:text-gray-400 text-xs mb-4">
                                        {plan.description}
                                    </p>
                                    <div className="flex items-baseline justify-center gap-1 mb-2">
                                        <span className={cn(
                                            "font-display font-bold",
                                            plan.isEnterprise ? "text-2xl" : "text-3xl"
                                        )}>
                                            {plan.price}
                                        </span>
                                        {plan.period && (
                                            <span className="text-gray-500 dark:text-gray-400 text-sm">
                                                {plan.period}
                                            </span>
                                        )}
                                    </div>
                                    <Badge variant="outline" className="text-xs">
                                        {plan.dataLimit}
                                    </Badge>
                                </div>

                                <ul className="space-y-2 mb-6 flex-grow">
                                    {plan.features.map((feature, fidx) => (
                                        <li key={fidx} className="flex items-start gap-2">
                                            <div className={cn(
                                                "w-4 h-4 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5",
                                                feature.included
                                                    ? "bg-green-100 dark:bg-green-900/30"
                                                    : "bg-gray-100 dark:bg-gray-800"
                                            )}>
                                                {feature.included ? (
                                                    <Check className="w-2.5 h-2.5 text-green-600 dark:text-green-400" />
                                                ) : (
                                                    <X className="w-2.5 h-2.5 text-gray-400" />
                                                )}
                                            </div>
                                            <span className={cn(
                                                "text-sm",
                                                feature.included
                                                    ? "text-gray-700 dark:text-gray-300"
                                                    : "text-gray-400 dark:text-gray-500"
                                            )}>
                                                {feature.text}
                                            </span>
                                        </li>
                                    ))}
                                </ul>

                                <Button
                                    variant={plan.id === userPlan ? "secondary" : (plan.popular ? "default" : "outline")}
                                    size="lg"
                                    className={cn(
                                        "w-full mt-auto",
                                        plan.isEnterprise && plan.id !== userPlan && "border-amber-500 text-amber-600 hover:bg-amber-50",
                                        plan.id === userPlan && "bg-green-50 text-green-700 border-green-200 hover:bg-green-50 dark:bg-green-900/20 dark:text-green-400 dark:border-green-900 cursor-default opacity-100"
                                    )}
                                    onClick={() => plan.id !== userPlan && handleUpgrade(plan)}
                                    disabled={loading === plan.id || (plan.id === userPlan)}
                                >
                                    {loading === plan.id ? (
                                        <Loader2 className="w-4 h-4 animate-spin mr-2" />
                                    ) : plan.id === userPlan ? (
                                        <Check className="w-4 h-4 mr-2" />
                                    ) : plan.popular ? (
                                        <Crown className="w-4 h-4 mr-2" />
                                    ) : plan.isEnterprise ? (
                                        <Building2 className="w-4 h-4 mr-2" />
                                    ) : null}
                                    {plan.id === userPlan ? "Active Plan" : plan.cta}
                                </Button>
                            </Card>
                        </motion.div>
                    ))}
                </div>

                {/* Comparison Table */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="mb-16"
                >
                    <h2 className="text-2xl font-display font-bold text-center mb-8">
                        Compare Plans
                    </h2>
                    <div className="overflow-x-auto">
                        <table className="w-full max-w-4xl mx-auto text-sm">
                            <thead>
                                <tr className="border-b dark:border-gray-700">
                                    <th className="text-left py-4 px-4">Feature</th>
                                    <th className="text-center py-4 px-4">Free</th>
                                    <th className="text-center py-4 px-4">Starter</th>
                                    <th className="text-center py-4 px-4 bg-purple-50 dark:bg-purple-900/20">Pro</th>
                                    <th className="text-center py-4 px-4">Enterprise</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr className="border-b dark:border-gray-800">
                                    <td className="py-3 px-4 font-medium">Analyses/Month</td>
                                    <td className="text-center py-3 px-4">3</td>
                                    <td className="text-center py-3 px-4">15</td>
                                    <td className="text-center py-3 px-4 bg-purple-50 dark:bg-purple-900/20 font-bold">30</td>
                                    <td className="text-center py-3 px-4">Unlimited</td>
                                </tr>
                                <tr className="border-b dark:border-gray-800">
                                    <td className="py-3 px-4 font-medium">Max File Size</td>
                                    <td className="text-center py-3 px-4">5MB</td>
                                    <td className="text-center py-3 px-4">25MB</td>
                                    <td className="text-center py-3 px-4 bg-purple-50 dark:bg-purple-900/20 font-bold">50MB</td>
                                    <td className="text-center py-3 px-4">Unlimited</td>
                                </tr>
                                <tr className="border-b dark:border-gray-800">
                                    <td className="py-3 px-4 font-medium">Export Formats</td>
                                    <td className="text-center py-3 px-4">CSV</td>
                                    <td className="text-center py-3 px-4">CSV, Excel</td>
                                    <td className="text-center py-3 px-4 bg-purple-50 dark:bg-purple-900/20 font-bold">All + PDF</td>
                                    <td className="text-center py-3 px-4">All + API</td>
                                </tr>
                                <tr className="border-b dark:border-gray-800">
                                    <td className="py-3 px-4 font-medium">AI Insights</td>
                                    <td className="text-center py-3 px-4"><X className="w-4 h-4 text-gray-400 mx-auto" /></td>
                                    <td className="text-center py-3 px-4"><X className="w-4 h-4 text-gray-400 mx-auto" /></td>
                                    <td className="text-center py-3 px-4 bg-purple-50 dark:bg-purple-900/20"><Check className="w-4 h-4 text-green-500 mx-auto" /></td>
                                    <td className="text-center py-3 px-4"><Check className="w-4 h-4 text-green-500 mx-auto" /></td>
                                </tr>
                                <tr className="border-b dark:border-gray-800">
                                    <td className="py-3 px-4 font-medium">Support</td>
                                    <td className="text-center py-3 px-4">Community</td>
                                    <td className="text-center py-3 px-4">Email</td>
                                    <td className="text-center py-3 px-4 bg-purple-50 dark:bg-purple-900/20 font-bold">Priority</td>
                                    <td className="text-center py-3 px-4">Dedicated</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </motion.div>

                {/* FAQs */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="max-w-3xl mx-auto"
                >
                    <h2 className="text-2xl font-display font-bold text-center mb-8">
                        Frequently Asked Questions
                    </h2>
                    <div className="space-y-4">
                        {faqs.map((faq, idx) => (
                            <Card key={idx} glass className="p-6">
                                <h3 className="font-semibold mb-2">{faq.question}</h3>
                                <p className="text-gray-600 dark:text-gray-400 text-sm">
                                    {faq.answer}
                                </p>
                            </Card>
                        ))}
                    </div>
                </motion.div>

                {/* Security Badge */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6 }}
                    className="text-center mt-12"
                >
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gray-100 dark:bg-gray-800">
                        <Shield className="w-4 h-4 text-green-600" />
                        <span className="text-sm text-gray-600 dark:text-gray-400">
                            Secure payments powered by Cashfree
                        </span>
                    </div>
                </motion.div>
            </div>

            {/* Phone Number Modal */}
            {showPhoneModal && selectedPlan && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-white dark:bg-gray-900 rounded-2xl p-6 max-w-md w-full"
                    >
                        <div className="text-center mb-6">
                            <div className="w-16 h-16 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Crown className="w-8 h-8 text-purple-600" />
                            </div>
                            <h3 className="text-xl font-bold mb-2">Upgrade to {selectedPlan.name}</h3>
                            <p className="text-gray-600 dark:text-gray-400">
                                {selectedPlan.price}{selectedPlan.period} • {selectedPlan.dataLimit}
                            </p>
                        </div>

                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium mb-2">
                                    Phone Number (for payment)
                                </label>
                                <div className="flex gap-2">
                                    <span className="px-3 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm">
                                        +91
                                    </span>
                                    <Input
                                        type="tel"
                                        placeholder="9876543210"
                                        value={phoneNumber}
                                        onChange={(e) => setPhoneNumber(e.target.value.replace(/\D/g, "").slice(0, 10))}
                                        className="flex-1"
                                    />
                                </div>
                            </div>

                            {error && (
                                <p className="text-red-500 text-sm">{error}</p>
                            )}

                            <Button
                                className="w-full"
                                size="lg"
                                onClick={handlePayment}
                                disabled={loading !== null}
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="w-4 h-4 animate-spin mr-2" />
                                        Processing...
                                    </>
                                ) : (
                                    <>Pay {selectedPlan.price}</>
                                )}
                            </Button>

                            <Button
                                variant="ghost"
                                className="w-full"
                                onClick={() => {
                                    setShowPhoneModal(false);
                                    setSelectedPlan(null);
                                    setError(null);
                                }}
                            >
                                Cancel
                            </Button>
                        </div>
                    </motion.div>
                </div>
            )}
        </div>
    );
}
