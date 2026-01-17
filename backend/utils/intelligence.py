"""
Intelligence Module - Advanced ML & Data Science Analysis Features
Tier-based feature set for Kuya Cloud
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


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
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
    def analyze(self) -> Dict[str, Any]:
        """Run all analyses based on tier."""
        result = {}
        
        # ============ FREE TIER ============
        result["why_this_matters"] = self._why_this_matters_basic()
        result["data_leakage_basic"] = self._detect_leakage_basic()
        result["class_imbalance"] = self._detect_class_imbalance()
        result["outlier_flag"] = self._outlier_presence_flag()
        result["executive_summary"] = self._executive_summary_basic()
        
        if self.tier == "free":
            return result
            
        # ============ STARTER TIER ============
        result["confidence_scores"] = self._confidence_scores()
        result["tradeoff_analysis"] = self._tradeoff_analysis_light()
        result["baseline_model"] = self._suggest_baseline_model()
        result["metric_sensitivity"] = self._metric_sensitivity_basic()
        result["assumption_checker"] = self._assumption_checker_basic()
        result["outlier_strategy"] = self._outlier_strategy_suggestion()
        result["high_impact_features"] = self._high_impact_features()
        
        if self.tier == "starter":
            return result
            
        # ============ PRO TIER ============
        result["model_impact_confidence"] = self._model_impact_confidence()  # Pro-only model confidence
        result["model_preprocessing_advice"] = self._model_specific_preprocessing()
        result["scaling_impact"] = self._scaling_impact_per_model()
        result["encoding_recommendation"] = self._encoding_choice_recommendation()
        result["feature_importance_preview"] = self._feature_importance_heuristic()
        result["train_serve_consistency"] = self._train_serve_consistency_check()
        result["preprocessing_pipeline"] = self._exportable_preprocessing_pipeline()
        result["saved_artifacts_info"] = self._saved_artifacts_info()
        result["reproducibility_lock"] = self._reproducibility_lock()
        result["risky_features"] = self._risky_features_flag()
        result["feature_interactions"] = self._feature_interaction_hints()
        
        if self.tier == "pro":
            return result
            
        # ============ ENTERPRISE TIER ============
        result["deployment_readiness"] = self._deployment_readiness_score()
        result["drift_risk"] = self._data_drift_risk()
        result["schema_alerts"] = self._schema_change_alerts()
        result["versioned_pipeline"] = self._versioned_pipeline_export()
        result["inference_cost"] = self._inference_cost_estimation()
        
        return result
    
    # ==================== FREE TIER FEATURES ====================
    
    def _why_this_matters_basic(self) -> List[Dict[str, str]]:
        """Basic 1-line explanations for key findings."""
        insights = []
        
        # Missing values insight
        missing_pct = (self.df.isnull().sum().sum() / self.df.size) * 100
        if missing_pct > 0:
            insights.append({
                "finding": "Missing Values Detected",
                "why": f"Missing data ({missing_pct:.1f}%) can bias your model. Models like XGBoost handle this, but Linear Regression will fail.",
                "action": "Consider imputation or use tree-based models."
            })
        
        # High cardinality
        for col in self.categorical_cols:
            unique_ratio = self.df[col].nunique() / len(self.df)
            if unique_ratio > 0.5:
                insights.append({
                    "finding": f"High Cardinality: {col}",
                    "why": f"Column '{col}' has {self.df[col].nunique()} unique values. One-hot encoding will explode dimensions.",
                    "action": "Use target encoding or frequency encoding instead."
                })
                break  # Only show one in free tier
        
        # Skewed distribution
        for col in self.numeric_cols[:3]:  # Check first 3 numeric cols
            skewness = self.df[col].skew()
            if abs(skewness) > 2:
                insights.append({
                    "finding": f"Skewed Distribution: {col}",
                    "why": f"Skewness of {skewness:.2f} means outliers dominate. Linear models will be affected.",
                    "action": "Apply log transform or use robust scaling."
                })
                break
        
        return insights
    
    def _detect_leakage_basic(self) -> Dict[str, Any]:
        """Basic data leakage detection."""
        warnings_list = []
        
        # Check for ID-like columns that might leak
        for col in self.df.columns:
            col_lower = col.lower()
            if any(x in col_lower for x in ['id', 'index', 'key', 'timestamp', 'created', 'updated']):
                warnings_list.append({
                    "column": col,
                    "risk": "high" if 'id' in col_lower else "medium",
                    "warning": f"'{col}' looks like an identifier/timestamp. Including it may cause data leakage."
                })
        
        # Check for near-perfect correlations (potential target leakage)
        if len(self.numeric_cols) >= 2:
            corr_matrix = self.df[self.numeric_cols].corr()
            for i, col1 in enumerate(self.numeric_cols):
                for col2 in self.numeric_cols[i+1:]:
                    corr = abs(corr_matrix.loc[col1, col2])
                    if corr > 0.95:
                        warnings_list.append({
                            "column": f"{col1} ↔ {col2}",
                            "risk": "high",
                            "warning": f"Very high correlation ({corr:.2f}). One might be derived from target."
                        })
        
        return {
            "has_leakage_risk": len(warnings_list) > 0,
            "warnings": warnings_list[:3]  # Limit in free tier
        }
    
    def _detect_class_imbalance(self) -> Dict[str, Any]:
        """Detect class imbalance in potential target columns."""
        imbalance_info = {}
        
        for col in self.categorical_cols:
            if self.df[col].nunique() <= 10:  # Likely a target
                value_counts = self.df[col].value_counts(normalize=True)
                if len(value_counts) >= 2:
                    ratio = value_counts.iloc[0] / value_counts.iloc[-1]
                    if ratio > 3:
                        imbalance_info[col] = {
                            "is_imbalanced": True,
                            "ratio": f"{ratio:.1f}:1",
                            "majority_class": value_counts.index[0],
                            "minority_class": value_counts.index[-1],
                            "warning": "High imbalance! Accuracy will be misleading. Use F1-score or AUROC."
                        }
                    else:
                        imbalance_info[col] = {
                            "is_imbalanced": False,
                            "ratio": f"{ratio:.1f}:1"
                        }
        
        return imbalance_info
    
    def _outlier_presence_flag(self) -> Dict[str, Any]:
        """Simple yes/no outlier flag."""
        outlier_cols = []
        
        for col in self.numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < Q1 - 1.5 * IQR) | (self.df[col] > Q3 + 1.5 * IQR)).sum()
            if outliers > 0:
                outlier_cols.append({
                    "column": col,
                    "count": int(outliers),
                    "percentage": round(outliers / len(self.df) * 100, 1)
                })
        
        return {
            "has_outliers": len(outlier_cols) > 0,
            "total_columns_affected": len(outlier_cols),
            "details": outlier_cols[:5]  # Limit in free tier
        }
    
    def _executive_summary_basic(self) -> List[str]:
        """Very short executive summary (3-4 bullets)."""
        summary = []
        
        # Size
        summary.append(f"📊 Dataset has {len(self.df):,} rows and {len(self.df.columns)} columns.")
        
        # Data completeness
        completeness = (1 - self.df.isnull().sum().sum() / self.df.size) * 100
        if completeness >= 95:
            summary.append(f"✅ Data is {completeness:.1f}% complete - ready for analysis.")
        else:
            summary.append(f"⚠️ Data is only {completeness:.1f}% complete - consider handling missing values.")
        
        # Column types
        summary.append(f"🔢 {len(self.numeric_cols)} numeric, {len(self.categorical_cols)} categorical columns detected.")
        
        # Quick recommendation
        if len(self.numeric_cols) >= 3:
            summary.append("💡 Dataset suitable for regression or classification tasks.")
        
        return summary
    
    # ==================== STARTER TIER FEATURES ====================
    
    def _confidence_scores(self) -> Dict[str, Any]:
        """Confidence score for data reliability (Starter tier)."""
        scores = {}
        
        # Data quality confidence - "How reliable is this dataset?"
        completeness = (1 - self.df.isnull().sum().sum() / self.df.size) * 100
        consistency = 100 - (self.df.duplicated().sum() / len(self.df) * 100)
        scores["data_reliability"] = {
            "score": round((completeness + consistency) / 2, 1),
            "explanation": "How reliable is this dataset? Based on completeness and consistency.",
            "label": "Data Reliability"
        }
        
        # ML readiness (basic) - describes data suitability, not model impact
        readiness_score = 70  # Base score
        if completeness > 90:
            readiness_score += 15
        if len(self.numeric_cols) >= 3:
            readiness_score += 10
        if len(self.df) >= 100:
            readiness_score += 5
        scores["ml_suitability"] = {
            "score": min(readiness_score, 100),
            "explanation": "Is this data suitable for ML? Based on size and feature availability.",
            "label": "ML Suitability"
        }
        
        return scores
    
    def _model_impact_confidence(self) -> Dict[str, Any]:
        """Model impact confidence (Pro tier only) - will this improve metrics?"""
        scores = {}
        
        # Feature quality impact
        feature_score = 60
        if len(self.numeric_cols) >= 5:
            feature_score += 15
        if not self._has_significant_outliers():
            feature_score += 10
        if len(self.categorical_cols) <= 5:  # Not too many categoricals
            feature_score += 10
        scores["feature_quality_impact"] = {
            "score": min(feature_score, 100),
            "explanation": "How likely are these features to improve model performance?",
            "label": "Feature Quality Impact"
        }
        
        # Data volume impact
        n = len(self.df)
        volume_score = 50
        if n >= 1000:
            volume_score = 85
        elif n >= 500:
            volume_score = 75
        elif n >= 100:
            volume_score = 65
        scores["data_volume_impact"] = {
            "score": volume_score,
            "explanation": "Will this data volume support robust model training?",
            "label": "Data Volume Impact"
        }
        
        return scores
    
    def _tradeoff_analysis_light(self) -> List[Dict[str, Any]]:
        """Light trade-off analysis between options."""
        tradeoffs = []
        
        # Missing value handling
        missing_pct = (self.df.isnull().sum().sum() / self.df.size) * 100
        if missing_pct > 0:
            tradeoffs.append({
                "decision": "Missing Value Handling",
                "option_a": {
                    "name": "Drop rows with missing values",
                    "pros": ["Simple", "No bias introduced"],
                    "cons": [f"Lose {self.df.isnull().any(axis=1).sum()} rows ({self.df.isnull().any(axis=1).sum()/len(self.df)*100:.1f}%)"]
                },
                "option_b": {
                    "name": "Impute with median/mode",
                    "pros": ["Keep all data", "Works with most models"],
                    "cons": ["May introduce bias", "Reduces variance"]
                },
                "recommendation": "option_b" if missing_pct < 20 else "option_a"
            })
        
        # Scaling decision
        if len(self.numeric_cols) > 0:
            tradeoffs.append({
                "decision": "Feature Scaling",
                "option_a": {
                    "name": "StandardScaler (Z-score)",
                    "pros": ["Works with most algorithms", "Preserves outlier info"],
                    "cons": ["Affected by outliers"]
                },
                "option_b": {
                    "name": "RobustScaler",
                    "pros": ["Robust to outliers", "Better for skewed data"],
                    "cons": ["Less common", "May not suit all models"]
                },
                "recommendation": "option_b" if self._has_significant_outliers() else "option_a"
            })
        
        return tradeoffs
    
    def _has_significant_outliers(self) -> bool:
        """Helper to check for significant outliers."""
        for col in self.numeric_cols[:5]:
            Q1, Q3 = self.df[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            outlier_pct = ((self.df[col] < Q1 - 1.5 * IQR) | (self.df[col] > Q3 + 1.5 * IQR)).sum() / len(self.df)
            if outlier_pct > 0.05:  # More than 5% outliers
                return True
        return False
    
    def _suggest_baseline_model(self) -> Dict[str, Any]:
        """Suggest best starting model for this data."""
        suggestions = []
        
        # Analyze data characteristics
        n_samples = len(self.df)
        n_features = len(self.df.columns)
        has_categorical = len(self.categorical_cols) > 0
        has_missing = self.df.isnull().sum().sum() > 0
        
        # Classification vs Regression guess
        task_type = "classification"
        for col in self.categorical_cols:
            if self.df[col].nunique() <= 10:
                task_type = "classification"
                break
        else:
            task_type = "regression"
        
        if task_type == "classification":
            if n_samples < 1000:
                suggestions.append({
                    "model": "Random Forest Classifier",
                    "reason": "Best for small datasets, handles mixed types, no scaling needed",
                    "confidence": 85
                })
            else:
                suggestions.append({
                    "model": "XGBoost Classifier",
                    "reason": "Excellent performance on larger datasets, handles missing values",
                    "confidence": 90
                })
            
            suggestions.append({
                "model": "Logistic Regression",
                "reason": "Simple baseline, interpretable, good for linear relationships",
                "confidence": 70
            })
        else:
            suggestions.append({
                "model": "Random Forest Regressor",
                "reason": "Robust baseline, handles non-linearity, minimal preprocessing",
                "confidence": 85
            })
            suggestions.append({
                "model": "Linear Regression",
                "reason": "Interpretable baseline, check assumptions first",
                "confidence": 65
            })
        
        return {
            "task_type": task_type,
            "recommended": suggestions[0],
            "alternatives": suggestions[1:],
            "data_characteristics": {
                "samples": n_samples,
                "features": n_features,
                "has_categorical": has_categorical,
                "has_missing": has_missing
            }
        }
    
    def _metric_sensitivity_basic(self) -> Dict[str, Any]:
        """Basic metric sensitivity analysis."""
        sensitivity = {}
        
        # Check for imbalance
        is_imbalanced = False
        for col in self.categorical_cols:
            if self.df[col].nunique() <= 10:
                value_counts = self.df[col].value_counts(normalize=True)
                if len(value_counts) >= 2 and value_counts.iloc[0] / value_counts.iloc[-1] > 3:
                    is_imbalanced = True
                    break
        
        sensitivity["accuracy"] = {
            "reliability": "low" if is_imbalanced else "high",
            "warning": "Misleading with imbalanced data" if is_imbalanced else "Reliable for balanced data",
            "recommendation": "Use F1-score or AUROC instead" if is_imbalanced else "Good primary metric"
        }
        
        sensitivity["recall"] = {
            "reliability": "high",
            "warning": None,
            "recommendation": "Use when missing positives is costly (e.g., fraud detection)"
        }
        
        sensitivity["precision"] = {
            "reliability": "high",
            "warning": None,
            "recommendation": "Use when false positives are costly (e.g., spam detection)"
        }
        
        return sensitivity
    
    def _assumption_checker_basic(self) -> Dict[str, Any]:
        """Basic assumption checking for models."""
        checks = {}
        
        # Sample size check
        n = len(self.df)
        p = len(self.df.columns)
        checks["sample_size"] = {
            "status": "pass" if n >= 10 * p else "warning",
            "message": f"Rule of thumb: need 10x features ({10*p}) samples. You have {n}.",
            "recommendation": "Collect more data" if n < 10 * p else "Sample size adequate"
        }
        
        # Linearity check (basic)
        if len(self.numeric_cols) >= 2:
            correlations = self.df[self.numeric_cols].corr().abs()
            avg_corr = correlations.values[np.triu_indices_from(correlations.values, 1)].mean()
            checks["linearity"] = {
                "status": "pass" if avg_corr > 0.3 else "warning",
                "message": f"Average feature correlation: {avg_corr:.2f}",
                "recommendation": "Linear models may work" if avg_corr > 0.3 else "Consider non-linear models"
            }
        
        # Multicollinearity check
        if len(self.numeric_cols) >= 2:
            corr_matrix = self.df[self.numeric_cols].corr().abs()
            high_corr_pairs = []
            for i in range(len(self.numeric_cols)):
                for j in range(i+1, len(self.numeric_cols)):
                    if corr_matrix.iloc[i, j] > 0.8:
                        high_corr_pairs.append((self.numeric_cols[i], self.numeric_cols[j]))
            
            checks["multicollinearity"] = {
                "status": "warning" if high_corr_pairs else "pass",
                "message": f"{len(high_corr_pairs)} highly correlated feature pairs found",
                "pairs": high_corr_pairs[:3],
                "recommendation": "Consider removing one of each pair" if high_corr_pairs else "No issues"
            }
        
        return checks
    
    def _outlier_strategy_suggestion(self) -> Dict[str, Any]:
        """Suggest outlier handling strategy."""
        outlier_info = self._outlier_presence_flag()
        
        if not outlier_info["has_outliers"]:
            return {
                "strategy": "none",
                "message": "No significant outliers detected",
                "confidence": 90
            }
        
        total_outlier_pct = sum(d["percentage"] for d in outlier_info["details"]) / len(outlier_info["details"])
        
        if total_outlier_pct < 1:
            return {
                "strategy": "remove",
                "message": "Very few outliers (<1%). Safe to remove.",
                "code_snippet": "df = df[(np.abs(stats.zscore(df[numeric_cols])) < 3).all(axis=1)]",
                "confidence": 85
            }
        elif total_outlier_pct < 5:
            return {
                "strategy": "robust_model",
                "message": "Moderate outliers. Use robust models or scaling.",
                "options": ["Use RobustScaler", "Use tree-based models", "Winsorize at 1st/99th percentile"],
                "confidence": 80
            }
        else:
            return {
                "strategy": "investigate",
                "message": "Many outliers. Investigate data quality first.",
                "options": ["Check for data entry errors", "Consider log transform", "Use median-based metrics"],
                "confidence": 70
            }
    
    def _high_impact_features(self) -> List[Dict[str, Any]]:
        """Identify top 3 high-impact features."""
        impact_scores = {}
        
        for col in self.numeric_cols:
            # Score based on variance, missing values, and distribution
            variance_score = min(self.df[col].std() / (self.df[col].mean() + 1e-10), 2) * 30
            missing_penalty = (1 - self.df[col].isnull().sum() / len(self.df)) * 30
            unique_score = min(self.df[col].nunique() / len(self.df) * 100, 40)
            
            impact_scores[col] = variance_score + missing_penalty + unique_score
        
        # Sort and get top 3
        sorted_features = sorted(impact_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return [
            {
                "feature": feat,
                "impact_score": round(score, 1),
                "reason": "High variance and information content"
            }
            for feat, score in sorted_features
        ]
    
    # ==================== PRO TIER FEATURES ====================
    
    def _model_specific_preprocessing(self) -> Dict[str, Any]:
        """Model-specific preprocessing advice."""
        advice = {}
        
        advice["linear_regression"] = {
            "scaling": "Required - StandardScaler",
            "encoding": "OneHotEncoder for categorical",
            "missing_values": "Must impute - use median for numeric, mode for categorical",
            "feature_engineering": "Consider polynomial features for non-linear relationships",
            "warnings": ["Check for multicollinearity", "Normalize skewed features"]
        }
        
        advice["random_forest"] = {
            "scaling": "Not required",
            "encoding": "LabelEncoder or OrdinalEncoder sufficient",
            "missing_values": "Can handle naturally (but sklearn doesn't - impute anyway)",
            "feature_engineering": "Raw features work well",
            "warnings": ["Watch for high cardinality features", "May overfit small datasets"]
        }
        
        advice["xgboost"] = {
            "scaling": "Not required",
            "encoding": "Can handle categorical natively (enable_categorical=True)",
            "missing_values": "Handles missing values internally",
            "feature_engineering": "Focus on creating meaningful interactions",
            "warnings": ["Tune regularization to prevent overfitting"]
        }
        
        advice["logistic_regression"] = {
            "scaling": "Required - StandardScaler",
            "encoding": "OneHotEncoder (watch dimensionality)",
            "missing_values": "Must impute before training",
            "feature_engineering": "Consider interaction terms",
            "warnings": ["Class imbalance affects convergence", "Add regularization (L1/L2)"]
        }
        
        return advice
    
    def _scaling_impact_per_model(self) -> Dict[str, Any]:
        """Explain scaling impact per model type."""
        return {
            "high_impact": {
                "models": ["Linear Regression", "Logistic Regression", "SVM", "Neural Networks", "KNN"],
                "reason": "Distance/gradient-based algorithms are sensitive to feature scales",
                "recommendation": "Always scale features before training"
            },
            "low_impact": {
                "models": ["Random Forest", "XGBoost", "LightGBM", "Decision Trees"],
                "reason": "Tree-based models split on thresholds, not magnitudes",
                "recommendation": "Scaling optional but may help interpretability"
            },
            "your_data_recommendation": {
                "has_varied_scales": any(self.df[col].std() > 10 * self.df[self.numeric_cols].std().mean() for col in self.numeric_cols) if self.numeric_cols else False,
                "suggested_scaler": "RobustScaler" if self._has_significant_outliers() else "StandardScaler"
            }
        }
    
    def _encoding_choice_recommendation(self) -> Dict[str, Any]:
        """Recommend encoding strategies."""
        recommendations = {}
        
        for col in self.categorical_cols:
            cardinality = self.df[col].nunique()
            
            if cardinality <= 2:
                recommendations[col] = {
                    "encoding": "LabelEncoder / Binary",
                    "reason": f"Binary column ({cardinality} values)",
                    "code": f"df['{col}'] = df['{col}'].map({{'value1': 0, 'value2': 1}})"
                }
            elif cardinality <= 10:
                recommendations[col] = {
                    "encoding": "OneHotEncoder",
                    "reason": f"Low cardinality ({cardinality} values)",
                    "code": f"pd.get_dummies(df, columns=['{col}'])"
                }
            elif cardinality <= 50:
                recommendations[col] = {
                    "encoding": "Target Encoding",
                    "reason": f"Medium cardinality ({cardinality} values) - OneHot would create too many columns",
                    "code": f"# Use category_encoders.TargetEncoder"
                }
            else:
                recommendations[col] = {
                    "encoding": "Frequency / Hash Encoding",
                    "reason": f"High cardinality ({cardinality} values)",
                    "code": f"df['{col}'] = df['{col}'].map(df['{col}'].value_counts(normalize=True))"
                }
        
        return recommendations
    
    def _feature_importance_heuristic(self) -> List[Dict[str, Any]]:
        """Heuristic feature importance without training."""
        importance = []
        
        for col in self.numeric_cols:
            # Calculate heuristic importance based on:
            # 1. Variance (normalized)
            # 2. Correlation with other features
            # 3. Missing value ratio (penalize high missing)
            
            variance_score = min(self.df[col].std() / (self.df[self.numeric_cols].std().mean() + 1e-10), 2) / 2
            missing_penalty = 1 - (self.df[col].isnull().sum() / len(self.df))
            
            # Correlation with potenti target (highest variance column as proxy)
            if len(self.numeric_cols) > 1:
                target_proxy = self.df[self.numeric_cols].std().idxmax()
                corr_score = abs(self.df[col].corr(self.df[target_proxy])) if col != target_proxy else 0
            else:
                corr_score = 0.5
            
            score = (variance_score * 0.4 + missing_penalty * 0.3 + corr_score * 0.3) * 100
            
            importance.append({
                "feature": col,
                "importance_score": round(score, 1),
                "components": {
                    "variance": round(variance_score * 100, 1),
                    "completeness": round(missing_penalty * 100, 1),
                    "correlation": round(corr_score * 100, 1)
                },
                "interpretation": "high" if score > 70 else "medium" if score > 40 else "low"
            })
        
        return sorted(importance, key=lambda x: x["importance_score"], reverse=True)
    
    def _train_serve_consistency_check(self) -> Dict[str, Any]:
        """Check for potential train-serve inconsistencies."""
        issues = []
        
        # Date columns that might cause issues
        for col in self.datetime_cols:
            issues.append({
                "type": "datetime",
                "column": col,
                "warning": "DateTime columns may cause train-serve skew",
                "recommendation": "Convert to numeric features (year, month, day) or relative values"
            })
        
        # High cardinality categoricals
        for col in self.categorical_cols:
            if self.df[col].nunique() > 100:
                issues.append({
                    "type": "high_cardinality",
                    "column": col,
                    "warning": "New categories in production will fail",
                    "recommendation": "Use handle_unknown='ignore' in encoder"
                })
        
        # Columns with many unique values (potential data entry issues)
        for col in self.categorical_cols:
            if self.df[col].nunique() > len(self.df) * 0.5:
                issues.append({
                    "type": "potential_id",
                    "column": col,
                    "warning": "Looks like an ID column - will not generalize",
                    "recommendation": "Exclude from features"
                })
        
        return {
            "consistent": len(issues) == 0,
            "issues": issues,
            "overall_recommendation": "Address issues before deployment" if issues else "Ready for production"
        }
    
    def _exportable_preprocessing_pipeline(self) -> Dict[str, Any]:
        """Generate sklearn-ready pipeline code."""
        code_parts = []
        
        code_parts.append("from sklearn.pipeline import Pipeline")
        code_parts.append("from sklearn.compose import ColumnTransformer")
        code_parts.append("from sklearn.preprocessing import StandardScaler, OneHotEncoder")
        code_parts.append("from sklearn.impute import SimpleImputer")
        code_parts.append("")
        
        # Numeric pipeline
        code_parts.append("numeric_transformer = Pipeline(steps=[")
        code_parts.append("    ('imputer', SimpleImputer(strategy='median')),")
        code_parts.append("    ('scaler', StandardScaler())")
        code_parts.append("])")
        code_parts.append("")
        
        # Categorical pipeline
        code_parts.append("categorical_transformer = Pipeline(steps=[")
        code_parts.append("    ('imputer', SimpleImputer(strategy='most_frequent')),")
        code_parts.append("    ('encoder', OneHotEncoder(handle_unknown='ignore'))")
        code_parts.append("])")
        code_parts.append("")
        
        # Column transformer
        code_parts.append("preprocessor = ColumnTransformer(")
        code_parts.append("    transformers=[")
        code_parts.append(f"        ('num', numeric_transformer, {self.numeric_cols}),")
        code_parts.append(f"        ('cat', categorical_transformer, {self.categorical_cols})")
        code_parts.append("    ])")
        
        return {
            "code": "\n".join(code_parts),
            "description": "Ready-to-use sklearn preprocessing pipeline",
            "numeric_columns": self.numeric_cols,
            "categorical_columns": self.categorical_cols
        }
    
    def _saved_artifacts_info(self) -> Dict[str, Any]:
        """Information about artifacts to save for deployment."""
        return {
            "required_artifacts": [
                {
                    "name": "preprocessor.pkl",
                    "description": "Fitted preprocessing pipeline",
                    "code": "joblib.dump(preprocessor, 'preprocessor.pkl')"
                },
                {
                    "name": "feature_schema.json",
                    "description": "Expected feature names and types",
                    "content": {
                        "numeric_features": self.numeric_cols,
                        "categorical_features": self.categorical_cols,
                        "expected_columns": list(self.df.columns)
                    }
                },
                {
                    "name": "data_stats.json",
                    "description": "Training data statistics for validation",
                    "content": {
                        "n_samples": len(self.df),
                        "n_features": len(self.df.columns),
                        "numeric_means": self.df[self.numeric_cols].mean().to_dict() if self.numeric_cols else {}
                    }
                }
            ],
            "optional_artifacts": [
                {"name": "label_encoders.pkl", "description": "Fitted label encoders"},
                {"name": "feature_selector.pkl", "description": "Feature selection model"}
            ]
        }
    
    def _reproducibility_lock(self) -> Dict[str, Any]:
        """Generate reproducibility information."""
        import hashlib
        
        # Create data hash
        data_string = self.df.to_string()
        data_hash = hashlib.md5(data_string.encode()).hexdigest()[:12]
        
        return {
            "data_hash": data_hash,
            "random_seed": 42,
            "python_code": """
# Add this at the start of your script
import numpy as np
import random
import os

SEED = 42
np.random.seed(SEED)
random.seed(SEED)
os.environ['PYTHONHASHSEED'] = str(SEED)

# For sklearn
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(X, test_size=0.2, random_state=SEED)
""",
            "data_version": data_hash,
            "n_samples": len(self.df),
            "n_features": len(self.df.columns)
        }
    
    def _risky_features_flag(self) -> List[Dict[str, Any]]:
        """Identify risky/unstable features."""
        risky = []
        
        for col in self.numeric_cols:
            issues = []
            
            # High missing
            missing_pct = self.df[col].isnull().sum() / len(self.df) * 100
            if missing_pct > 20:
                issues.append(f"High missing ({missing_pct:.1f}%)")
            
            # Near-zero variance
            if self.df[col].std() < 0.01:
                issues.append("Near-zero variance")
            
            # Extreme skewness
            skew = self.df[col].skew()
            if abs(skew) > 5:
                issues.append(f"Extreme skewness ({skew:.1f})")
            
            # Many outliers
            Q1, Q3 = self.df[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            outlier_pct = ((self.df[col] < Q1 - 3*IQR) | (self.df[col] > Q3 + 3*IQR)).sum() / len(self.df) * 100
            if outlier_pct > 5:
                issues.append(f"Many extreme outliers ({outlier_pct:.1f}%)")
            
            if issues:
                risky.append({
                    "feature": col,
                    "risk_level": "high" if len(issues) >= 2 else "medium",
                    "issues": issues,
                    "recommendation": "Consider removing or transforming"
                })
        
        return risky
    
    def _feature_interaction_hints(self) -> List[Dict[str, Any]]:
        """Hint at potential feature interactions."""
        interactions = []
        
        if len(self.numeric_cols) >= 2:
            # Find correlated pairs that might benefit from interaction
            corr = self.df[self.numeric_cols].corr()
            
            for i, col1 in enumerate(self.numeric_cols):
                for col2 in self.numeric_cols[i+1:]:
                    corr_val = abs(corr.loc[col1, col2])
                    
                    # Moderate correlation suggests potential interaction
                    if 0.3 < corr_val < 0.7:
                        interactions.append({
                            "features": [col1, col2],
                            "correlation": round(corr_val, 2),
                            "suggested_interaction": f"{col1}_x_{col2}",
                            "code": f"df['{col1}_x_{col2}'] = df['{col1}'] * df['{col2}']",
                            "reason": "Moderate correlation may indicate multiplicative relationship"
                        })
        
        return interactions[:5]  # Limit to top 5
    
    # ==================== ENTERPRISE TIER FEATURES ====================
    
    def _deployment_readiness_score(self) -> Dict[str, Any]:
        """Overall deployment readiness assessment."""
        score = 100
        issues = []
        
        # Check data quality
        missing_pct = (self.df.isnull().sum().sum() / self.df.size) * 100
        if missing_pct > 5:
            score -= 15
            issues.append("High missing values need handling")
        
        # Check for ID columns
        for col in self.df.columns:
            if self.df[col].nunique() == len(self.df):
                score -= 10
                issues.append(f"Potential ID column: {col}")
        
        # Check data types consistency
        for col in self.categorical_cols:
            if self.df[col].nunique() > 100:
                score -= 5
                issues.append(f"High cardinality: {col}")
        
        # Determine status
        if score >= 80:
            status = "ready"
            color = "green"
        elif score >= 60:
            status = "needs_work"
            color = "yellow"
        else:
            status = "not_ready"
            color = "red"
        
        return {
            "score": max(score, 0),
            "status": status,
            "color": color,
            "issues": issues,
            "checklist": {
                "data_quality": missing_pct < 5,
                "no_leakage": len(issues) < 2,
                "consistent_types": True,
                "sufficient_samples": len(self.df) >= 100
            }
        }
    
    def _data_drift_risk(self) -> Dict[str, Any]:
        """Assess data drift risk per feature."""
        risks = []
        
        for col in self.numeric_cols:
            # Features with high variance are more prone to drift
            cv = self.df[col].std() / (abs(self.df[col].mean()) + 1e-10)
            
            risk_level = "high" if cv > 1 else "medium" if cv > 0.5 else "low"
            
            risks.append({
                "feature": col,
                "coefficient_of_variation": round(cv, 2),
                "drift_risk": risk_level,
                "recommendation": "Monitor closely" if risk_level == "high" else "Standard monitoring"
            })
        
        return {
            "overall_risk": "high" if any(r["drift_risk"] == "high" for r in risks) else "medium",
            "features": sorted(risks, key=lambda x: x["coefficient_of_variation"], reverse=True)
        }
    
    def _schema_change_alerts(self) -> Dict[str, Any]:
        """Generate schema for change detection."""
        schema = {
            "columns": list(self.df.columns),
            "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()},
            "nullable": {col: bool(self.df[col].isnull().any()) for col in self.df.columns},
            "unique_counts": {col: int(self.df[col].nunique()) for col in self.df.columns}
        }
        
        return {
            "current_schema": schema,
            "validation_code": """
def validate_schema(new_df, expected_schema):
    errors = []
    for col in expected_schema['columns']:
        if col not in new_df.columns:
            errors.append(f"Missing column: {col}")
    for col in new_df.columns:
        if col not in expected_schema['columns']:
            errors.append(f"Unexpected column: {col}")
    return errors
""",
            "alert_on": ["Missing columns", "Type changes", "New columns"]
        }
    
    def _versioned_pipeline_export(self) -> Dict[str, Any]:
        """Export versioned pipeline information."""
        import hashlib
        from datetime import datetime
        
        version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return {
            "version": version,
            "export_format": "joblib",
            "code": f"""
import joblib
from datetime import datetime

# Save with version
version = "{version}"
artifacts = {{
    'preprocessor': preprocessor,
    'model': model,
    'version': version,
    'created_at': datetime.now().isoformat(),
    'n_features': {len(self.df.columns)},
    'feature_names': {list(self.df.columns)}
}}

joblib.dump(artifacts, f'pipeline_v{{version}}.pkl')
""",
            "metadata": {
                "n_features": len(self.df.columns),
                "feature_names": list(self.df.columns),
                "n_samples_trained": len(self.df)
            }
        }
    
    def _inference_cost_estimation(self) -> Dict[str, Any]:
        """Estimate inference costs."""
        n_features = len(self.df.columns)
        n_numeric = len(self.numeric_cols)
        n_categorical = len(self.categorical_cols)
        
        # Rough complexity estimation
        preprocessing_complexity = n_numeric * 2 + n_categorical * 5
        
        # Estimate one-hot explosion
        onehot_features = sum(self.df[col].nunique() for col in self.categorical_cols)
        
        return {
            "preprocessing_ops_per_sample": preprocessing_complexity,
            "estimated_feature_dimension": n_numeric + onehot_features,
            "memory_per_1000_samples_mb": round((n_numeric + onehot_features) * 1000 * 8 / 1024 / 1024, 2),
            "recommendations": {
                "batch_size": 1000 if preprocessing_complexity > 100 else 5000,
                "caching": preprocessing_complexity > 50,
                "async_processing": n_categorical > 10
            }
        }


def analyze_with_intelligence(df: pd.DataFrame, tier: str = "free") -> Dict[str, Any]:
    """
    Main entry point for intelligence analysis.
    
    Args:
        df: Pandas DataFrame to analyze
        tier: User tier (free, starter, pro, enterprise)
    
    Returns:
        Dictionary with all applicable intelligence features
    """
    intelligence = DataIntelligence(df, tier)
    return intelligence.analyze()
