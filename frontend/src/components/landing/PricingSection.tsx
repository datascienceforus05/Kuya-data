"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Check, Sparkles, Zap, Crown, Building2, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const plans = [
    {
        id: "free",
        name: "Free",
        description: "Perfect for trying out Kuya Cloud",
        price: "₹0",
        period: "forever",
        dataLimit: "3 analyses/month",
        features: [
            { text: "3 file analyses per month", included: true },
            { text: "Basic data cleaning", included: true },
            { text: "Summary statistics", included: true },
            { text: "Missing values analysis", included: true },
            { text: "CSV download only", included: true },
            { text: "Max 5MB file size", included: true },
            { text: "Community support", included: true },
            { text: "Advanced charts", included: false },
            { text: "PDF reports", included: false },
            { text: "AI insights", included: false },
        ],
        cta: "Get Started Free",
        popular: false,
        href: "/upload",
    },
    {
        id: "starter",
        name: "Starter",
        description: "For individuals & freelancers",
        price: "₹199",
        period: "/month",
        dataLimit: "15 analyses/month",
        features: [
            { text: "15 file analyses per month", included: true },
            { text: "Advanced data cleaning", included: true },
            { text: "Full EDA & correlations", included: true },
            { text: "All chart types", included: true },
            { text: "CSV & Excel download", included: true },
            { text: "Max 25MB file size", included: true },
            { text: "Email support", included: true },
            { text: "Quality score & health", included: true },
            { text: "PDF reports", included: false },
            { text: "AI insights", included: false },
        ],
        cta: "Get Starter",
        popular: false,
        href: "/pricing",
        amount: 199,
    },
    {
        id: "pro",
        name: "Pro",
        description: "For professionals & teams",
        price: "₹399",
        period: "/month",
        dataLimit: "30 analyses/month",
        features: [
            { text: "30 file analyses per month", included: true },
            { text: "Advanced data cleaning", included: true },
            { text: "Full EDA & correlations", included: true },
            { text: "All chart types + Pair plots", included: true },
            { text: "CSV, Excel & PDF download", included: true },
            { text: "Max 50MB file size", included: true },
            { text: "Priority support", included: true },
            { text: "Quality score & health", included: true },
            { text: "AI-powered insights", included: true },
            { text: "Feature importance", included: true },
        ],
        cta: "Upgrade to Pro",
        popular: true,
        href: "/pricing",
        amount: 399,
    },
    {
        id: "enterprise",
        name: "Enterprise",
        description: "For large teams & organizations",
        price: "Custom",
        period: "",
        dataLimit: "Unlimited analyses",
        features: [
            { text: "Unlimited file analyses", included: true },
            { text: "Everything in Pro", included: true },
            { text: "No file size limit", included: true },
            { text: "Custom integrations", included: true },
            { text: "API access", included: true },
            { text: "Custom branding", included: true },
            { text: "Dedicated account manager", included: true },
            { text: "On-premise deployment", included: true },
            { text: "SLA guarantee", included: true },
            { text: "Training & onboarding", included: true },
        ],
        cta: "Contact Sales",
        popular: false,
        href: "mailto:mebishnusahu0595@gmail.com?subject=Kuya%20Cloud%20Enterprise%20Inquiry",
        isEnterprise: true,
    },
];

export function PricingSection() {
    return (
        <section className="py-24 relative overflow-hidden" id="pricing">
            {/* Background */}
            <div className="absolute inset-0 bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-900 -z-10" />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-500/5 rounded-full blur-3xl -z-10" />

            <div className="section-container">
                {/* Header */}
                <div className="text-center max-w-3xl mx-auto mb-16">
                    <motion.span
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-sm font-medium mb-6"
                    >
                        <Sparkles className="w-4 h-4" />
                        Simple & Transparent Pricing
                    </motion.span>
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.1 }}
                        className="text-3xl sm:text-4xl lg:text-5xl font-display font-bold mb-6"
                    >
                        Choose Your{" "}
                        <span className="gradient-text">Plan</span>
                    </motion.h2>
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.2 }}
                        className="text-lg text-gray-600 dark:text-gray-400"
                    >
                        Start free with 3 analyses per month. Upgrade when you need more power.
                    </motion.p>
                </div>

                {/* Pricing Cards */}
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
                    {plans.map((plan, idx) => (
                        <motion.div
                            key={plan.name}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
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

                                <Link href={plan.href} className="mt-auto">
                                    <Button
                                        variant={plan.popular ? "default" : plan.isEnterprise ? "outline" : "outline"}
                                        size="lg"
                                        className={cn(
                                            "w-full",
                                            plan.isEnterprise && "border-amber-500 text-amber-600 hover:bg-amber-50 dark:hover:bg-amber-900/20"
                                        )}
                                    >
                                        {plan.isEnterprise && <Building2 className="w-4 h-4 mr-2" />}
                                        {plan.popular && <Crown className="w-4 h-4 mr-2" />}
                                        {plan.cta}
                                    </Button>
                                </Link>
                            </Card>
                        </motion.div>
                    ))}
                </div>

                {/* FAQ / Note */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="text-center mt-12"
                >
                    <p className="text-gray-500 dark:text-gray-400 text-sm">
                        All plans include SSL encryption & secure data handling.
                        <br />
                        Questions? Email us at <a href="mailto:mebishnusahu0595@gmail.com" className="text-purple-600 hover:underline">mebishnusahu0595@gmail.com</a>
                    </p>
                </motion.div>
            </div>
        </section>
    );
}
