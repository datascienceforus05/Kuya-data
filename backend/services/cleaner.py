"""
KuyaCleaner - Advanced Data Cleaning Service
Full implementation with ALL PRO features
"""

import pandas as pd
import numpy as np
from typing import Optional, Literal, Dict, Any, List, Tuple
from scipy import stats
import re


class DataCleaner:
    """
    Comprehensive data cleaning service with PRO features:
    - Missing value handling (multiple strategies)
    - Outlier detection and removal
    - Data type fixes
    - Smart column renaming (snake_case)
    - Auto date parsing
    - Duplicate removal
    - Normalization
    - Smart encoding
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_df = df.copy()
        self.cleaning_log = []
        self.column_mapping = {}  # Original -> New name

    def clean_missing(
        self, 
        strategy: Literal["auto", "mean", "median", "mode", "drop", "ffill", "bfill", "zero"] = "auto"
    ) -> pd.DataFrame:
        """
        Handle missing values with multiple strategies.
        """
        missing_before = self.df.isnull().sum().sum()
        
        if strategy == "drop":
            self.df = self.df.dropna()
            self.cleaning_log.append(f"Dropped rows with missing values")
        elif strategy == "ffill":
            self.df = self.df.ffill()
            self.cleaning_log.append("Forward filled missing values")
        elif strategy == "bfill":
            self.df = self.df.bfill()
            self.cleaning_log.append("Backward filled missing values")
        elif strategy == "zero":
            self.df = self.df.fillna(0)
            self.cleaning_log.append("Filled missing values with 0")
        else:
            for column in self.df.columns:
                if self.df[column].isnull().sum() > 0:
                    if strategy == "auto":
                        if self.df[column].dtype in ["int64", "float64"]:
                            skew = self.df[column].skew() if len(self.df[column].dropna()) > 0 else 0
                            if abs(skew) > 1:
                                fill_value = self.df[column].median()
                                method = "median (skewed)"
                            else:
                                fill_value = self.df[column].mean()
                                method = "mean"
                        else:
                            fill_value = self.df[column].mode().iloc[0] if len(self.df[column].mode()) > 0 else "Unknown"
                            method = "mode"
                    elif strategy == "mean":
                        if self.df[column].dtype in ["int64", "float64"]:
                            fill_value = self.df[column].mean()
                            method = "mean"
                        else:
                            fill_value = self.df[column].mode().iloc[0] if len(self.df[column].mode()) > 0 else "Unknown"
                            method = "mode (fallback)"
                    elif strategy == "median":
                        if self.df[column].dtype in ["int64", "float64"]:
                            fill_value = self.df[column].median()
                            method = "median"
                        else:
                            fill_value = self.df[column].mode().iloc[0] if len(self.df[column].mode()) > 0 else "Unknown"
                            method = "mode (fallback)"
                    elif strategy == "mode":
                        fill_value = self.df[column].mode().iloc[0] if len(self.df[column].mode()) > 0 else 0
                        method = "mode"
                    else:
                        continue
                    
                    self.df[column] = self.df[column].fillna(fill_value)
                    self.cleaning_log.append(f"Filled '{column}' using {method}")
        
        missing_after = self.df.isnull().sum().sum()
        return self.df

    def fix_dtypes(self) -> pd.DataFrame:
        """Automatically fix and optimize data types."""
        for column in self.df.columns:
            col_data = self.df[column]
            
            if col_data.isnull().all():
                continue
            
            if col_data.dtype == "object":
                numeric_converted = pd.to_numeric(col_data, errors="coerce")
                if numeric_converted.notna().sum() / len(col_data) > 0.8:
                    self.df[column] = numeric_converted
                    self.cleaning_log.append(f"Converted '{column}' to numeric")
                    continue
                
                # Try datetime
                try:
                    date_converted = pd.to_datetime(col_data, errors="coerce", infer_datetime_format=True)
                    if date_converted.notna().sum() / len(col_data) > 0.8:
                        self.df[column] = date_converted
                        self.cleaning_log.append(f"Converted '{column}' to datetime")
                        continue
                except:
                    pass
                
                self.df[column] = col_data.astype(str).str.strip()
            
            if self.df[column].dtype == "float64":
                if (self.df[column].dropna() % 1 == 0).all():
                    self.df[column] = self.df[column].astype("Int64")
                    self.cleaning_log.append(f"Converted '{column}' from float to int")
        
        return self.df

    def smart_rename_columns(self) -> pd.DataFrame:
        """
        Smart column renaming:
        - Convert to snake_case
        - Remove special characters
        - Lowercase
        - Suggest clean names
        """
        new_columns = {}
        suggestions = {}
        
        for col in self.df.columns:
            original = col
            # Convert to lowercase
            new_col = col.lower()
            # Replace spaces and special chars with underscore
            new_col = re.sub(r'[^a-z0-9]+', '_', new_col)
            # Remove leading/trailing underscores
            new_col = new_col.strip('_')
            # Remove consecutive underscores
            new_col = re.sub(r'_+', '_', new_col)
            
            # Handle empty result
            if not new_col:
                new_col = f"column_{list(self.df.columns).index(col)}"
            
            # Handle duplicates
            if new_col in new_columns.values():
                counter = 1
                while f"{new_col}_{counter}" in new_columns.values():
                    counter += 1
                new_col = f"{new_col}_{counter}"
            
            new_columns[col] = new_col
            if col != new_col:
                suggestions[col] = new_col
        
        self.column_mapping = new_columns
        self.df = self.df.rename(columns=new_columns)
        
        if suggestions:
            self.cleaning_log.append(f"Renamed {len(suggestions)} columns to snake_case")
        
        return self.df

    def auto_parse_dates(self) -> Tuple[pd.DataFrame, List[str]]:
        """
        Automatically detect and parse date columns.
        Returns dataframe and list of detected date columns.
        """
        date_columns = []
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY or DD/MM/YYYY
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        ]
        
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                sample = self.df[col].dropna().head(100).astype(str)
                
                # Check if column matches date patterns
                date_like = 0
                for val in sample:
                    for pattern in date_patterns:
                        if re.search(pattern, str(val)):
                            date_like += 1
                            break
                
                # If >50% look like dates, try to parse
                if date_like / len(sample) > 0.5 if len(sample) > 0 else False:
                    try:
                        parsed = pd.to_datetime(self.df[col], errors='coerce', infer_datetime_format=True)
                        if parsed.notna().sum() / len(self.df) > 0.7:
                            self.df[col] = parsed
                            date_columns.append(col)
                            self.cleaning_log.append(f"Auto-parsed '{col}' as datetime")
                    except:
                        pass
        
        return self.df, date_columns

    def detect_outliers(
        self, 
        method: Literal["iqr", "zscore", "isolation_forest"] = "iqr",
        threshold: float = 1.5
    ) -> Dict[str, List[int]]:
        """Detect outliers in numeric columns."""
        outliers = {}
        numeric_cols = self.df.select_dtypes(include=["number"]).columns
        
        for col in numeric_cols:
            col_data = self.df[col].dropna()
            if len(col_data) == 0:
                continue
            
            if method == "iqr":
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - threshold * IQR
                upper = Q3 + threshold * IQR
                outlier_mask = (self.df[col] < lower) | (self.df[col] > upper)
                outlier_indices = self.df[outlier_mask].index.tolist()
            
            elif method == "zscore":
                z_scores = np.abs(stats.zscore(col_data))
                outlier_idx = np.where(z_scores > threshold)[0]
                outlier_indices = col_data.index[outlier_idx].tolist()
            
            else:
                continue
            
            if outlier_indices:
                outliers[col] = outlier_indices
        
        return outliers

    def remove_outliers(
        self, 
        method: Literal["iqr", "zscore"] = "iqr",
        threshold: float = 1.5,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Remove outliers from specified columns."""
        outliers = self.detect_outliers(method, threshold)
        
        if columns:
            outliers = {k: v for k, v in outliers.items() if k in columns}
        
        all_outlier_indices = set()
        for indices in outliers.values():
            all_outlier_indices.update(indices)
        
        rows_before = len(self.df)
        self.df = self.df.drop(index=list(all_outlier_indices))
        rows_removed = rows_before - len(self.df)
        
        if rows_removed > 0:
            self.cleaning_log.append(f"Removed {rows_removed} outlier rows using {method} method")
        return self.df

    def detect_duplicates(self, subset: Optional[List[str]] = None) -> Dict[str, Any]:
        """Detect duplicate rows and return info."""
        duplicates = self.df.duplicated(subset=subset, keep=False)
        duplicate_count = duplicates.sum()
        duplicate_groups = self.df[duplicates].groupby(list(self.df.columns)).size().reset_index(name='count')
        
        return {
            "total_duplicates": int(duplicate_count),
            "unique_duplicate_patterns": len(duplicate_groups),
            "duplicate_percentage": round(duplicate_count / len(self.df) * 100, 2) if len(self.df) > 0 else 0,
            "duplicate_indices": self.df[duplicates].index.tolist()[:100],  # First 100
        }

    def remove_duplicates(
        self, 
        subset: Optional[List[str]] = None,
        keep: Literal["first", "last", False] = "first"
    ) -> pd.DataFrame:
        """Remove duplicate rows."""
        rows_before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        rows_removed = rows_before - len(self.df)
        
        if rows_removed > 0:
            self.cleaning_log.append(f"Removed {rows_removed} duplicate rows")
        return self.df

    def normalize(
        self, 
        method: Literal["minmax", "zscore", "robust"] = "minmax",
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Normalize numeric columns."""
        numeric_cols = columns or self.df.select_dtypes(include=["number"]).columns.tolist()
        
        for col in numeric_cols:
            if col not in self.df.columns:
                continue
            
            col_data = self.df[col].dropna()
            if len(col_data) == 0:
                continue
                
            if method == "minmax":
                min_val = col_data.min()
                max_val = col_data.max()
                if max_val != min_val:
                    self.df[col] = (self.df[col] - min_val) / (max_val - min_val)
            
            elif method == "zscore":
                mean = col_data.mean()
                std = col_data.std()
                if std != 0:
                    self.df[col] = (self.df[col] - mean) / std
            
            elif method == "robust":
                median = col_data.median()
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                if IQR != 0:
                    self.df[col] = (self.df[col] - median) / IQR
        
        self.cleaning_log.append(f"Normalized columns using {method} method")
        return self.df

    def smart_encode(
        self, 
        method: Literal["auto", "label", "onehot"] = "auto",
        max_categories: int = 10
    ) -> pd.DataFrame:
        """Smart encoding for categorical columns."""
        categorical_cols = self.df.select_dtypes(include=["object", "category"]).columns
        
        for col in categorical_cols:
            n_unique = self.df[col].nunique()
            
            if method == "auto":
                if n_unique <= max_categories:
                    dummies = pd.get_dummies(self.df[col], prefix=col, drop_first=True)
                    self.df = pd.concat([self.df.drop(columns=[col]), dummies], axis=1)
                    self.cleaning_log.append(f"One-hot encoded '{col}'")
                else:
                    self.df[col] = self.df[col].astype("category").cat.codes
                    self.cleaning_log.append(f"Label encoded '{col}'")
            
            elif method == "label":
                self.df[col] = self.df[col].astype("category").cat.codes
                self.cleaning_log.append(f"Label encoded '{col}'")
            
            elif method == "onehot":
                dummies = pd.get_dummies(self.df[col], prefix=col, drop_first=True)
                self.df = pd.concat([self.df.drop(columns=[col]), dummies], axis=1)
                self.cleaning_log.append(f"One-hot encoded '{col}'")
        
        return self.df

    def get_column_type_summary(self) -> Dict[str, Any]:
        """Get detailed summary of column types."""
        type_summary = {
            "numeric": [],
            "categorical": [],
            "datetime": [],
            "boolean": [],
            "mixed": [],
        }
        
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            
            if 'int' in dtype or 'float' in dtype:
                type_summary["numeric"].append({
                    "name": col,
                    "dtype": dtype,
                    "unique": int(self.df[col].nunique()),
                    "missing": int(self.df[col].isnull().sum()),
                })
            elif 'datetime' in dtype:
                type_summary["datetime"].append({
                    "name": col,
                    "dtype": dtype,
                    "range": f"{self.df[col].min()} to {self.df[col].max()}" if not self.df[col].isnull().all() else "N/A",
                })
            elif 'bool' in dtype:
                type_summary["boolean"].append({
                    "name": col,
                    "true_count": int((self.df[col] == True).sum()),
                    "false_count": int((self.df[col] == False).sum()),
                })
            elif 'object' in dtype or 'category' in dtype:
                type_summary["categorical"].append({
                    "name": col,
                    "unique": int(self.df[col].nunique()),
                    "top_values": self.df[col].value_counts().head(5).to_dict(),
                })
            else:
                type_summary["mixed"].append({
                    "name": col,
                    "dtype": dtype,
                })
        
        return type_summary

    def get_cleaning_report(self) -> Dict[str, Any]:
        """Get a summary of all cleaning operations performed."""
        return {
            "operations": self.cleaning_log,
            "total_operations": len(self.cleaning_log),
            "original_shape": self.original_df.shape,
            "final_shape": self.df.shape,
            "rows_changed": self.original_df.shape[0] - self.df.shape[0],
            "column_mapping": self.column_mapping,
            "dtypes": self.df.dtypes.astype(str).to_dict(),
            "memory_usage_mb": round(self.df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        }

    def get_dataframe(self) -> pd.DataFrame:
        """Return the cleaned DataFrame."""
        return self.df
