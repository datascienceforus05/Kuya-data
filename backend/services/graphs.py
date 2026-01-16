"""
KuyaViz - Advanced Visualization Service
Full implementation with ALL PRO features
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Optional, Literal, List, Dict, Any


class GraphGenerator:
    """
    Comprehensive visualization service with PRO features:
    - Missing values chart & heatmap
    - Correlation heatmap
    - Distribution charts
    - Box plots
    - Bar charts
    - Scatter plots
    - Pair plots
    - Feature importance chart
    - Target distribution
    - Skewness visualization
    """

    def __init__(self):
        plt.style.use("seaborn-v0_8-whitegrid")
        self.colors = {
            "primary": "#8b5cf6",
            "secondary": "#6366f1",
            "accent": "#f59e0b",
            "success": "#22c55e",
            "warning": "#f97316",
            "error": "#ef4444",
            "gradient": ["#8b5cf6", "#6366f1", "#4f46e5", "#4338ca"],
        }

    def _fig_to_base64(self, fig: plt.Figure) -> str:
        """Convert matplotlib figure to base64 string."""
        buffer = io.BytesIO()
        fig.savefig(
            buffer, 
            format="png", 
            dpi=150, 
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none"
        )
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close(fig)
        return f"data:image/png;base64,{image_base64}"

    def create_missing_values_chart(self, df: pd.DataFrame) -> Optional[str]:
        """Create a bar chart showing missing values per column."""
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=True)
        
        if missing.empty:
            return None
        
        fig, ax = plt.subplots(figsize=(10, max(6, len(missing) * 0.4)))
        
        colors = plt.cm.Reds(np.linspace(0.3, 0.8, len(missing)))
        
        bars = ax.barh(
            range(len(missing)), 
            missing.values,
            color=colors,
            edgecolor="white",
            linewidth=0.5
        )
        
        ax.set_yticks(range(len(missing)))
        ax.set_yticklabels(missing.index)
        
        # Add percentage labels
        total_rows = len(df)
        for i, (bar, val) in enumerate(zip(bars, missing.values)):
            pct = val / total_rows * 100
            ax.text(
                bar.get_width() + total_rows * 0.01, 
                bar.get_y() + bar.get_height()/2,
                f"{int(val)} ({pct:.1f}%)", 
                va="center",
                fontsize=9,
                fontweight="bold"
            )
        
        ax.set_xlabel("Missing Count", fontsize=12)
        ax.set_title("Missing Values Analysis", fontsize=14, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_missing_heatmap(self, df: pd.DataFrame) -> Optional[str]:
        """Create a heatmap showing missing values pattern."""
        missing_matrix = df.isnull()
        
        if not missing_matrix.any().any():
            return None
        
        # Limit columns for readability
        cols_with_missing = df.columns[missing_matrix.sum() > 0].tolist()
        if not cols_with_missing:
            return None
        
        if len(cols_with_missing) > 20:
            cols_with_missing = cols_with_missing[:20]
        
        # Sample rows if too many
        sample_size = min(100, len(df))
        sample_idx = np.random.choice(len(df), sample_size, replace=False)
        sample_idx = np.sort(sample_idx)
        
        fig, ax = plt.subplots(figsize=(max(8, len(cols_with_missing) * 0.5), 8))
        
        sns.heatmap(
            missing_matrix.iloc[sample_idx][cols_with_missing].astype(int),
            cmap="YlOrRd",
            cbar_kws={"label": "Missing (1) / Present (0)"},
            ax=ax,
            yticklabels=False
        )
        
        ax.set_title("Missing Values Pattern (Sample)", fontsize=14, fontweight="bold")
        ax.set_xlabel("Columns", fontsize=12)
        ax.set_ylabel("Rows (Sample)", fontsize=12)
        
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_correlation_heatmap(
        self, 
        df: pd.DataFrame,
        method: str = "pearson"
    ) -> Optional[str]:
        """Create a correlation heatmap for numeric columns."""
        numeric_df = df.select_dtypes(include=["number"])
        
        if numeric_df.empty or len(numeric_df.columns) < 2:
            return None
        
        # Limit columns
        if len(numeric_df.columns) > 15:
            numeric_df = numeric_df.iloc[:, :15]
        
        try:
            corr_matrix = numeric_df.corr(method=method)
            
            fig, ax = plt.subplots(figsize=(max(8, len(corr_matrix.columns) * 0.6), max(6, len(corr_matrix.columns) * 0.5)))
            
            cmap = sns.diverging_palette(250, 15, s=75, l=40, n=9, as_cmap=True)
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
            
            sns.heatmap(
                corr_matrix,
                mask=mask,
                annot=True,
                fmt=".2f",
                cmap=cmap,
                center=0,
                square=True,
                linewidths=0.5,
                cbar_kws={"shrink": 0.8, "label": "Correlation"},
                ax=ax,
                annot_kws={"size": 8}
            )
            
            ax.set_title("Correlation Heatmap", fontsize=14, fontweight="bold", pad=20)
            plt.xticks(rotation=45, ha="right")
            plt.yticks(rotation=0)
            
            plt.tight_layout()
            return self._fig_to_base64(fig)
        except Exception as e:
            print(f"Correlation heatmap error: {e}")
            return None

    def create_distribution_chart(
        self, 
        df: pd.DataFrame, 
        column: str,
        kind: Literal["hist", "kde", "both"] = "both"
    ) -> Optional[str]:
        """Create distribution chart for a numeric column."""
        if column not in df.columns:
            return None
        
        if df[column].dtype not in ["int64", "float64", "Int64", "Float64"]:
            return None
        
        data = df[column].dropna()
        if len(data) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if kind == "hist":
            ax.hist(data, bins=30, color=self.colors["primary"], edgecolor="white", alpha=0.8)
        elif kind == "kde":
            data.plot.kde(ax=ax, color=self.colors["primary"], linewidth=2)
            ax.fill_between(ax.lines[0].get_xdata(), ax.lines[0].get_ydata(), alpha=0.3, color=self.colors["primary"])
        else:
            ax.hist(data, bins=30, color=self.colors["primary"], edgecolor="white", alpha=0.6, density=True, label="Histogram")
            try:
                data.plot.kde(ax=ax, color=self.colors["secondary"], linewidth=2.5, label="KDE")
            except:
                pass
        
        # Add statistics
        mean_val = data.mean()
        median_val = data.median()
        ax.axvline(mean_val, color=self.colors["accent"], linestyle="--", linewidth=2, label=f"Mean: {mean_val:.2f}")
        ax.axvline(median_val, color=self.colors["success"], linestyle=":", linewidth=2, label=f"Median: {median_val:.2f}")
        
        # Add skewness annotation
        skewness = data.skew()
        ax.text(0.02, 0.98, f"Skewness: {skewness:.2f}", transform=ax.transAxes, 
                fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel("Density" if kind != "hist" else "Count", fontsize=12)
        ax.set_title(f"Distribution of {column}", fontsize=14, fontweight="bold")
        ax.legend(loc="upper right")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_boxplot(
        self, 
        df: pd.DataFrame, 
        columns: Optional[List[str]] = None,
        orient: Literal["v", "h"] = "v"
    ) -> Optional[str]:
        """Create box plot for numeric columns."""
        numeric_df = df.select_dtypes(include=["number"])
        
        if columns:
            numeric_df = numeric_df[[c for c in columns if c in numeric_df.columns]]
        
        if numeric_df.empty:
            return None
        
        # Limit columns
        if len(numeric_df.columns) > 10:
            numeric_df = numeric_df.iloc[:, :10]
        
        # Normalize for comparison
        normalized = (numeric_df - numeric_df.min()) / (numeric_df.max() - numeric_df.min())
        
        fig, ax = plt.subplots(figsize=(max(10, len(numeric_df.columns) * 1.2), 6))
        
        bp = ax.boxplot(
            [normalized[col].dropna() for col in normalized.columns],
            patch_artist=True,
            labels=numeric_df.columns,
            vert=(orient == "v")
        )
        
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(numeric_df.columns)))
        for patch, color in zip(bp["boxes"], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_title("Box Plot Analysis (Normalized)", fontsize=14, fontweight="bold")
        ax.set_ylabel("Normalized Value" if orient == "v" else "")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_bar_chart(
        self, 
        df: pd.DataFrame, 
        column: str,
        top_n: int = 10
    ) -> Optional[str]:
        """Create bar chart for categorical column."""
        if column not in df.columns:
            return None
        
        value_counts = df[column].value_counts().head(top_n)
        
        if len(value_counts) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = plt.cm.viridis(np.linspace(0.3, 0.8, len(value_counts)))
        
        bars = ax.bar(
            range(len(value_counts)), 
            value_counts.values,
            color=colors,
            edgecolor="white",
            linewidth=0.5
        )
        
        ax.set_xticks(range(len(value_counts)))
        ax.set_xticklabels([str(x)[:20] for x in value_counts.index], rotation=45, ha="right")
        
        # Add percentage labels
        total = len(df)
        for bar in bars:
            height = bar.get_height()
            pct = height / total * 100
            ax.text(
                bar.get_x() + bar.get_width()/2., 
                height,
                f"{int(height)}\n({pct:.1f}%)", 
                ha="center", 
                va="bottom",
                fontsize=9,
                fontweight="bold"
            )
        
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        ax.set_title(f"Top {min(top_n, len(value_counts))} Values in '{column}'", fontsize=14, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_scatter_plot(
        self, 
        df: pd.DataFrame, 
        x: str, 
        y: str,
        hue: Optional[str] = None
    ) -> Optional[str]:
        """Create scatter plot with trend line."""
        if x not in df.columns or y not in df.columns:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if hue and hue in df.columns:
            unique_values = df[hue].dropna().unique()[:10]  # Limit categories
            colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(unique_values)))
            
            for value, color in zip(unique_values, colors):
                mask = df[hue] == value
                ax.scatter(
                    df.loc[mask, x], 
                    df.loc[mask, y],
                    c=[color],
                    label=str(value)[:20],
                    alpha=0.6,
                    edgecolor="white",
                    linewidth=0.5
                )
            ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
            ax.scatter(
                df[x], 
                df[y],
                c=[self.colors["primary"]],
                alpha=0.6,
                edgecolor="white",
                linewidth=0.5
            )
        
        # Add trend line
        try:
            valid_mask = df[x].notna() & df[y].notna()
            if valid_mask.sum() > 2:
                z = np.polyfit(df.loc[valid_mask, x], df.loc[valid_mask, y], 1)
                p = np.poly1d(z)
                x_line = np.linspace(df[x].min(), df[x].max(), 100)
                ax.plot(x_line, p(x_line), color=self.colors["accent"], linestyle="--", linewidth=2, label="Trend")
                
                # Calculate R²
                y_pred = p(df.loc[valid_mask, x])
                ss_res = ((df.loc[valid_mask, y] - y_pred) ** 2).sum()
                ss_tot = ((df.loc[valid_mask, y] - df.loc[valid_mask, y].mean()) ** 2).sum()
                r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                ax.text(0.02, 0.98, f"R² = {r2:.3f}", transform=ax.transAxes, 
                        fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        except:
            pass
        
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
        ax.set_title(f"{x} vs {y}", fontsize=14, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_pairplot(
        self, 
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        hue: Optional[str] = None
    ) -> Optional[str]:
        """Create pair plot for numeric columns."""
        numeric_df = df.select_dtypes(include=["number"])
        
        if columns:
            numeric_df = numeric_df[[c for c in columns if c in numeric_df.columns]]
        
        # Limit for performance
        if len(numeric_df.columns) > 5:
            numeric_df = numeric_df.iloc[:, :5]
        
        if len(numeric_df.columns) < 2:
            return None
        
        # Sample for large datasets
        if len(numeric_df) > 1000:
            numeric_df = numeric_df.sample(1000, random_state=42)
        
        try:
            if hue and hue in df.columns:
                plot_df = pd.concat([numeric_df, df.loc[numeric_df.index, hue]], axis=1)
                g = sns.pairplot(
                    plot_df, 
                    hue=hue,
                    palette="viridis",
                    diag_kind="kde",
                    plot_kws={"alpha": 0.6, "s": 20}
                )
            else:
                g = sns.pairplot(
                    numeric_df,
                    diag_kind="kde",
                    plot_kws={"alpha": 0.6, "color": self.colors["primary"], "s": 20},
                    diag_kws={"color": self.colors["secondary"]}
                )
            
            g.fig.suptitle("Pair Plot Analysis", y=1.02, fontsize=14, fontweight="bold")
            
            return self._fig_to_base64(g.fig)
        except Exception as e:
            print(f"Pairplot error: {e}")
            return None

    def create_feature_importance_chart(
        self, 
        importance: Dict[str, float],
        title: str = "Feature Importance"
    ) -> Optional[str]:
        """Create horizontal bar chart for feature importance."""
        if not importance:
            return None
        
        # Sort and limit
        sorted_importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True)[:15])
        
        fig, ax = plt.subplots(figsize=(10, max(6, len(sorted_importance) * 0.4)))
        
        colors = plt.cm.viridis(np.linspace(0.3, 0.8, len(sorted_importance)))[::-1]
        
        y_pos = range(len(sorted_importance))
        bars = ax.barh(
            y_pos, 
            list(sorted_importance.values())[::-1],
            color=colors,
            edgecolor="white",
            linewidth=0.5
        )
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(list(sorted_importance.keys())[::-1])
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{width:.3f}', va='center', fontsize=9)
        
        ax.set_xlabel("Importance Score", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_target_distribution(
        self, 
        df: pd.DataFrame, 
        target_col: str
    ) -> Optional[str]:
        """Create target distribution chart."""
        if target_col not in df.columns:
            return None
        
        target = df[target_col]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if target.dtype in ['int64', 'float64'] and target.nunique() > 10:
            # Continuous - histogram
            ax.hist(target.dropna(), bins=30, color=self.colors["primary"], edgecolor="white", alpha=0.8)
            ax.set_ylabel("Count", fontsize=12)
        else:
            # Categorical - bar chart
            value_counts = target.value_counts()
            colors = plt.cm.viridis(np.linspace(0.3, 0.8, len(value_counts)))
            
            bars = ax.bar(range(len(value_counts)), value_counts.values, color=colors, edgecolor="white")
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels([str(x)[:15] for x in value_counts.index], rotation=45, ha="right")
            
            # Add count labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', 
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            ax.set_ylabel("Count", fontsize=12)
        
        ax.set_xlabel(target_col, fontsize=12)
        ax.set_title(f"Target Distribution: {target_col}", fontsize=14, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_skewness_chart(self, df: pd.DataFrame) -> Optional[str]:
        """Create chart showing skewness of numeric columns."""
        numeric_df = df.select_dtypes(include=["number"])
        
        if numeric_df.empty:
            return None
        
        skewness = numeric_df.skew().sort_values()
        
        fig, ax = plt.subplots(figsize=(10, max(6, len(skewness) * 0.4)))
        
        # Color based on skewness
        colors = ['#ef4444' if abs(s) > 2 else '#f59e0b' if abs(s) > 1 else '#22c55e' for s in skewness.values]
        
        bars = ax.barh(range(len(skewness)), skewness.values, color=colors, edgecolor="white")
        
        ax.set_yticks(range(len(skewness)))
        ax.set_yticklabels(skewness.index)
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        ax.axvline(x=-1, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.axvline(x=1, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        
        ax.set_xlabel("Skewness", fontsize=12)
        ax.set_title("Column Skewness Analysis", fontsize=14, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#22c55e', label='Normal (|skew| ≤ 1)'),
            Patch(facecolor='#f59e0b', label='Moderate (1 < |skew| ≤ 2)'),
            Patch(facecolor='#ef4444', label='High (|skew| > 2)'),
        ]
        ax.legend(handles=legend_elements, loc='lower right')
        
        plt.tight_layout()
        return self._fig_to_base64(fig)

    def quick_plot(
        self, 
        df: pd.DataFrame,
        kind: Literal["hist", "box", "scatter", "bar", "heatmap", "pair", "missing"] = "hist",
        x: Optional[str] = None,
        y: Optional[str] = None,
        hue: Optional[str] = None
    ) -> Optional[str]:
        """Quick plot function - Kuya's main visualization method."""
        if kind == "hist":
            if x:
                return self.create_distribution_chart(df, x)
            else:
                numeric_cols = df.select_dtypes(include=["number"]).columns
                if len(numeric_cols) > 0:
                    return self.create_distribution_chart(df, numeric_cols[0])
        
        elif kind == "box":
            return self.create_boxplot(df)
        
        elif kind == "scatter":
            if x and y:
                return self.create_scatter_plot(df, x, y, hue)
            else:
                numeric_cols = df.select_dtypes(include=["number"]).columns[:2]
                if len(numeric_cols) == 2:
                    return self.create_scatter_plot(df, numeric_cols[0], numeric_cols[1], hue)
        
        elif kind == "bar":
            if x:
                return self.create_bar_chart(df, x)
            else:
                cat_cols = df.select_dtypes(include=["object", "category"]).columns
                if len(cat_cols) > 0:
                    return self.create_bar_chart(df, cat_cols[0])
        
        elif kind == "heatmap":
            return self.create_correlation_heatmap(df)
        
        elif kind == "pair":
            return self.create_pairplot(df, hue=hue)
        
        elif kind == "missing":
            return self.create_missing_heatmap(df)
        
        return None
