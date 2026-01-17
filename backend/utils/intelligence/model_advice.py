"""
Model Advice Module - STARTER + PRO tier features
Handles model recommendations, preprocessing advice, and confidence scores
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


class ModelAdvisor:
    """Model recommendations and preprocessing advice."""
    
    def __init__(self, df: pd.DataFrame, has_significant_outliers_fn):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self._has_significant_outliers = has_significant_outliers_fn
    
    # ==================== STARTER TIER ====================
    
    def confidence_scores(self) -> Dict[str, Any]:
        """Confidence score for data reliability (Starter tier)."""
        scores = {}
        
        completeness = (1 - self.df.isnull().sum().sum() / self.df.size) * 100
        consistency = 100 - (self.df.duplicated().sum() / len(self.df) * 100)
        scores["data_reliability"] = {
            "score": round((completeness + consistency) / 2, 1),
            "explanation": "How reliable is this dataset? Based on completeness and consistency.",
            "label": "Data Reliability"
        }
        
        readiness_score = 70
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
    
    def model_impact_confidence(self) -> Dict[str, Any]:
        """Model impact confidence (Pro tier only)."""
        scores = {}
        
        feature_score = 60
        if len(self.numeric_cols) >= 5:
            feature_score += 15
        if not self._has_significant_outliers():
            feature_score += 10
        if len(self.categorical_cols) <= 5:
            feature_score += 10
        scores["feature_quality_impact"] = {
            "score": min(feature_score, 100),
            "explanation": "How likely are these features to improve model performance?",
            "label": "Feature Quality Impact"
        }
        
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
    
    def tradeoff_analysis_light(self) -> List[Dict[str, Any]]:
        """Light trade-off analysis between options."""
        tradeoffs = []
        
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
    
    def suggest_baseline_model(self) -> Dict[str, Any]:
        """Suggest best starting model for this data."""
        suggestions = []
        
        n_samples = len(self.df)
        n_features = len(self.df.columns)
        has_categorical = len(self.categorical_cols) > 0
        has_missing = self.df.isnull().sum().sum() > 0
        
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
    
    def metric_sensitivity_basic(self) -> Dict[str, Any]:
        """Basic metric sensitivity analysis."""
        sensitivity = {}
        
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
    
    def assumption_checker_basic(self) -> Dict[str, Any]:
        """Basic assumption checking for models."""
        checks = {}
        
        n = len(self.df)
        p = len(self.df.columns)
        checks["sample_size"] = {
            "status": "pass" if n >= 10 * p else "warning",
            "message": f"Rule of thumb: need 10x features ({10*p}) samples. You have {n}.",
            "recommendation": "Collect more data" if n < 10 * p else "Sample size adequate"
        }
        
        if len(self.numeric_cols) >= 2:
            correlations = self.df[self.numeric_cols].corr().abs()
            avg_corr = correlations.values[np.triu_indices_from(correlations.values, 1)].mean()
            checks["linearity"] = {
                "status": "pass" if avg_corr > 0.3 else "warning",
                "message": f"Average feature correlation: {avg_corr:.2f}",
                "recommendation": "Linear models may work" if avg_corr > 0.3 else "Consider non-linear models"
            }
        
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
    
    def outlier_strategy_suggestion(self) -> Dict[str, Any]:
        """Suggest outlier handling strategy."""
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
        
        if not outlier_cols:
            return {
                "strategy": "none",
                "message": "No significant outliers detected",
                "confidence": 90
            }
        
        total_outlier_pct = sum(d["percentage"] for d in outlier_cols) / len(outlier_cols)
        
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
    
    def high_impact_features(self) -> List[Dict[str, Any]]:
        """Identify top 3 high-impact features."""
        impact_scores = {}
        
        for col in self.numeric_cols:
            variance_score = min(self.df[col].std() / (self.df[col].mean() + 1e-10), 2) * 30
            missing_penalty = (1 - self.df[col].isnull().sum() / len(self.df)) * 30
            unique_score = min(self.df[col].nunique() / len(self.df) * 100, 40)
            
            impact_scores[col] = variance_score + missing_penalty + unique_score
        
        sorted_features = sorted(impact_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return [
            {
                "feature": feat,
                "impact_score": round(score, 1),
                "reason": "High variance and information content"
            }
            for feat, score in sorted_features
        ]
    
    # ==================== PRO TIER ====================
    
    def model_specific_preprocessing(self) -> Dict[str, Any]:
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
    
    def scaling_impact_per_model(self) -> Dict[str, Any]:
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
    
    def encoding_choice_recommendation(self) -> Dict[str, Any]:
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
    
    def feature_importance_heuristic(self) -> List[Dict[str, Any]]:
        """Heuristic feature importance without training."""
        importance = []
        
        for col in self.numeric_cols:
            variance_score = min(self.df[col].std() / (self.df[self.numeric_cols].std().mean() + 1e-10), 2) / 2
            missing_penalty = 1 - (self.df[col].isnull().sum() / len(self.df))
            
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
    
    def feature_interaction_hints(self) -> List[Dict[str, Any]]:
        """Hint at potential feature interactions."""
        interactions = []
        
        if len(self.numeric_cols) >= 2:
            corr = self.df[self.numeric_cols].corr()
            
            for i, col1 in enumerate(self.numeric_cols):
                for col2 in self.numeric_cols[i+1:]:
                    corr_val = abs(corr.loc[col1, col2])
                    
                    if 0.3 < corr_val < 0.7:
                        interactions.append({
                            "features": [col1, col2],
                            "correlation": round(corr_val, 2),
                            "suggested_interaction": f"{col1}_x_{col2}",
                            "code": f"df['{col1}_x_{col2}'] = df['{col1}'] * df['{col2}']",
                            "reason": "Moderate correlation may indicate multiplicative relationship"
                        })
        
        return interactions[:5]
