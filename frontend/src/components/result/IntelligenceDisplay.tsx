"use client";

import React, { memo } from "react";
import { motion } from "framer-motion";
import {
    Brain,
    AlertTriangle,
    CheckCircle,
    TrendingUp,
    Shield,
    Zap,
    Lock,
    BarChart3,
    Target,
    Settings2,
    Code,
    Package,
    GitBranch,
    AlertCircle,
    ArrowRight,
    Sparkles,
    Scale,
    Layers,
    Database,
    Cpu,
    Crown,
} from "lucide-react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import Link from "next/link";

interface IntelligenceData {
    why_this_matters?: Array<{ finding: string; why: string; action: string }>;
    data_leakage_basic?: { has_leakage_risk: boolean; warnings: any[] };
    class_imbalance?: Record<string, any>;
    outlier_flag?: { has_outliers: boolean; total_columns_affected: number; details: any[] };
    executive_summary?: string[];
    confidence_scores?: Record<string, { score: number; explanation: string; label?: string }>;
    tradeoff_analysis?: any[];
    baseline_model?: { task_type: string; recommended: any; alternatives: any[] };
    metric_sensitivity?: Record<string, any>;
    assumption_checker?: Record<string, any>;
    outlier_strategy?: { strategy: string; message: string; confidence: number };
    high_impact_features?: Array<{ feature: string; impact_score: number; reason: string }>;
    model_preprocessing_advice?: Record<string, any>;
    scaling_impact?: any;
    encoding_recommendation?: Record<string, any>;
    feature_importance_preview?: any[];
    train_serve_consistency?: { consistent: boolean; issues: any[] };
    preprocessing_pipeline?: { code: string; description: string };
    saved_artifacts_info?: any;
    reproducibility_lock?: any;
    risky_features?: any[];
    feature_interactions?: any[];
    deployment_readiness?: { score: number; status: string; color: string; issues: string[] };
    drift_risk?: any;
    schema_alerts?: any;
    versioned_pipeline?: any;
    inference_cost?: any;
    model_impact_confidence?: Record<string, { score: number; explanation: string; label?: string }>;
}

interface IntelligenceDisplayProps {
    intelligence: IntelligenceData;
    userTier: string;
}

// Memoized components for performance
const FeatureCard = memo(({
    title,
    icon: Icon,
    children,
    locked = false,
    tier = "pro"
}: {
    title: string;
    icon: React.ElementType;
    children: React.ReactNode;
    locked?: boolean;
    tier?: string;
}) => (
    <Card className={cn(
        "p-5 relative overflow-hidden transition-all duration-300",
        locked && "opacity-60"
    )}>
        {locked && (
            <div className="absolute inset-0 bg-gradient-to-t from-gray-900/80 to-transparent flex items-end justify-center pb-4 z-10">
                <Link href="/pricing">
                    <Button size="sm" className="gap-2">
                        <Crown className="w-4 h-4" />
                        Upgrade to {tier}
                    </Button>
                </Link>
            </div>
        )}
        <div className="flex items-center gap-2 mb-3">
            <div className="p-2 rounded-lg bg-purple-100 dark:bg-purple-900/30">
                <Icon className="w-4 h-4 text-purple-600" />
            </div>
            <h4 className="font-semibold text-sm">{title}</h4>
            {locked && <Lock className="w-3 h-3 text-amber-500 ml-auto" />}
        </div>
        {children}
    </Card>
));

FeatureCard.displayName = "FeatureCard";

// Confidence Score Meter
const ConfidenceMeter = memo(({ score, label }: { score: number; label: string }) => (
    <div className="flex items-center gap-3">
        <div className="flex-1">
            <div className="flex justify-between text-xs mb-1">
                <span className="text-gray-500">{label}</span>
                <span className="font-bold text-purple-600">{score}%</span>
            </div>
            <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${score}%` }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    className={cn(
                        "h-full rounded-full",
                        score >= 80 && "bg-green-500",
                        score >= 60 && score < 80 && "bg-amber-500",
                        score < 60 && "bg-red-500"
                    )}
                />
            </div>
        </div>
    </div>
));

ConfidenceMeter.displayName = "ConfidenceMeter";

// Main Component
const IntelligenceDisplay = memo(({ intelligence, userTier }: IntelligenceDisplayProps) => {
    const isStarter = userTier === "starter" || userTier === "pro" || userTier === "enterprise";
    const isPro = userTier === "pro" || userTier === "enterprise";
    const isEnterprise = userTier === "enterprise";

    if (!intelligence || Object.keys(intelligence).length === 0) {
        return null;
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="space-y-6"
        >
            {/* Section Header */}
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 rounded-xl bg-gradient-to-br from-purple-500 to-indigo-600">
                    <Brain className="w-6 h-6 text-white" />
                </div>
                <div>
                    <h2 className="text-xl font-bold">ML Intelligence</h2>
                    <p className="text-sm text-gray-500">
                        Tier: <Badge variant={isPro ? "pro" : "default"}>{userTier.toUpperCase()}</Badge>
                    </p>
                </div>
            </div>

            {/* ============ FREE TIER FEATURES ============ */}

            {/* Executive Summary */}
            {intelligence.executive_summary && intelligence.executive_summary.length > 0 && (
                <FeatureCard title="Executive Summary" icon={BarChart3}>
                    <ul className="space-y-2">
                        {intelligence.executive_summary.map((point, idx) => (
                            <li key={idx} className="text-sm text-gray-600 dark:text-gray-300 flex items-start gap-2">
                                <span>{point}</span>
                            </li>
                        ))}
                    </ul>
                </FeatureCard>
            )}

            {/* Why This Matters */}
            {intelligence.why_this_matters && intelligence.why_this_matters.length > 0 && (
                <FeatureCard title="Why This Matters" icon={Sparkles}>
                    <div className="space-y-3">
                        {intelligence.why_this_matters.map((item, idx) => (
                            <div key={idx} className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                                <div className="font-medium text-sm text-purple-700 dark:text-purple-300 mb-1">
                                    {item.finding}
                                </div>
                                <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">{item.why}</p>
                                <div className="flex items-center gap-1 text-xs text-purple-600">
                                    <ArrowRight className="w-3 h-3" />
                                    {item.action}
                                </div>
                            </div>
                        ))}
                    </div>
                </FeatureCard>
            )}

            {/* Data Leakage Detection */}
            {intelligence.data_leakage_basic && (
                <FeatureCard title="Data Leakage Detection" icon={AlertTriangle}>
                    {intelligence.data_leakage_basic.has_leakage_risk ? (
                        <div className="space-y-2">
                            <Badge variant="destructive" className="mb-2">⚠️ Leakage Risk Detected</Badge>
                            {intelligence.data_leakage_basic.warnings.map((warn, idx) => (
                                <div key={idx} className="text-xs p-2 bg-red-50 dark:bg-red-900/20 rounded">
                                    <span className="font-medium">{warn.column}:</span> {warn.warning}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="flex items-center gap-2 text-green-600">
                            <CheckCircle className="w-4 h-4" />
                            <span className="text-sm">No obvious leakage risks detected</span>
                        </div>
                    )}
                </FeatureCard>
            )}

            {/* Class Imbalance */}
            {intelligence.class_imbalance && Object.keys(intelligence.class_imbalance).length > 0 && (
                <FeatureCard title="Class Imbalance" icon={Scale}>
                    <div className="space-y-2">
                        {Object.entries(intelligence.class_imbalance).map(([col, info]: [string, any]) => (
                            <div key={col} className={cn(
                                "p-2 rounded text-xs",
                                info.is_imbalanced ? "bg-amber-50 dark:bg-amber-900/20" : "bg-green-50 dark:bg-green-900/20"
                            )}>
                                <span className="font-medium">{col}:</span> {info.ratio}
                                {info.is_imbalanced && (
                                    <span className="text-amber-600 ml-2">⚠️ Imbalanced</span>
                                )}
                            </div>
                        ))}
                    </div>
                </FeatureCard>
            )}

            {/* Outlier Flag */}
            {intelligence.outlier_flag && (
                <FeatureCard title="Outlier Detection" icon={AlertCircle}>
                    {intelligence.outlier_flag.has_outliers ? (
                        <div>
                            <Badge variant="outline" className="mb-2 text-amber-600 border-amber-600">
                                {intelligence.outlier_flag.total_columns_affected} columns with outliers
                            </Badge>
                            <div className="grid grid-cols-2 gap-2 mt-2">
                                {intelligence.outlier_flag.details.slice(0, 4).map((d, idx) => (
                                    <div key={idx} className="text-xs p-2 bg-gray-50 dark:bg-gray-800 rounded">
                                        <span className="font-medium">{d.column}:</span> {d.count} ({d.percentage}%)
                                    </div>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <div className="flex items-center gap-2 text-green-600">
                            <CheckCircle className="w-4 h-4" />
                            <span className="text-sm">No significant outliers</span>
                        </div>
                    )}
                </FeatureCard>
            )}

            {/* ============ STARTER TIER FEATURES ============ */}

            {/* Confidence Scores */}
            <FeatureCard title="Data Reliability Scores" icon={TrendingUp} locked={!isStarter} tier="Starter">
                {isStarter && intelligence.confidence_scores ? (
                    <div className="space-y-3">
                        {Object.entries(intelligence.confidence_scores).map(([key, val]) => (
                            <ConfidenceMeter key={key} score={val.score} label={val.label || key.replace(/_/g, ' ')} />
                        ))}
                    </div>
                ) : (
                    <div className="h-16" />
                )}
            </FeatureCard>

            {/* Baseline Model */}
            <FeatureCard title="Recommended Model" icon={Target} locked={!isStarter} tier="Starter">
                {isStarter && intelligence.baseline_model ? (
                    <div>
                        <div className="flex items-center gap-2 mb-3">
                            <Badge>{intelligence.baseline_model.task_type}</Badge>
                        </div>
                        <div className="p-3 bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/20 dark:to-indigo-900/20 rounded-lg mb-3">
                            <div className="font-bold text-purple-700 dark:text-purple-300">
                                {intelligence.baseline_model.recommended.model}
                            </div>
                            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                                {intelligence.baseline_model.recommended.reason}
                            </p>
                            <div className="mt-2">
                                <ConfidenceMeter score={intelligence.baseline_model.recommended.confidence} label="Confidence" />
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="h-20" />
                )}
            </FeatureCard>

            {/* High Impact Features */}
            <FeatureCard title="High Impact Features" icon={Zap} locked={!isStarter} tier="Starter">
                {isStarter && intelligence.high_impact_features ? (
                    <div className="space-y-2">
                        {intelligence.high_impact_features.map((feat, idx) => (
                            <div key={idx} className="flex items-center gap-3">
                                <div className={cn(
                                    "w-8 h-8 rounded-lg flex items-center justify-center font-bold text-white",
                                    idx === 0 && "bg-amber-500",
                                    idx === 1 && "bg-gray-400",
                                    idx === 2 && "bg-amber-700"
                                )}>
                                    #{idx + 1}
                                </div>
                                <div className="flex-1">
                                    <div className="font-medium text-sm">{feat.feature}</div>
                                    <div className="text-xs text-gray-500">Score: {feat.impact_score}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="h-24" />
                )}
            </FeatureCard>

            {/* Trade-off Analysis */}
            <FeatureCard title="Trade-off Analysis" icon={Scale} locked={!isStarter} tier="Starter">
                {isStarter && intelligence.tradeoff_analysis && intelligence.tradeoff_analysis.length > 0 ? (
                    <div className="space-y-4">
                        {intelligence.tradeoff_analysis.slice(0, 2).map((tradeoff, idx) => (
                            <div key={idx} className="border-l-2 border-purple-500 pl-3">
                                <div className="font-medium text-sm mb-2">{tradeoff.decision}</div>
                                <div className="grid grid-cols-2 gap-2 text-xs">
                                    <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded">
                                        <div className="font-medium text-blue-700 dark:text-blue-300">{tradeoff.option_a.name}</div>
                                        <div className="text-green-600">✓ {tradeoff.option_a.pros[0]}</div>
                                        <div className="text-red-600">✗ {tradeoff.option_a.cons[0]}</div>
                                    </div>
                                    <div className="p-2 bg-indigo-50 dark:bg-indigo-900/20 rounded">
                                        <div className="font-medium text-indigo-700 dark:text-indigo-300">{tradeoff.option_b.name}</div>
                                        <div className="text-green-600">✓ {tradeoff.option_b.pros[0]}</div>
                                        <div className="text-red-600">✗ {tradeoff.option_b.cons[0]}</div>
                                    </div>
                                </div>
                                <div className="mt-2 text-xs text-purple-600">
                                    → Recommended: {tradeoff.recommendation === "option_a" ? tradeoff.option_a.name : tradeoff.option_b.name}
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="h-32" />
                )}
            </FeatureCard>

            {/* ============ PRO TIER FEATURES ============ */}

            {/* Model-Specific Preprocessing */}
            <FeatureCard title="Model-Specific Preprocessing" icon={Settings2} locked={!isPro} tier="Pro">
                {isPro && intelligence.model_preprocessing_advice ? (
                    <div className="space-y-3">
                        {Object.entries(intelligence.model_preprocessing_advice).slice(0, 3).map(([model, advice]: [string, any]) => (
                            <details key={model} className="group">
                                <summary className="cursor-pointer text-sm font-medium text-purple-600 flex items-center gap-2">
                                    <span>{model.replace(/_/g, ' ')}</span>
                                    <ArrowRight className="w-3 h-3 group-open:rotate-90 transition-transform" />
                                </summary>
                                <div className="mt-2 text-xs space-y-1 text-gray-600 dark:text-gray-400 ml-4">
                                    <div>• Scaling: {advice.scaling}</div>
                                    <div>• Encoding: {advice.encoding}</div>
                                    <div>• Missing: {advice.missing_values}</div>
                                </div>
                            </details>
                        ))}
                    </div>
                ) : (
                    <div className="h-24" />
                )}
            </FeatureCard>

            {/* Model Impact Confidence (Pro only) */}
            <FeatureCard title="Model Impact Confidence" icon={TrendingUp} locked={!isPro} tier="Pro">
                {isPro && intelligence.model_impact_confidence ? (
                    <div className="space-y-3">
                        <p className="text-xs text-gray-500 mb-2">How confident are we this will improve model metrics?</p>
                        {Object.entries(intelligence.model_impact_confidence).map(([key, val]) => (
                            <ConfidenceMeter key={key} score={val.score} label={val.label || key.replace(/_/g, ' ')} />
                        ))}
                    </div>
                ) : (
                    <div className="h-20" />
                )}
            </FeatureCard>

            {/* Feature Priority (Pre-training) - renamed from feature_importance_preview */}
            <FeatureCard title="Feature Priority (Pre-training)" icon={Target} locked={!isPro} tier="Pro">
                {isPro && intelligence.feature_importance_preview ? (
                    <div>
                        <p className="text-xs text-gray-500 mb-3">Heuristic ranking based on data characteristics, not model training.</p>
                        <div className="space-y-2">
                            {intelligence.feature_importance_preview.slice(0, 5).map((feat: any, idx: number) => (
                                <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded">
                                    <span className="text-sm font-medium">{feat.feature}</span>
                                    <div className="flex items-center gap-2">
                                        <Badge variant={feat.interpretation === 'high' ? 'default' : 'outline'} className="text-xs">
                                            {feat.interpretation}
                                        </Badge>
                                        <span className="text-xs text-gray-500">{feat.importance_score}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div className="h-24" />
                )}
            </FeatureCard>

            {/* Interaction Candidates - renamed from feature_interactions */}
            <FeatureCard title="Potential Interaction Candidates" icon={Layers} locked={!isPro} tier="Pro">
                {isPro && intelligence.feature_interactions && intelligence.feature_interactions.length > 0 ? (
                    <div>
                        <p className="text-xs text-amber-600 mb-3">⚠️ These are suggestions based on correlation patterns, not guaranteed to improve models.</p>
                        <div className="space-y-2">
                            {intelligence.feature_interactions.slice(0, 3).map((interaction: any, idx: number) => (
                                <div key={idx} className="p-2 bg-purple-50 dark:bg-purple-900/20 rounded text-xs">
                                    <div className="font-medium text-purple-700 dark:text-purple-300">
                                        {interaction.features[0]} × {interaction.features[1]}
                                    </div>
                                    <div className="text-gray-500 mt-1">{interaction.reason}</div>
                                    <code className="text-xs bg-gray-100 dark:bg-gray-800 px-1 rounded mt-1 inline-block">
                                        {interaction.code}
                                    </code>
                                </div>
                            ))}
                        </div>
                    </div>
                ) : isPro ? (
                    <div className="text-sm text-gray-500">No interaction candidates found</div>
                ) : (
                    <div className="h-24" />
                )}
            </FeatureCard>

            {/* Encoding Recommendations */}
            <FeatureCard title="Encoding Recommendations" icon={Layers} locked={!isPro} tier="Pro">
                {isPro && intelligence.encoding_recommendation ? (
                    <div className="space-y-2 max-h-48 overflow-y-auto">
                        {Object.entries(intelligence.encoding_recommendation).slice(0, 5).map(([col, rec]: [string, any]) => (
                            <div key={col} className="flex items-center justify-between text-xs p-2 bg-gray-50 dark:bg-gray-800 rounded">
                                <span className="font-medium truncate max-w-[120px]">{col}</span>
                                <Badge variant="outline" className="text-xs">{rec.encoding}</Badge>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="h-20" />
                )}
            </FeatureCard>

            {/* Preprocessing Pipeline */}
            <FeatureCard title="sklearn Pipeline" icon={Code} locked={!isPro} tier="Pro">
                {isPro && intelligence.preprocessing_pipeline ? (
                    <div>
                        <p className="text-xs text-gray-500 mb-2">{intelligence.preprocessing_pipeline.description}</p>
                        <pre className="text-xs bg-gray-900 text-gray-100 p-3 rounded-lg overflow-x-auto max-h-40">
                            {intelligence.preprocessing_pipeline.code}
                        </pre>
                        <Button size="sm" variant="outline" className="mt-2 text-xs" onClick={() => {
                            navigator.clipboard.writeText(intelligence.preprocessing_pipeline?.code || '');
                        }}>
                            Copy Code
                        </Button>
                    </div>
                ) : (
                    <div className="h-32" />
                )}
            </FeatureCard>

            {/* Risky Features */}
            <FeatureCard title="Risky Features" icon={AlertTriangle} locked={!isPro} tier="Pro">
                {isPro && intelligence.risky_features && intelligence.risky_features.length > 0 ? (
                    <div className="space-y-2">
                        {intelligence.risky_features.map((risk, idx) => (
                            <div key={idx} className={cn(
                                "p-2 rounded text-xs",
                                risk.risk_level === "high" ? "bg-red-50 dark:bg-red-900/20" : "bg-amber-50 dark:bg-amber-900/20"
                            )}>
                                <div className="font-medium flex items-center gap-2">
                                    {risk.feature}
                                    <Badge variant={risk.risk_level === "high" ? "destructive" : "outline"} className="text-xs">
                                        {risk.risk_level}
                                    </Badge>
                                </div>
                                <div className="text-gray-600 dark:text-gray-400 mt-1">
                                    Issues: {risk.issues.join(", ")}
                                </div>
                            </div>
                        ))}
                    </div>
                ) : isPro ? (
                    <div className="flex items-center gap-2 text-green-600">
                        <CheckCircle className="w-4 h-4" />
                        <span className="text-sm">No risky features detected</span>
                    </div>
                ) : (
                    <div className="h-20" />
                )}
            </FeatureCard>

            {/* Train-Serve Consistency */}
            <FeatureCard title="Production Readiness" icon={Database} locked={!isPro} tier="Pro">
                {isPro && intelligence.train_serve_consistency ? (
                    <div>
                        {intelligence.train_serve_consistency.consistent ? (
                            <div className="flex items-center gap-2 text-green-600 mb-2">
                                <CheckCircle className="w-5 h-5" />
                                <span className="font-medium">Ready for production</span>
                            </div>
                        ) : (
                            <div className="space-y-2">
                                <Badge variant="outline" className="text-amber-600 border-amber-600">
                                    {intelligence.train_serve_consistency.issues.length} issues found
                                </Badge>
                                {intelligence.train_serve_consistency.issues.slice(0, 3).map((issue, idx) => (
                                    <div key={idx} className="text-xs p-2 bg-amber-50 dark:bg-amber-900/20 rounded">
                                        <span className="font-medium">{issue.column}:</span> {issue.warning}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="h-20" />
                )}
            </FeatureCard>

            {/* ============ ENTERPRISE TIER FEATURES ============ */}

            {/* Deployment Readiness */}
            <FeatureCard title="Deployment Score" icon={Cpu} locked={!isEnterprise} tier="Enterprise">
                {isEnterprise && intelligence.deployment_readiness ? (
                    <div className="text-center">
                        <div className={cn(
                            "text-4xl font-bold mb-2",
                            intelligence.deployment_readiness.color === "green" && "text-green-600",
                            intelligence.deployment_readiness.color === "yellow" && "text-amber-600",
                            intelligence.deployment_readiness.color === "red" && "text-red-600"
                        )}>
                            {intelligence.deployment_readiness.score}%
                        </div>
                        <Badge className={cn(
                            intelligence.deployment_readiness.status === "ready" && "bg-green-500",
                            intelligence.deployment_readiness.status === "needs_work" && "bg-amber-500",
                            intelligence.deployment_readiness.status === "not_ready" && "bg-red-500"
                        )}>
                            {intelligence.deployment_readiness.status.replace(/_/g, ' ')}
                        </Badge>
                    </div>
                ) : (
                    <div className="h-24" />
                )}
            </FeatureCard>

        </motion.div>
    );
});

IntelligenceDisplay.displayName = "IntelligenceDisplay";

export default IntelligenceDisplay;
