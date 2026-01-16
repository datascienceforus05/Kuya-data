"""
PDF Report Generator - Generate professional PDF reports
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
import io
import base64
from datetime import datetime
from typing import Dict, Any


class PDFReportGenerator:
    """
    Generate professional PDF reports from analysis data.
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
        
    def _create_custom_styles(self):
        """Create custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=28,
            textColor=HexColor('#8b5cf6'),
            spaceAfter=30,
            alignment=TA_CENTER,
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=HexColor('#6b7280'),
            spaceAfter=20,
            alignment=TA_CENTER,
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=HexColor('#1f2937'),
            spaceBefore=20,
            spaceAfter=12,
            borderPadding=10,
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=HexColor('#374151'),
            spaceAfter=8,
            leading=16,
        ))
        
        # Insight style
        self.styles.add(ParagraphStyle(
            name='Insight',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=HexColor('#1f2937'),
            leftIndent=20,
            spaceAfter=6,
            bulletIndent=10,
        ))
    
    def _create_header(self, report_id: str, file_name: str) -> list:
        """Create report header elements."""
        elements = []
        
        # Title
        elements.append(Paragraph("Kuya Cloud", self.styles['CustomTitle']))
        elements.append(Paragraph(
            "Data Analysis Report",
            self.styles['CustomSubtitle']
        ))
        
        # Report info
        info_text = f"""
        <b>Report ID:</b> {report_id}<br/>
        <b>File:</b> {file_name}<br/>
        <b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        """
        elements.append(Paragraph(info_text, self.styles['BodyText']))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_summary_section(self, summary: Dict[str, Any]) -> list:
        """Create data summary section."""
        elements = []
        
        elements.append(Paragraph("📊 Data Summary", self.styles['SectionHeader']))
        
        # Summary stats table
        summary_data = [
            ["Metric", "Value"],
            ["Total Rows", f"{summary.get('rows', 0):,}"],
            ["Total Columns", str(summary.get('columns', 0))],
            ["Numeric Columns", str(len(summary.get('numericColumns', [])))],
            ["Categorical Columns", str(len(summary.get('categoricalColumns', [])))],
            ["Missing Values", str(sum(summary.get('missingValues', {}).values()))],
        ]
        
        table = Table(summary_data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#8b5cf6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f9fafb')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_statistics_section(self, summary: Dict[str, Any]) -> list:
        """Create column statistics section."""
        elements = []
        
        statistics = summary.get('statistics', {})
        numeric_cols = summary.get('numericColumns', [])
        
        if not numeric_cols:
            return elements
        
        elements.append(Paragraph("📈 Column Statistics", self.styles['SectionHeader']))
        
        # Create stats table for numeric columns
        headers = ["Column", "Mean", "Std", "Min", "Max"]
        stats_data = [headers]
        
        for col in numeric_cols[:10]:  # Limit to 10 columns
            col_stats = statistics.get(col, {})
            row = [
                col[:20] + "..." if len(col) > 20 else col,
                f"{col_stats.get('mean', 'N/A'):.2f}" if col_stats.get('mean') else "N/A",
                f"{col_stats.get('std', 'N/A'):.2f}" if col_stats.get('std') else "N/A",
                f"{col_stats.get('min', 'N/A'):.2f}" if col_stats.get('min') else "N/A",
                f"{col_stats.get('max', 'N/A'):.2f}" if col_stats.get('max') else "N/A",
            ]
            stats_data.append(row)
        
        table = Table(stats_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#6366f1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f9fafb')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_insights_section(self, insights: list) -> list:
        """Create insights section."""
        elements = []
        
        if not insights:
            return elements
        
        elements.append(Paragraph("💡 Key Insights", self.styles['SectionHeader']))
        
        for i, insight in enumerate(insights, 1):
            # Add emoji based on insight type
            if "Good" in insight or "clean" in insight.lower():
                bullet = "✅"
            elif "Warning" in insight:
                bullet = "⚠️"
            elif "Trend" in insight:
                bullet = "📈"
            else:
                bullet = "•"
            
            elements.append(Paragraph(
                f"{bullet} {insight}",
                self.styles['Insight']
            ))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_correlation_section(self, correlation: Dict) -> list:
        """Create correlation section."""
        elements = []
        
        if not correlation:
            return elements
        
        elements.append(Paragraph("🔗 Correlation Analysis", self.styles['SectionHeader']))
        
        # Create correlation table (limited to 6 columns for readability)
        cols = list(correlation.keys())[:6]
        
        if len(cols) < 2:
            return elements
        
        # Header row
        headers = [""] + cols
        corr_data = [headers]
        
        # Data rows
        for col1 in cols:
            row = [col1[:10] + "..." if len(col1) > 10 else col1]
            for col2 in cols:
                val = correlation.get(col1, {}).get(col2, 0)
                row.append(f"{val:.2f}")
            corr_data.append(row)
        
        col_width = 0.9 * inch
        table = Table(corr_data, colWidths=[1.2*inch] + [col_width] * len(cols))
        
        # Style with conditional formatting
        style_commands = [
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#a855f7')),
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#a855f7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]
        
        table.setStyle(TableStyle(style_commands))
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_footer(self) -> list:
        """Create report footer."""
        elements = []
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            "─" * 60,
            self.styles['BodyText']
        ))
        elements.append(Paragraph(
            "Generated by Kuya Cloud • kuyacloud.com",
            ParagraphStyle(
                name='Footer',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=HexColor('#9ca3af'),
                alignment=TA_CENTER,
                spaceBefore=10,
            )
        ))
        
        return elements
    
    def generate_report(self, report_data: Dict[str, Any]) -> io.BytesIO:
        """
        Generate a complete PDF report.
        
        Args:
            report_data: Dictionary containing report information
            
        Returns:
            BytesIO buffer containing the PDF
        """
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50,
        )
        
        elements = []
        
        # Add report sections
        elements.extend(self._create_header(
            report_data.get('reportId', 'N/A'),
            report_data.get('fileName', 'Unknown File')
        ))
        
        elements.extend(self._create_summary_section(
            report_data.get('summary', {})
        ))
        
        elements.extend(self._create_statistics_section(
            report_data.get('summary', {})
        ))
        
        elements.extend(self._create_insights_section(
            report_data.get('insights', [])
        ))
        
        elements.extend(self._create_correlation_section(
            report_data.get('correlation', {})
        ))
        
        elements.extend(self._create_footer())
        
        # Build PDF
        doc.build(elements)
        
        return buffer
