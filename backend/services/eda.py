"""
KuyaEDA - Advanced Exploratory Data Analysis Service
Full implementation with ALL PRO features
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from scipy import stats


class EDAGenerator:
    """
    Comprehensive EDA service with PRO features:
    - Summary statistics with skewness/kurtosis
    - Missing value heatmap data
    - Correlation analysis
    - Feature importance (variance-based)
    - Data quality scoring
    - Target analysis
    - AI-like insights
    - Dataset health score
    """

    def generate_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive summary statistics."""
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()
        
        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "numericColumns": numeric_cols,
            "categoricalColumns": categorical_cols,
            "datetimeColumns": datetime_cols,
            "memoryUsage": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        }
        
        # Missing values analysis
        missing = df.isnull().sum()
        summary["missingValues"] = {col: int(missing[col]) for col in df.columns if missing[col] > 0}
        summary["totalMissing"] = int(missing.sum())
        summary["missingPercentage"] = round(missing.sum() / (len(df) * len(df.columns)) * 100, 2) if len(df) > 0 else 0
        
        # Missing by column percentage
        summary["missingByColumn"] = {
            col: round(missing[col] / len(df) * 100, 2) 
            for col in df.columns if missing[col] > 0
        }
        
        # Detailed statistics for numeric columns
        if numeric_cols:
            stats_dict = {}
            for col in numeric_cols:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    stats_dict[col] = {
                        "count": int(len(col_data)),
                        "mean": round(float(col_data.mean()), 4),
                        "std": round(float(col_data.std()), 4),
                        "min": round(float(col_data.min()), 4),
                        "max": round(float(col_data.max()), 4),
                        "median": round(float(col_data.median()), 4),
                        "q25": round(float(col_data.quantile(0.25)), 4),
                        "q75": round(float(col_data.quantile(0.75)), 4),
                        "skewness": round(float(col_data.skew()), 4),
                        "kurtosis": round(float(col_data.kurtosis()), 4),
                        "variance": round(float(col_data.var()), 4),
                        "cv": round(float(col_data.std() / col_data.mean()), 4) if col_data.mean() != 0 else 0,
                        "iqr": round(float(col_data.quantile(0.75) - col_data.quantile(0.25)), 4),
                        "range": round(float(col_data.max() - col_data.min()), 4),
                    }
            summary["statistics"] = stats_dict
        
        # Categorical stats
        if categorical_cols:
            unique_dict = {}
            for col in categorical_cols:
                vc = df[col].value_counts()
                unique_dict[col] = {
                    "count": int(df[col].nunique()),
                    "top": str(vc.index[0]) if len(vc) > 0 else None,
                    "topFreq": int(vc.iloc[0]) if len(vc) > 0 else 0,
                    "topPercent": round(vc.iloc[0] / len(df) * 100, 2) if len(vc) > 0 and len(df) > 0 else 0,
                }
            summary["categoricalStats"] = unique_dict
        
        return summary

    def generate_missing_heatmap_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate data for missing values heatmap visualization."""
        # Create binary matrix (1 = missing, 0 = present)
        missing_matrix = df.isnull().astype(int)
        
        # Calculate co-occurrence of missing values
        if missing_matrix.sum().sum() > 0:
            # Get columns with missing values
            cols_with_missing = missing_matrix.columns[missing_matrix.sum() > 0].tolist()
            
            if len(cols_with_missing) > 1:
                # Calculate co-occurrence matrix
                co_occurrence = {}
                for col1 in cols_with_missing:
                    co_occurrence[col1] = {}
                    for col2 in cols_with_missing:
                        both_missing = ((missing_matrix[col1] == 1) & (missing_matrix[col2] == 1)).sum()
                        co_occurrence[col1][col2] = int(both_missing)
                
                return {
                    "columns": cols_with_missing,
                    "coOccurrence": co_occurrence,
                    "missingCounts": {col: int(missing_matrix[col].sum()) for col in cols_with_missing},
                }
        
        return {"columns": [], "coOccurrence": {}, "missingCounts": {}}

    def generate_correlation(
        self, 
        df: pd.DataFrame,
        method: str = "pearson"
    ) -> Dict[str, Dict[str, float]]:
        """Generate correlation matrix for numeric columns."""
        numeric_df = df.select_dtypes(include=["number"])
        
        if numeric_df.empty or len(numeric_df.columns) < 2:
            return {}
        
        try:
            corr_matrix = numeric_df.corr(method=method)
            return {
                col: {
                    other_col: round(float(corr_matrix.loc[col, other_col]), 4)
                    for other_col in corr_matrix.columns
                }
                for col in corr_matrix.index
            }
        except Exception as e:
            print(f"Correlation error: {e}")
            return {}

    def calculate_feature_importance(self, df: pd.DataFrame, target_col: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate feature importance based on variance and correlation with target.
        """
        numeric_df = df.select_dtypes(include=["number"])
        
        if numeric_df.empty:
            return {}
        
        importance = {}
        
        # Variance-based importance (normalized)
        variances = numeric_df.var()
        max_var = variances.max() if variances.max() > 0 else 1
        
        for col in numeric_df.columns:
            # Normalize variance to 0-1
            var_score = variances[col] / max_var if max_var > 0 else 0
            
            # If target specified, also use correlation
            if target_col and target_col in numeric_df.columns and col != target_col:
                try:
                    corr = abs(numeric_df[col].corr(numeric_df[target_col]))
                    importance[col] = round((var_score * 0.3 + corr * 0.7), 4)
                except:
                    importance[col] = round(var_score, 4)
            else:
                importance[col] = round(var_score, 4)
        
        # Sort by importance
        importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
        
        return importance

    def analyze_target(self, df: pd.DataFrame, target_col: str) -> Dict[str, Any]:
        """
        Analyze target column for classification/regression insights.
        """
        if target_col not in df.columns:
            return {}
        
        target = df[target_col]
        
        result = {
            "column": target_col,
            "dtype": str(target.dtype),
            "unique_values": int(target.nunique()),
            "missing": int(target.isnull().sum()),
        }
        
        # Check if binary/multiclass classification or regression
        if target.dtype in ['int64', 'float64']:
            unique = target.nunique()
            if unique <= 10:
                # Classification
                result["task_type"] = "classification"
                result["class_distribution"] = target.value_counts().to_dict()
                
                # Check imbalance
                vc = target.value_counts()
                if len(vc) >= 2:
                    imbalance_ratio = vc.iloc[0] / vc.iloc[-1]
                    result["imbalance_ratio"] = round(imbalance_ratio, 2)
                    result["is_imbalanced"] = imbalance_ratio > 3
            else:
                # Regression
                result["task_type"] = "regression"
                result["mean"] = round(float(target.mean()), 4)
                result["std"] = round(float(target.std()), 4)
                result["skewness"] = round(float(target.skew()), 4)
        else:
            # Categorical target
            result["task_type"] = "classification"
            result["class_distribution"] = target.value_counts().head(10).to_dict()
        
        return result

    def calculate_data_quality_score(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate overall data quality score (0-100)."""
        scores = []
        details = {}
        
        # Completeness
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isnull().sum().sum()
        completeness = (1 - missing_cells / total_cells) * 100 if total_cells > 0 else 0
        scores.append(completeness)
        details["completeness"] = round(completeness, 2)
        
        # Uniqueness (duplicate check)
        duplicates = df.duplicated().sum()
        uniqueness = (1 - duplicates / len(df)) * 100 if len(df) > 0 else 0
        scores.append(uniqueness)
        details["uniqueness"] = round(uniqueness, 2)
        
        # Consistency
        consistency_scores = []
        for col in df.columns:
            if df[col].dtype == "object":
                try:
                    pd.to_numeric(df[col], errors="raise")
                    consistency_scores.append(50)
                except:
                    consistency_scores.append(100)
            else:
                consistency_scores.append(100)
        consistency = np.mean(consistency_scores) if consistency_scores else 100
        scores.append(consistency)
        details["consistency"] = round(consistency, 2)
        
        # Validity (outlier check)
        numeric_cols = df.select_dtypes(include=["number"]).columns
        outlier_percentages = []
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
            outlier_pct = outliers / len(df) * 100 if len(df) > 0 else 0
            outlier_percentages.append(100 - outlier_pct)
        validity = np.mean(outlier_percentages) if outlier_percentages else 100
        scores.append(validity)
        details["validity"] = round(validity, 2)
        
        # Overall score
        overall = np.mean(scores)
        
        # Grade
        if overall >= 90:
            grade, status = "A", "Excellent"
        elif overall >= 80:
            grade, status = "B", "Good"
        elif overall >= 70:
            grade, status = "C", "Fair"
        elif overall >= 60:
            grade, status = "D", "Poor"
        else:
            grade, status = "F", "Critical"
        
        return {
            "overall_score": round(overall, 2),
            "grade": grade,
            "status": status,
            "details": details,
        }

    def calculate_dataset_health(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive dataset health metrics."""
        health = {
            "size": {
                "rows": len(df),
                "columns": len(df.columns),
                "total_cells": len(df) * len(df.columns),
                "memory_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
            },
            "completeness": {
                "total_missing": int(df.isnull().sum().sum()),
                "missing_percentage": round(df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100, 2) if len(df) > 0 else 0,
                "complete_rows": int((~df.isnull().any(axis=1)).sum()),
                "complete_columns": int((~df.isnull().any()).sum()),
            },
            "diversity": {
                "numeric_columns": len(df.select_dtypes(include=["number"]).columns),
                "categorical_columns": len(df.select_dtypes(include=["object", "category"]).columns),
                "datetime_columns": len(df.select_dtypes(include=["datetime64"]).columns),
                "high_cardinality_cols": len([c for c in df.columns if df[c].nunique() > 100]),
            },
            "duplicates": {
                "count": int(df.duplicated().sum()),
                "percentage": round(df.duplicated().sum() / len(df) * 100, 2) if len(df) > 0 else 0,
            },
        }
        
        # Health score (0-100)
        scores = [
            100 - health["completeness"]["missing_percentage"],
            100 - health["duplicates"]["percentage"],
            min(100, health["diversity"]["numeric_columns"] * 10),  # Reward diversity
        ]
        health["overall_health"] = round(np.mean(scores), 2)
        
        return health

    def generate_insights(
        self, 
        original_df: pd.DataFrame, 
        cleaned_df: pd.DataFrame,
        summary: Dict[str, Any],
        correlation: Dict[str, Dict[str, float]]
    ) -> List[str]:
        """Generate AI-like insights from the data analysis."""
        insights = []
        
        rows, cols = cleaned_df.shape
        insights.append(f"📊 Your dataset contains **{rows:,} rows** and **{cols} columns** ready for analysis.")
        
        # Missing values insights
        total_missing = summary.get("totalMissing", 0)
        if total_missing > 0:
            missing_pct = summary.get("missingPercentage", 0)
            if missing_pct < 5:
                insights.append(f"✅ **Good:** Data cleaned with only {missing_pct:.1f}% missing values filled.")
            elif missing_pct < 20:
                insights.append(f"⚠️ **Warning:** {missing_pct:.1f}% of data was missing and has been handled.")
            else:
                insights.append(f"🚨 **Alert:** High missing rate ({missing_pct:.1f}%). Consider data collection improvements.")
            
            # Column-specific
            missing_by_col = summary.get("missingByColumn", {})
            for col, pct in sorted(missing_by_col.items(), key=lambda x: x[1], reverse=True)[:3]:
                if pct > 10:
                    insights.append(f"⚠️ Column **'{col}'** has {pct:.1f}% missing values.")
        else:
            insights.append("✅ **Excellent:** Your dataset has no missing values!")
        
        # Correlation insights
        if correlation:
            strong_corrs = []
            for col1, correlations in correlation.items():
                for col2, corr_val in correlations.items():
                    if col1 < col2 and abs(corr_val) > 0.7:
                        direction = "positive" if corr_val > 0 else "negative"
                        strong_corrs.append((col1, col2, corr_val, direction))
            
            if strong_corrs:
                insights.append(f"🔗 Found **{len(strong_corrs)} strong correlations** between columns:")
                for col1, col2, corr_val, direction in strong_corrs[:3]:
                    insights.append(f"   • '{col1}' ↔ '{col2}': {direction} correlation ({corr_val:.2f})")
        
        # Skewness insights
        stats = summary.get("statistics", {})
        skewed_cols = []
        for col, col_stats in stats.items():
            skewness = col_stats.get("skewness", 0)
            if abs(skewness) > 2:
                direction = "right" if skewness > 0 else "left"
                skewed_cols.append((col, skewness, direction))
        
        if skewed_cols:
            insights.append(f"📈 **{len(skewed_cols)} columns have skewed distributions:**")
            for col, skew, direction in skewed_cols[:3]:
                insights.append(f"   • '{col}' is {direction}-skewed (skewness: {skew:.2f})")
        
        # High variability columns
        high_cv_cols = []
        for col, col_stats in stats.items():
            cv = col_stats.get("cv", 0)
            if cv > 1:
                high_cv_cols.append((col, cv))
        
        if high_cv_cols:
            insights.append(f"📉 **{len(high_cv_cols)} columns have high variability:**")
            for col, cv in sorted(high_cv_cols, key=lambda x: x[1], reverse=True)[:3]:
                insights.append(f"   • '{col}' (CV: {cv:.2f})")
        
        # Categorical insights
        cat_stats = summary.get("categoricalStats", {})
        for col, col_stats in cat_stats.items():
            unique_count = col_stats.get("count", 0)
            if unique_count > 100:
                insights.append(f"📝 Column **'{col}'** has high cardinality ({unique_count:,} unique values).")
            elif unique_count == 2:
                insights.append(f"🔘 Column **'{col}'** is binary ({unique_count} unique values).")
        
        # Quality score
        quality = self.calculate_data_quality_score(cleaned_df)
        insights.append(f"🏆 **Data Quality Score: {quality['overall_score']:.0f}/100** ({quality['status']})")
        
        return insights

    def magic_analyze(self, df: pd.DataFrame, target_col: Optional[str] = None) -> Dict[str, Any]:
        """AI-powered comprehensive analysis with recommendations."""
        results = {
            "summary": self.generate_summary(df),
            "correlation": self.generate_correlation(df),
            "missing_heatmap": self.generate_missing_heatmap_data(df),
            "quality_score": self.calculate_data_quality_score(df),
            "health": self.calculate_dataset_health(df),
            "feature_importance": self.calculate_feature_importance(df, target_col),
            "recommendations": [],
        }
        
        if target_col:
            results["target_analysis"] = self.analyze_target(df, target_col)
        
        recommendations = []
        
        # Missing data recommendations
        if results["summary"]["totalMissing"] > 0:
            missing_pct = results["summary"]["missingPercentage"]
            if missing_pct > 20:
                recommendations.append({
                    "type": "warning",
                    "title": "High Missing Data",
                    "description": f"{missing_pct:.1f}% of data is missing. Consider imputation or removing columns with >50% missing.",
                    "action": "df.clean_missing(strategy='auto')",
                })
        
        # Multicollinearity
        high_corr_pairs = []
        for col1, correlations in results["correlation"].items():
            for col2, corr_val in correlations.items():
                if col1 < col2 and abs(corr_val) > 0.9:
                    high_corr_pairs.append((col1, col2, corr_val))
        
        if high_corr_pairs:
            recommendations.append({
                "type": "info",
                "title": "Multicollinearity Detected",
                "description": f"Found {len(high_corr_pairs)} highly correlated pairs. Remove redundant features for ML models.",
                "action": "Consider removing one of each correlated pair",
            })
        
        # Quality recommendations
        quality = results["quality_score"]
        if quality["details"]["completeness"] < 80:
            recommendations.append({
                "type": "warning",
                "title": "Low Data Completeness",
                "description": "Data completeness is below 80%. Improve data collection or use imputation.",
                "action": "df.clean_missing(strategy='auto')",
            })
        
        if quality["details"]["uniqueness"] < 95:
            dup_count = results["health"]["duplicates"]["count"]
            recommendations.append({
                "type": "info",
                "title": f"{dup_count} Duplicate Rows Found",
                "description": "Remove duplicates for cleaner analysis.",
                "action": "df.remove_duplicates()",
            })
        
        if quality["details"]["validity"] < 90:
            recommendations.append({
                "type": "info",
                "title": "Outliers Detected",
                "description": "Some columns contain outliers that may affect analysis.",
                "action": "df.remove_outliers() or investigate further",
            })
        
        # Target imbalance
        if target_col and "target_analysis" in results:
            target_info = results["target_analysis"]
            if target_info.get("is_imbalanced"):
                recommendations.append({
                    "type": "warning",
                    "title": "Imbalanced Target Variable",
                    "description": f"Imbalance ratio: {target_info.get('imbalance_ratio', 0):.1f}x. Use SMOTE or class weights.",
                    "action": "Use class_weight='balanced' or SMOTE",
                })
        
        results["recommendations"] = recommendations
        return results
