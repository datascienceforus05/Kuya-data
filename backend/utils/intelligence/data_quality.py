"""
Data Quality Module - FREE tier features
Handles basic data quality checks and insights
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


class DataQualityAnalyzer:
    """Basic data quality analysis (FREE tier)."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    def why_this_matters_basic(self) -> List[Dict[str, str]]:
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
        for col in self.numeric_cols[:3]:
            skewness = self.df[col].skew()
            if abs(skewness) > 2:
                insights.append({
                    "finding": f"Skewed Distribution: {col}",
                    "why": f"Skewness of {skewness:.2f} means outliers dominate. Linear models will be affected.",
                    "action": "Apply log transform or use robust scaling."
                })
                break
        
        return insights
    
    def detect_leakage_basic(self) -> Dict[str, Any]:
        """Basic data leakage detection."""
        warnings_list = []
        
        # Check for ID-like columns
        for col in self.df.columns:
            col_lower = col.lower()
            if any(x in col_lower for x in ['id', 'index', 'key', 'timestamp', 'created', 'updated']):
                warnings_list.append({
                    "column": col,
                    "risk": "high" if 'id' in col_lower else "medium",
                    "warning": f"'{col}' looks like an identifier/timestamp. Including it may cause data leakage."
                })
        
        # Check for near-perfect correlations
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
            "warnings": warnings_list[:3]
        }
    
    def detect_class_imbalance(self) -> Dict[str, Any]:
        """Detect class imbalance in potential target columns."""
        imbalance_info = {}
        
        for col in self.categorical_cols:
            if self.df[col].nunique() <= 10:
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
    
    def outlier_presence_flag(self) -> Dict[str, Any]:
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
            "details": outlier_cols[:5]
        }
    
    def executive_summary_basic(self) -> List[str]:
        """Very short executive summary (3-4 bullets)."""
        summary = []
        
        summary.append(f"📊 Dataset has {len(self.df):,} rows and {len(self.df.columns)} columns.")
        
        completeness = (1 - self.df.isnull().sum().sum() / self.df.size) * 100
        if completeness >= 95:
            summary.append(f"✅ Data is {completeness:.1f}% complete - ready for analysis.")
        else:
            summary.append(f"⚠️ Data is only {completeness:.1f}% complete - consider handling missing values.")
        
        summary.append(f"🔢 {len(self.numeric_cols)} numeric, {len(self.categorical_cols)} categorical columns detected.")
        
        if len(self.numeric_cols) >= 3:
            summary.append("💡 Dataset suitable for regression or classification tasks.")
        
        return summary
    
    def has_significant_outliers(self) -> bool:
        """Helper to check for significant outliers."""
        for col in self.numeric_cols[:5]:
            Q1, Q3 = self.df[col].quantile([0.25, 0.75])
            IQR = Q3 - Q1
            outlier_pct = ((self.df[col] < Q1 - 1.5 * IQR) | (self.df[col] > Q3 + 1.5 * IQR)).sum() / len(self.df)
            if outlier_pct > 0.05:
                return True
        return False
