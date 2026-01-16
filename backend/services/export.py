"""
KuyaExport - Multi-format Export Service
Supports: CSV, Excel, PDF, HTML, JSON
"""

import pandas as pd
import io
import json
from typing import Dict, Any, Optional
from datetime import datetime


class ExportService:
    """
    Multi-format data export service:
    - Cleaned CSV
    - Cleaned Excel
    - PDF report
    - HTML report
    - JSON summary
    """

    def __init__(self):
        pass

    def export_csv(self, df: pd.DataFrame) -> bytes:
        """Export DataFrame to CSV bytes."""
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue().encode('utf-8')

    def export_excel(self, df: pd.DataFrame, sheet_name: str = "Cleaned Data") -> bytes:
        """Export DataFrame to Excel bytes."""
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        buffer.seek(0)
        return buffer.getvalue()

    def export_json_summary(
        self, 
        summary: Dict[str, Any],
        correlation: Dict[str, Any],
        insights: list,
        quality_score: Dict[str, Any],
        filename: str = "data.csv"
    ) -> str:
        """Export analysis summary as JSON."""
        export_data = {
            "generated_at": datetime.utcnow().isoformat(),
            "file_analyzed": filename,
            "summary": summary,
            "correlation": correlation,
            "insights": insights,
            "quality_score": quality_score,
        }
        return json.dumps(export_data, indent=2, default=str)

    def export_html_report(
        self,
        summary: Dict[str, Any],
        correlation: Dict[str, Any],
        insights: list,
        quality_score: Dict[str, Any],
        graphs: list,
        data_preview: list,
        filename: str = "data.csv"
    ) -> str:
        """Generate HTML report."""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kuya Data Analysis Report - {filename}</title>
    <style>
        :root {{
            --primary: #8b5cf6;
            --secondary: #6366f1;
            --success: #22c55e;
            --warning: #f59e0b;
            --error: #ef4444;
            --bg: #f8fafc;
            --text: #1e293b;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        h2 {{
            color: var(--primary);
            margin: 2rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--primary);
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        .stat-card {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
        }}
        .stat-value {{ font-size: 2rem; font-weight: bold; }}
        .stat-label {{ opacity: 0.9; font-size: 0.9rem; }}
        .quality-badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-weight: bold;
            font-size: 1.2rem;
        }}
        .quality-A {{ background: #dcfce7; color: #166534; }}
        .quality-B {{ background: #dbeafe; color: #1e40af; }}
        .quality-C {{ background: #fef3c7; color: #92400e; }}
        .quality-D {{ background: #ffedd5; color: #9a3412; }}
        .quality-F {{ background: #fee2e2; color: #991b1b; }}
        .insight {{
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid var(--primary);
            background: #f1f5f9;
            border-radius: 0 8px 8px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        th, td {{
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{ background: #f1f5f9; font-weight: 600; }}
        tr:hover {{ background: #f8fafc; }}
        .graph-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
        }}
        .graph-card {{ text-align: center; }}
        .graph-card img {{ max-width: 100%; border-radius: 8px; }}
        .footer {{
            text-align: center;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e2e8f0;
            color: #64748b;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>📊 Kuya Data Analysis Report</h1>
            <p><strong>File:</strong> {filename}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <h2>📈 Dataset Overview</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{summary.get('rows', 0):,}</div>
                <div class="stat-label">Total Rows</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('columns', 0)}</div>
                <div class="stat-label">Total Columns</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(summary.get('numericColumns', []))}</div>
                <div class="stat-label">Numeric Columns</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('totalMissing', 0)}</div>
                <div class="stat-label">Missing Values</div>
            </div>
        </div>

        <h2>🏆 Data Quality Score</h2>
        <div class="card">
            <div class="quality-badge quality-{quality_score.get('grade', 'C')}">
                Grade: {quality_score.get('grade', 'N/A')} ({quality_score.get('overall_score', 0):.0f}/100)
            </div>
            <p style="margin-top: 1rem;"><strong>Status:</strong> {quality_score.get('status', 'Unknown')}</p>
            <div class="stats-grid" style="margin-top: 1rem;">
                {self._generate_quality_cards(quality_score.get('details', {}))}
            </div>
        </div>

        <h2>💡 AI-Generated Insights</h2>
        <div class="card">
            {''.join(f'<div class="insight">{insight}</div>' for insight in insights[:10])}
        </div>

        <h2>📊 Visualizations</h2>
        <div class="graph-container">
            {''.join(f'<div class="graph-card card"><h3>{g.get("title", "Chart")}</h3><img src="{g.get("image", "")}" alt="{g.get("title", "")}"></div>' for g in graphs[:8])}
        </div>

        <h2>📋 Column Statistics</h2>
        <div class="card">
            {self._generate_stats_table(summary.get('statistics', {}))}
        </div>

        <h2>🔍 Data Preview</h2>
        <div class="card">
            {self._generate_data_table(data_preview[:10])}
        </div>

        <div class="footer">
            <p>Generated by <strong>Kuya Cloud</strong> - Your AI Data Analysis Assistant</p>
            <p>© {datetime.now().year} Kuya Data</p>
        </div>
    </div>
</body>
</html>
"""
        return html

    def _generate_quality_cards(self, details: Dict[str, float]) -> str:
        """Generate HTML for quality detail cards."""
        cards = ""
        for key, value in details.items():
            color = "#22c55e" if value >= 80 else "#f59e0b" if value >= 60 else "#ef4444"
            cards += f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {color};">
                <div style="font-size: 1.5rem; font-weight: bold; color: {color};">{value:.0f}%</div>
                <div style="text-transform: capitalize; color: #64748b;">{key}</div>
            </div>
            """
        return cards

    def _generate_stats_table(self, statistics: Dict[str, Any]) -> str:
        """Generate HTML table for statistics."""
        if not statistics:
            return "<p>No statistics available</p>"
        
        headers = ["Column", "Mean", "Std", "Min", "Max", "Median", "Skewness"]
        rows = ""
        for col, stats in statistics.items():
            rows += f"""
            <tr>
                <td><strong>{col}</strong></td>
                <td>{stats.get('mean', 'N/A'):.2f}</td>
                <td>{stats.get('std', 'N/A'):.2f}</td>
                <td>{stats.get('min', 'N/A'):.2f}</td>
                <td>{stats.get('max', 'N/A'):.2f}</td>
                <td>{stats.get('median', 'N/A'):.2f}</td>
                <td>{stats.get('skewness', 'N/A'):.2f}</td>
            </tr>
            """
        
        return f"""
        <table>
            <thead>
                <tr>{''.join(f'<th>{h}</th>' for h in headers)}</tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        """

    def _generate_data_table(self, data: list) -> str:
        """Generate HTML table for data preview."""
        if not data:
            return "<p>No data available</p>"
        
        headers = list(data[0].keys())
        header_row = ''.join(f'<th>{h}</th>' for h in headers)
        
        rows = ""
        for row in data:
            cells = ''.join(f'<td>{str(v)[:50]}</td>' for v in row.values())
            rows += f"<tr>{cells}</tr>"
        
        return f"""
        <table>
            <thead><tr>{header_row}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
        <p style="color: #64748b; margin-top: 0.5rem;">Showing first {len(data)} rows</p>
        """
