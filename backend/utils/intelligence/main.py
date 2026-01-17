"""
Main Intelligence Orchestrator
==============================
Purpose:
    - Combine all intelligence modules
    - Handle tier-based feature gating
    - ZERO logic here, only orchestration

Rules:
    - If logic creeps into this file, refactor immediately
    - Each tier adds features, never removes
    - All actual analysis happens in submodules
"""

import pandas as pd
from typing import Dict, Any

from .data_quality import DataQualityAnalyzer
from .model_advice import ModelAdvisor
from .production_checks import ProductionChecker


# Tier levels for clean comparisons
TIER_FREE = 0
TIER_STARTER = 1
TIER_PRO = 2
TIER_ENTERPRISE = 3

TIER_MAP = {
    "free": TIER_FREE,
    "starter": TIER_STARTER,
    "pro": TIER_PRO,
    "enterprise": TIER_ENTERPRISE
}


class DataIntelligence:
    """
    Advanced data intelligence engine with tier-based features.
    
    Tiers:
    - free: Basic insights only
    - starter: Learning features
    - pro: Professional ML features
    - enterprise: Full production features
    """
    
    def __init__(self, df: pd.DataFrame, tier: str = "free"):
        self.df = df
        self.tier = tier
        self.tier_level = TIER_MAP.get(tier.lower(), TIER_FREE)
        
        # Initialize analyzers
        self.quality = DataQualityAnalyzer(df)
        self.advisor = ModelAdvisor(df, self.quality.has_significant_outliers)
        self.production = ProductionChecker(df)
    
    def analyze(self) -> Dict[str, Any]:
        """
        Run all analyses based on tier.
        Pure orchestration - no logic here.
        """
        result = {}
        
        # ============ FREE TIER ============
        if self.tier_level >= TIER_FREE:
            result.update(self._run_free_tier())
        
        # ============ STARTER TIER ============
        if self.tier_level >= TIER_STARTER:
            result.update(self._run_starter_tier())
        
        # ============ PRO TIER ============
        if self.tier_level >= TIER_PRO:
            result.update(self._run_pro_tier())
        
        # ============ ENTERPRISE TIER ============
        if self.tier_level >= TIER_ENTERPRISE:
            result.update(self._run_enterprise_tier())
        
        return result
    
    def _run_free_tier(self) -> Dict[str, Any]:
        """Free tier: Basic data quality insights."""
        return {
            "why_this_matters": self.quality.why_this_matters_basic(),
            "data_leakage_basic": self.quality.detect_leakage_basic(),
            "class_imbalance": self.quality.detect_class_imbalance(),
            "outlier_flag": self.quality.outlier_presence_flag(),
            "executive_summary": self.quality.executive_summary_basic(),
        }
    
    def _run_starter_tier(self) -> Dict[str, Any]:
        """Starter tier: Learning-focused features."""
        return {
            "confidence_scores": self.advisor.confidence_scores(),
            "tradeoff_analysis": self.advisor.tradeoff_analysis_light(),
            "baseline_model": self.advisor.suggest_baseline_model(),
            "metric_sensitivity": self.advisor.metric_sensitivity_basic(),
            "assumption_checker": self.advisor.assumption_checker_basic(),
            "outlier_strategy": self.advisor.outlier_strategy_suggestion(),
            "high_impact_features": self.advisor.high_impact_features(),
        }
    
    def _run_pro_tier(self) -> Dict[str, Any]:
        """Pro tier: Professional ML features."""
        return {
            # Model advice (Pro)
            "model_impact_confidence": self.advisor.model_impact_confidence(),
            "model_preprocessing_advice": self.advisor.model_specific_preprocessing(),
            "scaling_impact": self.advisor.scaling_impact_per_model(),
            "encoding_recommendation": self.advisor.encoding_choice_recommendation(),
            "feature_importance_preview": self.advisor.feature_importance_heuristic(),
            "feature_interactions": self.advisor.feature_interaction_hints(),
            # Production checks (Pro)
            "train_serve_consistency": self.production.train_serve_consistency_check(),
            "preprocessing_pipeline": self.production.exportable_preprocessing_pipeline(),
            "saved_artifacts_info": self.production.saved_artifacts_info(),
            "reproducibility_lock": self.production.reproducibility_lock(),
            "risky_features": self.production.risky_features_flag(),
        }
    
    def _run_enterprise_tier(self) -> Dict[str, Any]:
        """Enterprise tier: Full production features."""
        return {
            "deployment_readiness": self.production.deployment_readiness_score(),
            "drift_risk": self.production.data_drift_risk(),
            "schema_alerts": self.production.schema_change_alerts(),
            "versioned_pipeline": self.production.versioned_pipeline_export(),
            "inference_cost": self.production.inference_cost_estimation(),
        }
