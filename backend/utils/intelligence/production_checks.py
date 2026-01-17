"""
Production Checks Module - PRO + ENTERPRISE tier features
==========================================================
Purpose:
    Assess production readiness and export deployment artifacts.
    All outputs help bridge the gap between analysis and deployment.

Features (Pro):
    - Train-Serve Consistency Checks
    - Exportable Preprocessing Pipeline (sklearn)
    - Saved Artifacts Information
    - Reproducibility Lock (seeds, hashes)
    - Risky Features Flagging

Features (Enterprise):
    - Deployment Readiness Score
    - Data Drift Risk Assessment
    - Schema Change Alerts
    - Versioned Pipeline Export
    - Inference Cost Estimation

Target Users:
    Pro tier: Analysts preparing for production
    Enterprise tier: ML engineers, production systems
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
import hashlib
from datetime import datetime


class ProductionChecker:
    """Production readiness and deployment checks."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # ==================== PRO TIER ====================
    
    def train_serve_consistency_check(self) -> Dict[str, Any]:
        """Check for potential train-serve inconsistencies."""
        issues = []
        
        for col in self.datetime_cols:
            issues.append({
                "type": "datetime",
                "column": col,
                "warning": "DateTime columns may cause train-serve skew",
                "recommendation": "Convert to numeric features (year, month, day) or relative values"
            })
        
        for col in self.categorical_cols:
            if self.df[col].nunique() > 100:
                issues.append({
                    "type": "high_cardinality",
                    "column": col,
                    "warning": "New categories in production will fail",
                    "recommendation": "Use handle_unknown='ignore' in encoder"
                })
        
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
    
    def exportable_preprocessing_pipeline(self) -> Dict[str, Any]:
        """Generate sklearn-ready pipeline code."""
        code_parts = []
        
        code_parts.append("from sklearn.pipeline import Pipeline")
        code_parts.append("from sklearn.compose import ColumnTransformer")
        code_parts.append("from sklearn.preprocessing import StandardScaler, OneHotEncoder")
        code_parts.append("from sklearn.impute import SimpleImputer")
        code_parts.append("")
        
        code_parts.append("numeric_transformer = Pipeline(steps=[")
        code_parts.append("    ('imputer', SimpleImputer(strategy='median')),")
        code_parts.append("    ('scaler', StandardScaler())")
        code_parts.append("])")
        code_parts.append("")
        
        code_parts.append("categorical_transformer = Pipeline(steps=[")
        code_parts.append("    ('imputer', SimpleImputer(strategy='most_frequent')),")
        code_parts.append("    ('encoder', OneHotEncoder(handle_unknown='ignore'))")
        code_parts.append("])")
        code_parts.append("")
        
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
    
    def saved_artifacts_info(self) -> Dict[str, Any]:
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
    
    def reproducibility_lock(self) -> Dict[str, Any]:
        """Generate reproducibility information."""
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
    
    def risky_features_flag(self) -> List[Dict[str, Any]]:
        """Identify risky/unstable features."""
        risky = []
        
        for col in self.numeric_cols:
            issues = []
            
            missing_pct = self.df[col].isnull().sum() / len(self.df) * 100
            if missing_pct > 20:
                issues.append(f"High missing ({missing_pct:.1f}%)")
            
            if self.df[col].std() < 0.01:
                issues.append("Near-zero variance")
            
            skew = self.df[col].skew()
            if abs(skew) > 5:
                issues.append(f"Extreme skewness ({skew:.1f})")
            
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
    
    # ==================== ENTERPRISE TIER ====================
    
    def deployment_readiness_score(self) -> Dict[str, Any]:
        """Overall deployment readiness assessment."""
        score = 100
        issues = []
        
        missing_pct = (self.df.isnull().sum().sum() / self.df.size) * 100
        if missing_pct > 5:
            score -= 15
            issues.append("High missing values need handling")
        
        for col in self.df.columns:
            if self.df[col].nunique() == len(self.df):
                score -= 10
                issues.append(f"Potential ID column: {col}")
        
        for col in self.categorical_cols:
            if self.df[col].nunique() > 100:
                score -= 5
                issues.append(f"High cardinality: {col}")
        
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
    
    def data_drift_risk(self) -> Dict[str, Any]:
        """Assess data drift risk per feature."""
        risks = []
        
        for col in self.numeric_cols:
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
    
    def schema_change_alerts(self) -> Dict[str, Any]:
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
    
    def versioned_pipeline_export(self) -> Dict[str, Any]:
        """Export versioned pipeline information."""
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
    
    def inference_cost_estimation(self) -> Dict[str, Any]:
        """Estimate inference costs."""
        n_features = len(self.df.columns)
        n_numeric = len(self.numeric_cols)
        n_categorical = len(self.categorical_cols)
        
        preprocessing_complexity = n_numeric * 2 + n_categorical * 5
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
