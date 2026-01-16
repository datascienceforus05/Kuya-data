"""
PDF Report Generator - Generate professional PDF reports
"""

import io
from typing import Dict, Any, List
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class PDFReportGenerator:
    """Generate PDF reports from analysis data."""

    def __init__(self):
        if not HAS_REPORTLAB:
            raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
        
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#8b5cf6'),
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#4f46e5'),
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
        ))
        
        self.styles.add(ParagraphStyle(
            name='Insight',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            borderColor=colors.HexColor('#8b5cf6'),
            borderWidth=1,
            borderPadding=5,
            spaceAfter=5,
        ))

    def generate_report(
        self,
        summary: Dict[str, Any],
        correlation: Dict[str, Any],
        insights: List[str],
        quality_score: Dict[str, Any],
        graphs: List[Dict[str, Any]],
        filename: str = "data.csv",
    ) -> io.BytesIO:
        """Generate a PDF report."""
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
        
        # Title
        elements.append(Paragraph(
            "📊 Kuya Data Analysis Report",
            self.styles['CustomTitle']
        ))
        
        # File info
        elements.append(Paragraph(
            f"<b>File:</b> {filename}<br/><b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['CustomBody']
        ))
        elements.append(Spacer(1, 20))
        
        # Summary section
        elements.append(Paragraph("📈 Dataset Overview", self.styles['CustomHeading']))
        
        summary_data = [
            ["Metric", "Value"],
            ["Total Rows", f"{summary.get('rows', 0):,}"],
            ["Total Columns", str(summary.get('columns', 0))],
            ["Numeric Columns", str(len(summary.get('numericColumns', [])))],
            ["Categorical Columns", str(len(summary.get('categoricalColumns', [])))],
            ["Missing Values", f"{summary.get('totalMissing', 0):,}"],
            ["Missing %", f"{summary.get('missingPercentage', 0):.1f}%"],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Quality Score section
        if quality_score:
            elements.append(Paragraph("🏆 Data Quality Score", self.styles['CustomHeading']))
            
            grade = quality_score.get('grade', 'N/A')
            score = quality_score.get('overall_score', 0)
            status = quality_score.get('status', 'Unknown')
            
            elements.append(Paragraph(
                f"<b>Grade: {grade}</b> ({score:.0f}/100) - {status}",
                self.styles['CustomBody']
            ))
            
            details = quality_score.get('details', {})
            if details:
                quality_data = [["Metric", "Score"]]
                for key, value in details.items():
                    quality_data.append([key.capitalize(), f"{value:.0f}%"])
                
                quality_table = Table(quality_data, colWidths=[2*inch, 1.5*inch])
                quality_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#22c55e')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ]))
                elements.append(quality_table)
            elements.append(Spacer(1, 20))
        
        # Insights section
        if insights:
            elements.append(Paragraph("💡 AI-Generated Insights", self.styles['CustomHeading']))
            
            for insight in insights[:10]:  # Limit to 10 insights
                # Clean up insight text
                clean_insight = insight.replace('**', '').replace('*', '')
                elements.append(Paragraph(f"• {clean_insight}", self.styles['CustomBody']))
            
            elements.append(Spacer(1, 20))
        
        # Statistics section
        stats = summary.get('statistics', {})
        if stats:
            elements.append(Paragraph("📊 Column Statistics", self.styles['CustomHeading']))
            
            stats_data = [["Column", "Mean", "Std", "Min", "Max", "Median"]]
            for col, col_stats in list(stats.items())[:10]:  # Limit columns
                stats_data.append([
                    col[:15],  # Truncate column name
                    f"{col_stats.get('mean', 0):.2f}",
                    f"{col_stats.get('std', 0):.2f}",
                    f"{col_stats.get('min', 0):.2f}",
                    f"{col_stats.get('max', 0):.2f}",
                    f"{col_stats.get('median', 0):.2f}",
                ])
            
            stats_table = Table(stats_data, colWidths=[1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
            ]))
            elements.append(stats_table)
            elements.append(Spacer(1, 20))
        
        # Footer
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            "Generated by Kuya Cloud - Your AI Data Analysis Assistant",
            ParagraphStyle(
                name='Footer',
                parent=self.styles['Normal'],
                fontSize=9,
                textColor=colors.gray,
                alignment=TA_CENTER,
            )
        ))
        elements.append(Paragraph(
            f"© {datetime.now().year} Kuya Data",
            ParagraphStyle(
                name='FooterSmall',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=colors.gray,
                alignment=TA_CENTER,
            )
        ))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
