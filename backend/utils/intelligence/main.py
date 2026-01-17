"""
Main Intelligence Orchestrator
Combines all modules and handles tier-based feature gating
"""

import pandas as pd
from typing import Dict, Any

from .data_quality import DataQualityAnalyzer
from .model_advice import ModelAdvisor
from .production_checks import ProductionChecker


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
        
        # Initialize analyzers
        self.quality = DataQualityAnalyzer(df)
        self.advisor = ModelAdvisor(df, self.quality.has_significant_outliers)
        self.production = ProductionChecker(df)
    
    def analyze(self) -> Dict[str, Any]:
        """Run all analyses based on tier."""
        result = {}
        
        # ============ FREE TIER ============
        result["why_this_matters"] = self.quality.why_this_matters_basic()
        result["data_leakage_basic"] = self.quality.detect_leakage_basic()
        result["class_imbalance"] = self.quality.detect_class_imbalance()
        result["outlier_flag"] = self.quality.outlier_presence_flag()
        result["executive_summary"] = self.quality.executive_summary_basic()
        
        if self.tier == "free":
            return result
        
        # ============ STARTER TIER ============
        result["confidence_scores"] = self.advisor.confidence_scores()
        result["tradeoff_analysis"] = self.advisor.tradeoff_analysis_light()
        result["baseline_model"] = self.advisor.suggest_baseline_model()
        result["metric_sensitivity"] = self.advisor.metric_sensitivity_basic()
        result["assumption_checker"] = self.advisor.assumption_checker_basic()
        result["outlier_strategy"] = self.advisor.outlier_strategy_suggestion()
        result["high_impact_features"] = self.advisor.high_impact_features()
        
        if self.tier == "starter":
            return result
        
        # ============ PRO TIER ============
        result["model_impact_confidence"] = self.advisor.model_impact_confidence()
        result["model_preprocessing_advice"] = self.advisor.model_specific_preprocessing()
        result["scaling_impact"] = self.advisor.scaling_impact_per_model()
        result["encoding_recommendation"] = self.advisor.encoding_choice_recommendation()
        result["feature_importance_preview"] = self.advisor.feature_importance_heuristic()
        result["feature_interactions"] = self.advisor.feature_interaction_hints()
        
        result["train_serve_consistency"] = self.production.train_serve_consistency_check()
        result["preprocessing_pipeline"] = self.production.exportable_preprocessing_pipeline()
        result["saved_artifacts_info"] = self.production.saved_artifacts_info()
        result["reproducibility_lock"] = self.production.reproducibility_lock()
        result["risky_features"] = self.production.risky_features_flag()
        
        if self.tier == "pro":
            return result
        
        # ============ ENTERPRISE TIER ============
        result["deployment_readiness"] = self.production.deployment_readiness_score()
        result["drift_risk"] = self.production.data_drift_risk()
        result["schema_alerts"] = self.production.schema_change_alerts()
        result["versioned_pipeline"] = self.production.versioned_pipeline_export()
        result["inference_cost"] = self.production.inference_cost_estimation()
        
        return result
