"""
Kuya Data Service - Using the actual kuya-data library
https://pypi.org/project/kuya-data/
"""

import kuya as ky
from kuya.core import KuyaDataFrame
import pandas as pd
import io
import base64
from typing import Dict, Any, List, Optional
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class KuyaDataService:
    """
    Service wrapper for kuya-data library.
    Uses the official kuya-data package for:
    - Data cleaning
    - EDA & insights
    - Visualization
    - Quality reports
    """

    def __init__(self, df: pd.DataFrame):
        """Initialize with a pandas DataFrame."""
        self.kdf = KuyaDataFrame(df)
        self.original_df = df.copy()

    def quick_clean(self) -> pd.DataFrame:
        """
        One-command cleaning using kuya's quick_clean.
        ✅ Standardizes columns
        ✅ Fixes data types
        ✅ Handles missing values
        ✅ Removes outliers
        """
        cleaned = ky.quick_clean(self.kdf)
        self.kdf = KuyaDataFrame(cleaned)
        return cleaned

    def clean_missing(self, method: str = "fill", value: Any = None) -> pd.DataFrame:
        """Clean missing values."""
        self.kdf = self.kdf.clean_missing(method=method, value=value)
        return self.kdf

    def fix_dtypes(self) -> pd.DataFrame:
        """Auto-convert columns to proper types."""
        self.kdf = self.kdf.fix_dtypes()
        return self.kdf

    def standardize_columns(self) -> pd.DataFrame:
        """Make column names lowercase with underscores."""
        self.kdf = self.kdf.standardize_columns()
        return self.kdf

    def handle_outliers(self, method: str = "iqr") -> pd.DataFrame:
        """Remove outliers using IQR or Z-score method."""
        self.kdf = self.kdf.handle_outliers(method=method)
        return self.kdf

    def get_summary(self) -> Dict[str, Any]:
        """Get full descriptive summary."""
        summary_df = self.kdf.summary()
        
        # Build summary dict
        summary = {
            "rows": len(self.kdf),
            "columns": len(self.kdf.columns),
            "numericColumns": self.kdf.select_dtypes(include=["number"]).columns.tolist(),
            "categoricalColumns": self.kdf.select_dtypes(include=["object", "category"]).columns.tolist(),
            "missingValues": self.kdf.isnull().sum().to_dict(),
            "totalMissing": int(self.kdf.isnull().sum().sum()),
            "missingPercentage": round(self.kdf.isnull().sum().sum() / (len(self.kdf) * len(self.kdf.columns)) * 100, 2) if len(self.kdf) > 0 else 0,
        }
        
        # Add statistics for numeric columns
        numeric_df = self.kdf.select_dtypes(include=["number"])
        if len(numeric_df.columns) > 0:
            stats = {}
            for col in numeric_df.columns:
                col_data = numeric_df[col].dropna()
                if len(col_data) > 0:
                    stats[col] = {
                        "mean": round(float(col_data.mean()), 4),
                        "std": round(float(col_data.std()), 4),
                        "min": round(float(col_data.min()), 4),
                        "max": round(float(col_data.max()), 4),
                        "median": round(float(col_data.median()), 4),
                        "q25": round(float(col_data.quantile(0.25)), 4),
                        "q75": round(float(col_data.quantile(0.75)), 4),
                        "skewness": round(float(col_data.skew()), 4),
                        "kurtosis": round(float(col_data.kurtosis()), 4),
                    }
            summary["statistics"] = stats
        
        return summary

    def check_missing(self) -> Dict[str, Any]:
        """Get missing value analysis."""
        missing_info = self.kdf.check_missing()
        return {
            "columns": self.kdf.isnull().sum().to_dict(),
            "percentages": (self.kdf.isnull().sum() / len(self.kdf) * 100).round(2).to_dict(),
            "total": int(self.kdf.isnull().sum().sum()),
        }

    def unique_summary(self) -> Dict[str, int]:
        """Get unique value counts per column."""
        return self.kdf.nunique().to_dict()

    def correlation_report(self) -> Dict[str, Dict[str, float]]:
        """Get correlation matrix."""
        numeric_df = self.kdf.select_dtypes(include=["number"])
        if len(numeric_df.columns) < 2:
            return {}
        
        corr = numeric_df.corr()
        return {
            col: {other: round(float(corr.loc[col, other]), 4) for other in corr.columns}
            for col in corr.index
        }

    def quality_report(self) -> Dict[str, Any]:
        """Get comprehensive data quality report with scoring."""
        try:
            quality = self.kdf.quality_report()
            return quality
        except:
            # Fallback if method not available
            total_cells = len(self.kdf) * len(self.kdf.columns)
            missing = self.kdf.isnull().sum().sum()
            duplicates = self.kdf.duplicated().sum()
            
            completeness = (1 - missing / total_cells) * 100 if total_cells > 0 else 0
            uniqueness = (1 - duplicates / len(self.kdf)) * 100 if len(self.kdf) > 0 else 0
            
            score = (completeness + uniqueness) / 2
            
            if score >= 90: grade, status = "A", "Excellent"
            elif score >= 80: grade, status = "B", "Good"
            elif score >= 70: grade, status = "C", "Fair"
            elif score >= 60: grade, status = "D", "Poor"
            else: grade, status = "F", "Critical"
            
            return {
                "overall_score": round(score, 2),
                "grade": grade,
                "status": status,
                "details": {
                    "completeness": round(completeness, 2),
                    "uniqueness": round(uniqueness, 2),
                },
            }

    def smart_analysis(self) -> Dict[str, Any]:
        """Get AI-powered smart analysis with insights."""
        try:
            insights = self.kdf.smart_analysis()
            return insights
        except:
            # Generate insights manually
            return self._generate_insights()

    def auto_insights(self) -> List[str]:
        """Generate automated insights from data."""
        try:
            insights = self.kdf.auto_insights()
            if isinstance(insights, list) and len(insights) > 0:
                return insights
            # Fallback if empty list returned
            print("⚠️ Library auto_insights returned empty, using manual fallback.")
            return self._generate_insights_list()
        except Exception as e:
            print(f"⚠️ auto_insights failed: {e}, using manual fallback.")
            return self._generate_insights_list()

    def _generate_insights_list(self) -> List[str]:
        """Generate manual insights with advanced heuristics."""
        insights = []
        
        # 1. Dataset Shape & Overview
        insights.append(f"📊 Dataset contains {len(self.kdf):,} rows and {len(self.kdf.columns)} columns.")
        
        # 2. Missing Data Analysis
        missing_total = self.kdf.isnull().sum().sum()
        if missing_total == 0:
            insights.append("✅ Data Quality is excellent! No missing values detected.")
        else:
            missing_pct = missing_total / (len(self.kdf) * len(self.kdf.columns)) * 100
            if missing_pct < 1:
                insights.append(f"ℹ️ Slight data gaps detected ({missing_pct:.2f}% missing). Handling strategies applied.")
            elif missing_pct < 20:
                insights.append(f"⚠️ Moderate missing data ({missing_pct:.1f}%). Imputation recommended.")
            else:
                insights.append(f"🚨 Significant data missing ({missing_pct:.1f}%). Data collection review advised.")

        # 3. Column Analysis
        numeric_cols = self.kdf.select_dtypes(include=["number"]).columns
        categorical_cols = self.kdf.select_dtypes(include=["object", "category"]).columns
        
        insights.append(f"📝 Found {len(numeric_cols)} numeric and {len(categorical_cols)} categorical variables.")

        # 4. Constant & ID Columns (New Logic)
        for col in self.kdf.columns:
            try:
                unique_count = self.kdf[col].nunique()
                if unique_count == 1:
                    insights.append(f"⚪ Column '{col}' is constant (only 1 unique value). It provides no predictive power.")
                elif unique_count == len(self.kdf) and len(self.kdf) > 1:
                    insights.append(f"🔑 Column '{col}' appears to be a unique identifier (ID).")
                elif col in numeric_cols and unique_count < 10 and unique_count > 1:
                     insights.append(f"🏷️ Numeric column '{col}' has only {unique_count} unique values. It might be categorical.")
            except:
                continue

        # 5. Distribution & Skewness
        for col in numeric_cols[:5]: # Check first few
            try:
                skew = self.kdf[col].skew()
                if abs(skew) > 1.5:
                    direction = "right-skewed" if skew > 0 else "left-skewed"
                    insights.append(f"📉 Distribution of '{col}' is highly {direction} (skew: {skew:.2f}).")
            except:
                pass

        # 6. Correlation Checks
        if len(numeric_cols) >= 2:
            try:
                corr_mat = self.kdf[numeric_cols].corr()
                # Find strongest correlations
                pairs = []
                for i in range(len(numeric_cols)):
                    for j in range(i+1, len(numeric_cols)):
                        val = corr_mat.iloc[i, j]
                        if abs(val) > 0.8:
                            pairs.append((numeric_cols[i], numeric_cols[j], val))
                
                # Sort by strength and take top 3
                pairs.sort(key=lambda x: abs(x[2]), reverse=True)
                for c1, c2, val in pairs[:3]:
                    insights.append(f"🔗 Strong correlation found between '{c1}' and '{c2}' ({val:.2f}).")
            except:
                pass
        
        return insights

    def _generate_insights(self) -> Dict[str, Any]:
        """Generate manual insights dictionary."""
        return {
            "insights": self._generate_insights_list(),
            "summary": self.get_summary(),
            "quality": self.quality_report(),
        }

    def smart_encode(self, method: str = "auto") -> pd.DataFrame:
        """Intelligently encode categorical variables."""
        try:
            self.kdf = self.kdf.smart_encode(method=method)
        except:
            pass
        return self.kdf

    def normalize(self, method: str = "minmax") -> pd.DataFrame:
        """Normalize numeric columns."""
        try:
            self.kdf = self.kdf.normalize(method=method)
        except:
            pass
        return self.kdf

    def detect_duplicates(self) -> Dict[str, Any]:
        """Find duplicate rows."""
        duplicates = self.kdf.duplicated()
        return {
            "count": int(duplicates.sum()),
            "percentage": round(duplicates.sum() / len(self.kdf) * 100, 2) if len(self.kdf) > 0 else 0,
            "indices": self.kdf[duplicates].index.tolist()[:50],
        }

    def magic_analyze(self, target_col: Optional[str] = None) -> Dict[str, Any]:
        """
        Magic Analyze - Complete analysis with ONE command!
        ✅ Data quality assessment
        ✅ Statistical analysis
        ✅ Automated insights
        ✅ Correlation analysis
        ✅ All in one go!
        """
        try:
            if target_col:
                result = self.kdf.magic_analyze(target_col=target_col)
            else:
                result = self.kdf.magic_analyze()
            return result if isinstance(result, dict) else {}
        except:
            # Fallback
            return {
                "summary": self.get_summary(),
                "correlation": self.correlation_report(),
                "quality": self.quality_report(),
                "insights": self._generate_insights_list(),
                "recommendations": self._generate_recommendations(),
            }

    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate recommendations based on data analysis."""
        recs = []
        
        # Missing data
        missing_pct = self.kdf.isnull().sum().sum() / (len(self.kdf) * len(self.kdf.columns)) * 100
        if missing_pct > 20:
            recs.append({
                "type": "warning",
                "title": "High Missing Data",
                "description": f"{missing_pct:.1f}% missing. Use df.clean_missing() or collect more data.",
            })
        
        # Duplicates
        dup_pct = self.kdf.duplicated().sum() / len(self.kdf) * 100
        if dup_pct > 5:
            recs.append({
                "type": "info",
                "title": "Duplicate Rows Found",
                "description": f"{dup_pct:.1f}% duplicates. Consider using df.drop_duplicates().",
            })
        
        # High correlations
        numeric_df = self.kdf.select_dtypes(include=["number"])
        if len(numeric_df.columns) >= 2:
            corr = numeric_df.corr()
            high_corr = []
            for i, col1 in enumerate(corr.columns):
                for col2 in corr.columns[i+1:]:
                    if abs(corr.loc[col1, col2]) > 0.9:
                        high_corr.append((col1, col2))
            if high_corr:
                recs.append({
                    "type": "info",
                    "title": "Multicollinearity Detected",
                    "description": f"Found {len(high_corr)} highly correlated pairs. Consider removing redundant features.",
                })
        
        return recs

    # =========================================================================
    # 🔥 THE 5 UNIQUE PILLARS - GAME CHANGERS
    # =========================================================================

    def smart_column_analysis(self) -> Dict[str, Dict[str, Any]]:
        """
        🧠 SMART COLUMN ANALYSIS ENGINE
        Per-column intelligent analysis with:
        - Type detection (ID, datetime, categorical, numeric, text)
        - Quality assessment
        - Transformation recommendations
        - Importance indicators
        """
        analysis = {}
        
        for col in self.kdf.columns:
            try:
                col_data = self.kdf[col]
                unique_count = col_data.nunique()
                missing_count = col_data.isnull().sum()
                missing_pct = (missing_count / len(self.kdf)) * 100 if len(self.kdf) > 0 else 0
                
                # Detect column type
                if unique_count == len(self.kdf) and len(self.kdf) > 10:
                    col_type = "identifier"
                    importance = "low"
                    action = "drop"
                    reason = "Unique per row - likely an ID column"
                elif unique_count == 1:
                    col_type = "constant"
                    importance = "none"
                    action = "drop"
                    reason = "Single value - provides no information"
                elif col_data.dtype in ['datetime64[ns]', 'datetime64']:
                    col_type = "datetime"
                    importance = "medium"
                    action = "extract_features"
                    reason = "Extract year, month, day, weekday features"
                elif col_data.dtype == 'object':
                    if unique_count <= 20:
                        col_type = "categorical"
                        importance = "high"
                        action = "encode"
                        reason = f"Encode using OneHot or Label encoding ({unique_count} categories)"
                    else:
                        col_type = "text"
                        importance = "medium"
                        action = "vectorize_or_drop"
                        reason = f"High cardinality ({unique_count}). Consider TF-IDF or dropping"
                elif col_data.dtype in ['int64', 'float64', 'int32', 'float32']:
                    col_type = "numeric"
                    importance = "high"
                    action = "keep"
                    reason = "Numeric feature - ready for modeling"
                    
                    # Check for transformations
                    try:
                        skew = col_data.skew()
                        if abs(skew) > 2:
                            action = "log_transform"
                            reason = f"Highly skewed ({skew:.2f}). Apply log transform"
                        elif abs(skew) > 1:
                            action = "normalize"
                            reason = f"Moderately skewed ({skew:.2f}). Consider normalization"
                    except:
                        pass
                else:
                    col_type = "unknown"
                    importance = "low"
                    action = "review"
                    reason = "Unknown type - manual review needed"
                
                # Quality score for column
                quality_score = 100
                quality_issues = []
                
                if missing_pct > 0:
                    quality_score -= min(50, missing_pct)
                    quality_issues.append(f"{missing_pct:.1f}% missing")
                
                if col_type == "constant":
                    quality_score = 0
                    quality_issues.append("Constant value")
                
                if col_type == "identifier":
                    quality_score = 10
                    quality_issues.append("ID column")
                
                # Outlier check for numeric
                outlier_count = 0
                if col_type == "numeric":
                    try:
                        Q1 = col_data.quantile(0.25)
                        Q3 = col_data.quantile(0.75)
                        IQR = Q3 - Q1
                        outliers = ((col_data < Q1 - 1.5 * IQR) | (col_data > Q3 + 1.5 * IQR)).sum()
                        outlier_count = int(outliers)
                        if outlier_count > len(self.kdf) * 0.05:
                            quality_score -= 15
                            quality_issues.append(f"{outlier_count} outliers")
                    except:
                        pass
                
                analysis[col] = {
                    "type": col_type,
                    "importance": importance,
                    "action": action,
                    "reason": reason,
                    "unique_values": unique_count,
                    "missing": missing_count,
                    "missing_pct": round(missing_pct, 2),
                    "outliers": outlier_count,
                    "quality_score": max(0, round(quality_score, 1)),
                    "issues": quality_issues,
                }
            except Exception as e:
                analysis[col] = {"error": str(e)}
        
        return analysis

    def enhanced_health_score(self) -> Dict[str, Any]:
        """
        🏥 ENHANCED HEALTH SCORE
        Comprehensive 0-100 scoring with detailed breakdown:
        - Completeness (missing values)
        - Uniqueness (duplicates)
        - Validity (outliers, types)
        - Consistency (patterns)
        - ML Readiness
        """
        total_cells = len(self.kdf) * len(self.kdf.columns)
        if total_cells == 0:
            return {"score": 0, "grade": "F", "status": "Empty Dataset"}
        
        # 1. Completeness Score (25 points)
        missing_cells = self.kdf.isnull().sum().sum()
        completeness = max(0, 25 - (missing_cells / total_cells * 100))
        
        # 2. Uniqueness Score (20 points)
        duplicate_rows = self.kdf.duplicated().sum()
        uniqueness = max(0, 20 - (duplicate_rows / len(self.kdf) * 100)) if len(self.kdf) > 0 else 20
        
        # 3. Validity Score (20 points)
        validity = 20
        numeric_cols = self.kdf.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            try:
                col_data = self.kdf[col].dropna()
                if len(col_data) > 0:
                    Q1, Q3 = col_data.quantile(0.25), col_data.quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = ((col_data < Q1 - 1.5 * IQR) | (col_data > Q3 + 1.5 * IQR)).sum()
                    outlier_pct = outliers / len(col_data) * 100
                    if outlier_pct > 10:
                        validity -= 2
            except:
                pass
        validity = max(0, validity)
        
        # 4. Consistency Score (15 points) - Check for useless columns
        consistency = 15
        for col in self.kdf.columns:
            try:
                unique_count = self.kdf[col].nunique()
                if unique_count == 1:  # Constant column
                    consistency -= 2
                elif unique_count == len(self.kdf) and self.kdf[col].dtype == 'object':  # ID-like
                    consistency -= 1
            except:
                pass
        consistency = max(0, consistency)
        
        # 5. ML Readiness Score (20 points)
        ml_ready = 20
        if len(numeric_cols) == 0:
            ml_ready -= 10  # No numeric features
        if len(self.kdf) < 100:
            ml_ready -= 5  # Too few samples
        if missing_cells / total_cells > 0.2:
            ml_ready -= 5  # Too much missing
        ml_ready = max(0, ml_ready)
        
        # Total Score
        total = round(completeness + uniqueness + validity + consistency + ml_ready, 1)
        
        # Grade and Status
        if total >= 90: grade, status, color = "A+", "Excellent", "green"
        elif total >= 80: grade, status, color = "A", "Very Good", "green"
        elif total >= 70: grade, status, color = "B", "Good", "blue"
        elif total >= 60: grade, status, color = "C", "Fair", "yellow"
        elif total >= 50: grade, status, color = "D", "Poor", "orange"
        else: grade, status, color = "F", "Critical", "red"
        
        return {
            "score": total,
            "grade": grade,
            "status": status,
            "color": color,
            "breakdown": {
                "completeness": {"score": round(completeness, 1), "max": 25, "label": "Data Completeness"},
                "uniqueness": {"score": round(uniqueness, 1), "max": 20, "label": "Row Uniqueness"},
                "validity": {"score": round(validity, 1), "max": 20, "label": "Data Validity"},
                "consistency": {"score": round(consistency, 1), "max": 15, "label": "Schema Consistency"},
                "ml_readiness": {"score": round(ml_ready, 1), "max": 20, "label": "ML Readiness"},
            },
            "issues": {
                "missing_cells": int(missing_cells),
                "duplicate_rows": int(duplicate_rows),
                "total_columns": len(self.kdf.columns),
                "numeric_columns": len(numeric_cols),
            }
        }

    def feature_engineering_suggestions(self) -> List[Dict[str, Any]]:
        """
        🔧 FEATURE ENGINEERING SUGGESTIONS ENGINE
        Automatically recommend:
        - Encoding strategies
        - Normalization methods
        - Drop suggestions
        - Log transforms
        - Binning
        - Feature combinations
        """
        suggestions = []
        column_analysis = self.smart_column_analysis()
        
        for col, info in column_analysis.items():
            if "error" in info:
                continue
            
            action = info.get("action", "")
            col_type = info.get("type", "")
            reason = info.get("reason", "")
            
            # Generate actionable suggestions
            if action == "drop":
                suggestions.append({
                    "column": col,
                    "action": "DROP",
                    "method": f"df.drop('{col}', axis=1)",
                    "reason": reason,
                    "priority": "high" if col_type in ["constant", "identifier"] else "medium",
                    "icon": "🗑️"
                })
            
            elif action == "encode":
                suggestions.append({
                    "column": col,
                    "action": "ENCODE",
                    "method": f"pd.get_dummies(df, columns=['{col}']) OR LabelEncoder()",
                    "reason": reason,
                    "priority": "high",
                    "icon": "🔢"
                })
            
            elif action == "log_transform":
                suggestions.append({
                    "column": col,
                    "action": "LOG TRANSFORM",
                    "method": f"df['{col}'] = np.log1p(df['{col}'])",
                    "reason": reason,
                    "priority": "high",
                    "icon": "📈"
                })
            
            elif action == "normalize":
                suggestions.append({
                    "column": col,
                    "action": "NORMALIZE",
                    "method": f"from sklearn.preprocessing import StandardScaler",
                    "reason": reason,
                    "priority": "medium",
                    "icon": "⚖️"
                })
            
            elif action == "extract_features":
                suggestions.append({
                    "column": col,
                    "action": "EXTRACT DATETIME",
                    "method": f"df['year'] = df['{col}'].dt.year, etc.",
                    "reason": reason,
                    "priority": "high",
                    "icon": "📅"
                })
            
            # Missing value handling
            if info.get("missing_pct", 0) > 0:
                pct = info["missing_pct"]
                if pct > 50:
                    suggestions.append({
                        "column": col,
                        "action": "DROP COLUMN",
                        "method": f"df.drop('{col}', axis=1)",
                        "reason": f"{pct:.1f}% missing - too much to impute",
                        "priority": "high",
                        "icon": "🗑️"
                    })
                elif pct > 5:
                    suggestions.append({
                        "column": col,
                        "action": "IMPUTE",
                        "method": f"df['{col}'].fillna(df['{col}'].median())",
                        "reason": f"{pct:.1f}% missing - imputation needed",
                        "priority": "medium",
                        "icon": "🩹"
                    })
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        suggestions.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 2))
        
        return suggestions

    def ml_readiness_check(self) -> Dict[str, Any]:
        """
        🤖 ML READINESS CHECK
        Is your data ready for machine learning?
        - Feature count check
        - Sample size check
        - Missing data check
        - Encoding requirements
        - Scaling needs
        """
        checks = []
        score = 100
        
        # 1. Sample Size
        n_samples = len(self.kdf)
        if n_samples >= 1000:
            checks.append({"check": "Sample Size", "status": "pass", "message": f"✅ {n_samples:,} samples - Good for ML"})
        elif n_samples >= 100:
            checks.append({"check": "Sample Size", "status": "warning", "message": f"⚠️ {n_samples} samples - Might need more data"})
            score -= 10
        else:
            checks.append({"check": "Sample Size", "status": "fail", "message": f"❌ Only {n_samples} samples - Insufficient for reliable ML"})
            score -= 30
        
        # 2. Feature Count
        n_features = len(self.kdf.columns)
        if n_features >= 3:
            checks.append({"check": "Feature Count", "status": "pass", "message": f"✅ {n_features} features available"})
        else:
            checks.append({"check": "Feature Count", "status": "fail", "message": f"❌ Only {n_features} features - Need more"})
            score -= 20
        
        # 3. Numeric Features
        numeric_cols = self.kdf.select_dtypes(include=['number']).columns
        if len(numeric_cols) >= 1:
            checks.append({"check": "Numeric Features", "status": "pass", "message": f"✅ {len(numeric_cols)} numeric features ready"})
        else:
            checks.append({"check": "Numeric Features", "status": "warning", "message": "⚠️ No numeric features - encoding needed"})
            score -= 15
        
        # 4. Missing Data
        missing_pct = (self.kdf.isnull().sum().sum() / (len(self.kdf) * len(self.kdf.columns))) * 100
        if missing_pct == 0:
            checks.append({"check": "Missing Data", "status": "pass", "message": "✅ No missing values"})
        elif missing_pct < 5:
            checks.append({"check": "Missing Data", "status": "warning", "message": f"⚠️ {missing_pct:.1f}% missing - Handle before training"})
            score -= 10
        else:
            checks.append({"check": "Missing Data", "status": "fail", "message": f"❌ {missing_pct:.1f}% missing - Must fix first"})
            score -= 25
        
        # 5. Categorical Encoding
        cat_cols = self.kdf.select_dtypes(include=['object', 'category']).columns
        if len(cat_cols) == 0:
            checks.append({"check": "Categorical Encoding", "status": "pass", "message": "✅ No encoding needed"})
        else:
            checks.append({"check": "Categorical Encoding", "status": "warning", "message": f"⚠️ {len(cat_cols)} columns need encoding"})
            score -= 5
        
        # 6. Feature Scaling
        if len(numeric_cols) >= 2:
            try:
                ranges = [(self.kdf[c].max() - self.kdf[c].min()) for c in numeric_cols if self.kdf[c].notna().sum() > 0]
                if ranges and max(ranges) / (min(ranges) + 0.001) > 100:
                    checks.append({"check": "Feature Scaling", "status": "warning", "message": "⚠️ Large range differences - Consider scaling"})
                    score -= 5
                else:
                    checks.append({"check": "Feature Scaling", "status": "pass", "message": "✅ Feature ranges are reasonable"})
            except:
                checks.append({"check": "Feature Scaling", "status": "pass", "message": "✅ Feature ranges OK"})
        
        # Final verdict
        score = max(0, score)
        if score >= 80:
            verdict = "Ready for ML! 🚀"
            verdict_color = "green"
        elif score >= 60:
            verdict = "Almost Ready - Minor fixes needed"
            verdict_color = "yellow"
        else:
            verdict = "Not Ready - Address issues first"
            verdict_color = "red"
        
        return {
            "score": score,
            "verdict": verdict,
            "verdict_color": verdict_color,
            "checks": checks,
            "recommended_models": self._recommend_models()
        }
    
    def _recommend_models(self) -> List[Dict[str, str]]:
        """Recommend suitable ML models based on data characteristics."""
        models = []
        n_samples = len(self.kdf)
        n_features = len(self.kdf.columns)
        numeric_cols = self.kdf.select_dtypes(include=['number']).columns
        
        if n_samples < 100:
            models.append({"name": "Linear Regression/Logistic", "reason": "Small dataset - simple models work best"})
        elif n_samples < 1000:
            models.append({"name": "Random Forest", "reason": "Good for medium datasets"})
            models.append({"name": "XGBoost", "reason": "Handles mixed data well"})
        else:
            models.append({"name": "XGBoost/LightGBM", "reason": "Great for large datasets"})
            models.append({"name": "Neural Networks", "reason": "Consider deep learning"})
        
        if len(numeric_cols) < 5:
            models.append({"name": "Decision Tree", "reason": "Interpretable with few features"})
        
        return models

    def target_aware_analysis(self, target_column: str) -> Dict[str, Any]:
        """
        🎯 TARGET-AWARE ANALYSIS
        Context-driven analysis focused on prediction target:
        - Feature importance estimation
        - Correlation with target
        - Leakage detection
        - Class imbalance (classification)
        - Target distribution (regression)
        """
        if target_column not in self.kdf.columns:
            return {"error": f"Target column '{target_column}' not found"}
        
        target = self.kdf[target_column]
        other_cols = [c for c in self.kdf.columns if c != target_column]
        
        # Determine task type
        unique_values = target.nunique()
        if unique_values <= 10 or target.dtype == 'object':
            task_type = "classification"
        else:
            task_type = "regression"
        
        result = {
            "target_column": target_column,
            "task_type": task_type,
            "target_stats": {},
            "feature_correlations": {},
            "leakage_warnings": [],
            "class_distribution": None,
            "feature_importance_estimate": {},
        }
        
        # Target statistics
        if task_type == "classification":
            result["class_distribution"] = target.value_counts().to_dict()
            # Check imbalance
            counts = target.value_counts()
            if len(counts) >= 2:
                ratio = counts.iloc[0] / counts.iloc[-1]
                if ratio > 10:
                    result["imbalance_warning"] = f"⚠️ Severe class imbalance (ratio: {ratio:.1f}:1). Consider SMOTE or class weights."
                elif ratio > 3:
                    result["imbalance_warning"] = f"⚠️ Moderate imbalance (ratio: {ratio:.1f}:1)"
        else:
            result["target_stats"] = {
                "mean": float(target.mean()),
                "std": float(target.std()),
                "min": float(target.min()),
                "max": float(target.max()),
                "skew": float(target.skew()),
            }
            if abs(result["target_stats"]["skew"]) > 1:
                result["target_warning"] = "⚠️ Target is skewed. Consider log transformation."
        
        # Feature correlations with target
        numeric_cols = self.kdf.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            if col == target_column:
                continue
            try:
                if target.dtype in ['int64', 'float64']:
                    corr = self.kdf[col].corr(target)
                    result["feature_correlations"][col] = round(float(corr), 4)
                    
                    # Leakage detection
                    if abs(corr) > 0.95:
                        result["leakage_warnings"].append({
                            "column": col,
                            "correlation": round(float(corr), 4),
                            "warning": f"🚨 POTENTIAL LEAKAGE: '{col}' has {corr:.2f} correlation with target!"
                        })
            except:
                pass
        
        # Sort correlations by absolute value
        sorted_corrs = dict(sorted(result["feature_correlations"].items(), key=lambda x: abs(x[1]), reverse=True))
        result["feature_correlations"] = sorted_corrs
        
        # Estimate feature importance based on correlation
        for col, corr in sorted_corrs.items():
            abs_corr = abs(corr)
            if abs_corr > 0.7:
                importance = "High"
            elif abs_corr > 0.4:
                importance = "Medium"
            elif abs_corr > 0.1:
                importance = "Low"
            else:
                importance = "Very Low"
            result["feature_importance_estimate"][col] = {"correlation": corr, "importance": importance}
        
        return result

    def get_dataframe(self) -> pd.DataFrame:
        """Return the current DataFrame."""
        return pd.DataFrame(self.kdf)

    # ==================== VISUALIZATION ====================
    
    def _fig_to_base64(self, fig: plt.Figure) -> str:
        """Convert matplotlib figure to base64."""
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight", facecolor="white")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close(fig)
        return f"data:image/png;base64,{image_base64}"

    def corr_heatmap(self) -> Optional[str]:
        """Generate correlation heatmap using kuya."""
        try:
            fig = plt.figure(figsize=(10, 8))
            self.kdf.corr_heatmap()
            fig = plt.gcf()
            return self._fig_to_base64(fig)
        except Exception as e:
            print(f"Heatmap error: {e}")
            return None

    def plot_histogram(self, column: str) -> Optional[str]:
        """Plot histogram for a column."""
        try:
            fig = plt.figure(figsize=(10, 6))
            self.kdf.plot_histogram(column)
            fig = plt.gcf()
            return self._fig_to_base64(fig)
        except Exception as e:
            print(f"Histogram error: {e}")
            return None

    def quick_plot(self, kind: str, x: str = None, y: str = None) -> Optional[str]:
        """Quick plot using kuya's quick_plot."""
        try:
            fig = plt.figure(figsize=(10, 6))
            self.kdf.quick_plot(kind, x=x, y=y)
            fig = plt.gcf()
            return self._fig_to_base64(fig)
        except Exception as e:
            print(f"Quick plot error: {e}")
            return None

    def pairplot(self, columns: List[str] = None) -> Optional[str]:
        """Generate pairplot."""
        try:
            self.kdf.pairplot(columns=columns)
            fig = plt.gcf()
            return self._fig_to_base64(fig)
        except Exception as e:
            print(f"Pairplot error: {e}")
            return None

    def generate_all_graphs(self, selected_features: List[str] = None) -> List[Dict[str, Any]]:
        """
        Generate relevant graphs based on selected features.
        selected_features: list of feature IDs (e.g. ['distribution', 'correlation'])
        """
        if selected_features is None:
            selected_features = ["all"]
            
        run_all = "all" in selected_features or "magic" in selected_features
        graphs = []
        seen_titles = set()
        
        print(f"📈 Generating graphs for features: {selected_features}")
        numeric_cols_debug = self.kdf.select_dtypes(include=["number"]).columns.tolist()
        print(f"🔢 Numeric columns: {numeric_cols_debug}")
        
        # Correlation heatmap
        if run_all or "correlation" in selected_features:
            heatmap = self.corr_heatmap()
            title = "Correlation Heatmap"
            if heatmap and title not in seen_titles:
                graphs.append({
                    "type": "correlation",
                    "title": title,
                    "image": heatmap,
                })
                seen_titles.add(title)
        
        # Histograms for numeric columns
        if run_all or "distribution" in selected_features:
            numeric_cols = self.kdf.select_dtypes(include=["number"]).columns[:5]
            for col in numeric_cols:
                title = f"Distribution of {col}"
                if title in seen_titles: continue

                hist = self.plot_histogram(col) # plot_histogram is correct from file view
                if hist:
                    graphs.append({
                        "type": "histogram",
                        "title": title,
                        "image": hist,
                    })
                    seen_titles.add(title)
        
        # Bar charts for categorical columns
        if run_all or "bar" in selected_features:
            cat_cols = self.kdf.select_dtypes(include=["object", "category"]).columns[:3]
            for col in cat_cols:
                title = f"Top Values in {col}"
                if title in seen_titles: continue

                bar = self.quick_plot("bar", x=col)
                if bar:
                    graphs.append({
                        "type": "bar",
                        "title": title,
                        "image": bar,
                    })
                    seen_titles.add(title)

        # Box plots for numeric columns
        if run_all or "boxplot" in selected_features or "outliers" in selected_features:
            numeric_cols = self.kdf.select_dtypes(include=["number"]).columns[:5]
            for col in numeric_cols:
                title = f"Box Plot of {col}"
                if title in seen_titles: continue
                
                box = self.quick_plot("box", x=col)
                if box:
                    graphs.append({
                        "type": "boxplot",
                        "title": title,
                        "image": box,
                    })
                    seen_titles.add(title)
        
        # Pairplot
        if run_all or "pairplot" in selected_features:
            title = "Pair Plot"
            if title not in seen_titles:
                numeric_cols = self.kdf.select_dtypes(include=["number"]).columns.tolist()
                if len(numeric_cols) >= 2:
                    pair = self.pairplot(columns=numeric_cols[:5]) 
                    if pair:
                        graphs.append({
                            "type": "pairplot",
                            "title": title,
                            "image": pair,
                        })
                        seen_titles.add(title)

        # Scatter plots (all numeric pairs, max 6)
        if run_all or "scatter" in selected_features:
            numeric_cols = self.kdf.select_dtypes(include=["number"]).columns.tolist()
            
            count = 0
            for i in range(len(numeric_cols)):
                if count >= 6: break
                for j in range(i + 1, len(numeric_cols)):
                    if count >= 6: break
                    
                    x_col = numeric_cols[i]
                    y_col = numeric_cols[j]
                    title = f"{x_col} vs {y_col}"
                    
                    if title in seen_titles: continue

                    print(f"🔍 Checking pair {x_col} vs {y_col}")
                    
                    # Try to plot
                    # Fallback to manual if quick_plot returns None
                    scatter = self.quick_plot("scatter", x=x_col, y=y_col)
                    
                    if not scatter:
                        try:
                             # Manually plot using matplotlib
                             print(f"⚠️  Falling back to manual scatter for {x_col} vs {y_col}")
                             plt.clf() # Clear current figure
                             fig = plt.figure(figsize=(10, 6))
                             plt.scatter(self.kdf[x_col], self.kdf[y_col], alpha=0.6)
                             plt.xlabel(str(x_col))
                             plt.ylabel(str(y_col))
                             plt.title(f"Scatter Plot: {x_col} vs {y_col}")
                             plt.grid(True, alpha=0.3)
                             scatter = self._fig_to_base64(fig)
                        except Exception as e:
                             print(f"❌ Manual scatter fallback failed: {e}")

                    if scatter:
                        print(f"✨ Created scatter: {x_col} vs {y_col}")
                        graphs.append({
                            "type": "scatter",
                            "title": title,
                            "image": scatter,
                        })
                        seen_titles.add(title)
                        count += 1
            print(f"✅ Generated {count} scatter plots")
        
        return graphs

    def process_features(self, selected_features: List[str], target_column: Optional[str] = None) -> Dict[str, Any]:
        """
        Run selected analysis features and return all results in a dictionary.
        This allows re-use of logic for both initial upload and re-analysis.
        """
        print(f"⚙️ process_features called with: {selected_features}")
        # Magic Analysis or Select All triggers everything
        run_all = "all" in selected_features or "magic" in selected_features
        
        # ==================== KUYA DATA CLEANING ====================
        cleaning_log = []
        if run_all or "cleaning" in selected_features:
            try:
                self.quick_clean()
                cleaning_log.append("✅ Applied ky.quick_clean() - standardized, fixed types, handled missing, removed outliers")
            except Exception:
                self.standardize_columns()
                cleaning_log.append("✅ Standardized column names")
                self.fix_dtypes()
                cleaning_log.append("✅ Fixed data types")
                self.clean_missing()
                cleaning_log.append("✅ Handled missing values")
        
        cleaned_df = self.get_dataframe()
        
        # ==================== KUYA SUMMARY ====================
        # Always generate basic summary
        summary = self.get_summary()
        
        # ==================== KUYA CORRELATION ====================
        correlation = {}
        if run_all or "correlation" in selected_features:
            correlation = self.correlation_report()
            
        # ==================== KUYA QUALITY REPORT ====================
        quality_score = {}
        if run_all or "quality" in selected_features:
            quality_score = self.quality_report()
            
        # ==================== KUYA SMART ANALYSIS ====================
        smart_analysis = {}
        if run_all or "smart" in selected_features:
            smart_analysis = self.smart_analysis()
            
        # ==================== KUYA MAGIC ANALYZE ====================
        magic_result = {}
        if "magic" in selected_features: # Specific to magic feature
             magic_result = self.magic_analyze(target_col=target_column)
             
        # ==================== KUYA AUTO INSIGHTS ====================
        insights = []
        if run_all or "insights" in selected_features:
            insights = self.auto_insights()
            
        # ==================== DUPLICATES ====================
        duplicates_info = {}
        if run_all or "duplicates" in selected_features or "outliers" in selected_features:
             duplicates_info = self.detect_duplicates()
             
        # ==================== RECOMMENDATIONS ====================
        recommendations = magic_result.get("recommendations", self._generate_recommendations())
        
        # ==================== KUYA VISUALIZATIONS ====================
        graphs = []
        # Add 'outliers' to this list to ensure graph engine starts for boxplots
        graph_features = ["viz", "graphs", "distribution", "boxplot", "bar", "pairplot", "scatter", "outliers"]
        
        # Ensure we have data types ready for graphing if not cleaned
        # Many graphs require numeric columns. If user skipped 'cleaning', types might be object.
        if (run_all or any(f in selected_features for f in graph_features)) and "cleaning" not in selected_features:
             current_numeric = self.kdf.select_dtypes(include=["number"]).columns
             if len(current_numeric) < 2:
                 print("⚠️ Visualizations requested but insufficient numeric columns. Attempting auto-fix...")
                 try:
                     self.fix_dtypes()
                 except Exception as e:
                     print(f"Auto-fix failed: {e}")

        if run_all or any(f in selected_features for f in graph_features):
            graphs = self.generate_all_graphs(selected_features=selected_features)
        
        # ==================== 🔥 THE 5 UNIQUE PILLARS ====================
        # Smart Column Analysis
        column_analysis = self.smart_column_analysis()
        
        # Enhanced Health Score
        health_score = self.enhanced_health_score()
        
        # Feature Engineering Suggestions
        engineering_suggestions = self.feature_engineering_suggestions()
        
        # ML Readiness Check
        ml_readiness = self.ml_readiness_check()
        
        # Target-Aware Analysis (if target provided)
        target_analysis = {}
        if target_column:
            target_analysis = self.target_aware_analysis(target_column)
            
        return {
            "cleaning_log": cleaning_log,
            "cleaned_df": cleaned_df,
            "summary": summary,
            "correlation": correlation,
            "quality_score": quality_score,
            "smart_analysis": smart_analysis,
            "magic_result": magic_result,
            "insights": insights,
            "duplicates_info": duplicates_info,
            "recommendations": recommendations,
            "graphs": graphs,
            # 🔥 NEW PILLARS
            "columnAnalysis": column_analysis,
            "healthScore": health_score,
            "engineeringSuggestions": engineering_suggestions,
            "mlReadiness": ml_readiness,
            "targetAnalysis": target_analysis,
        }

