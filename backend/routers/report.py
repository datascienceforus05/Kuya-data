"""
Report Router - Generate and export reports in multiple formats
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from typing import Optional
import io
from datetime import datetime

from utils.db import get_database
from services.export import ExportService
from services.pdf_generator import PDFReportGenerator

router = APIRouter(prefix="/report", tags=["Report"])

from services.kuya_service import KuyaDataService
import pandas as pd
import os
import json
from pydantic import BaseModel
from typing import List
from utils.json_utils import sanitize_for_json

class ReanalyzeRequest(BaseModel):
    features: List[str]
    target_column: Optional[str] = None

@router.post("/{report_id}/reanalyze")
async def reanalyze_report(report_id: str, request: ReanalyzeRequest):
    """Re-run analysis on an existing report with selected features."""
    try:
        db = get_database()
        reports_collection = db.reports
        
        # Get existing report to find file extension/original file info
        report = await reports_collection.find_one({"reportId": report_id})
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
            
        file_ext = report.get("fileExt", "csv")
        file_path = os.path.join("uploads", f"{report_id}.{file_ext}")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Original file not found on server")
            
        # Load file
        if file_ext == "csv":
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        # Initialize Service
        kuya_service = KuyaDataService(df)
        
        # Process new features
        results = kuya_service.process_features(request.features, request.target_column)
        
        # Update Report in DB
        update_data = sanitize_for_json({
            "selectedFeatures": request.features,
            "targetColumn": request.target_column,
            "summary": results["summary"],
            "correlation": results["correlation"],
            "graphs": results["graphs"],
            "insights": results["insights"],
            "cleanedDataHead": results["cleaned_df"].head(10000).to_dict(orient="records"),
            "cleaningLog": results["cleaning_log"],
            "qualityScore": results["quality_score"],
            "duplicates": results["duplicates_info"],
            "recommendations": results["recommendations"],
            "smartAnalysis": results["smart_analysis"],
            # 🔥 NEW PILLARS
            "columnAnalysis": results["columnAnalysis"],
            "healthScore": results["healthScore"],
            "engineeringSuggestions": results["engineeringSuggestions"],
            "mlReadiness": results["mlReadiness"],
            "targetAnalysis": results["targetAnalysis"],
            "updatedAt": datetime.utcnow()
        })
        
        await reports_collection.update_one(
            {"reportId": report_id},
            {"$set": update_data}
        )
        
        # Prepare Response
        response_data = sanitize_for_json({
            "success": True,
            "reportId": report_id,
            "selectedFeatures": request.features,
            "summary": results["summary"],
            "correlation": results["correlation"],
            "graphs": results["graphs"],
            "cleanedDataHead": results["cleaned_df"].head(10000).to_dict(orient="records"),
            "insights": results["insights"],
            "cleaningLog": results["cleaning_log"],
            "qualityScore": results["quality_score"],
            "duplicates": results["duplicates_info"],
            "recommendations": results["recommendations"],
            # 🔥 NEW PILLARS - ADDING HERE FOR FRONTEND
            "columnAnalysis": results["columnAnalysis"],
            "healthScore": results["healthScore"],
            "engineeringSuggestions": results["engineeringSuggestions"],
            "mlReadiness": results["mlReadiness"],
            "targetAnalysis": results["targetAnalysis"],
        })
        
        print(f"📡 Sending {len(results.get('graphs', []))} graphs and new intelligence pillars to frontend")
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        print(f"Re-analysis error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/user/{email}")
async def get_user_reports(email: str):
    """Get all reports for a user."""
    try:
        db = get_database()
        reports_collection = db.reports
        
        # Find all reports for this user
        cursor = reports_collection.find({"userEmail": email}).sort("createdAt", -1).limit(50)
        reports = await cursor.to_list(length=50)
        
        # Format for response
        formatted_reports = []
        for report in reports:
            formatted_reports.append({
                "_id": str(report.get("_id")),
                "reportId": report.get("reportId"),
                "fileName": report.get("fileName"),
                "createdAt": report.get("createdAt").isoformat() if report.get("createdAt") else None,
            })
        
        return JSONResponse(content={"reports": formatted_reports, "total": len(formatted_reports)})
        
    except Exception as e:
        print(f"Error fetching user reports: {e}")
        return JSONResponse(content={"reports": [], "total": 0})


@router.get("/{report_id}")
async def download_pdf_report(report_id: str):
    """Download PDF report for a given report ID."""
    try:
        db = get_database()
        reports_collection = db.reports
        
        report = await reports_collection.find_one({"reportId": report_id})
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Generate PDF
        pdf_gen = PDFReportGenerator()
        pdf_buffer = pdf_gen.generate_report(
            summary=report.get("summary", {}),
            correlation=report.get("correlation", {}),
            insights=report.get("insights", []),
            quality_score=report.get("qualityScore", {}),
            graphs=report.get("graphs", []),
            filename=report.get("fileName", "data.csv"),
        )
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=kuya-report-{report_id}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"PDF generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF report")


@router.get("/{report_id}/data")
async def get_report_data(report_id: str):
    """Get report data as JSON."""
    try:
        db = get_database()
        reports_collection = db.reports
        
        report = await reports_collection.find_one({"reportId": report_id})
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Remove MongoDB _id field
        report.pop("_id", None)
        
        # Convert datetime
        if "createdAt" in report:
            report["createdAt"] = report["createdAt"].isoformat()
        
        return JSONResponse(content=report)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching report: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch report data")


@router.get("/{report_id}/export/csv")
async def export_csv(report_id: str):
    """Export cleaned data as CSV."""
    try:
        db = get_database()
        reports_collection = db.reports
        
        report = await reports_collection.find_one({"reportId": report_id})
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        data = report.get("cleanedDataHead", [])
        if not data:
            raise HTTPException(status_code=404, detail="No data available")
        
        # Convert to CSV
        import pandas as pd
        df = pd.DataFrame(data)
        
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffer.getvalue().encode()),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=kuya-cleaned-{report_id}.csv"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"CSV export error: {e}")
        raise HTTPException(status_code=500, detail="Failed to export CSV")


@router.get("/{report_id}/export/excel")
async def export_excel(report_id: str):
    """Export cleaned data as Excel."""
    try:
        db = get_database()
        reports_collection = db.reports
        
        report = await reports_collection.find_one({"reportId": report_id})
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        data = report.get("cleanedDataHead", [])
        if not data:
            raise HTTPException(status_code=404, detail="No data available")
        
        # Convert to Excel
        import pandas as pd
        df = pd.DataFrame(data)
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Cleaned Data', index=False)
            
            # Add summary sheet
            summary = report.get("summary", {})
            if summary:
                summary_data = {
                    "Metric": ["Rows", "Columns", "Missing Values", "Quality Score"],
                    "Value": [
                        summary.get("rows", "N/A"),
                        summary.get("columns", "N/A"),
                        summary.get("totalMissing", "N/A"),
                        report.get("qualityScore", {}).get("overall_score", "N/A"),
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        buffer.seek(0)
        
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=kuya-report-{report_id}.xlsx"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Excel export error: {e}")
        raise HTTPException(status_code=500, detail="Failed to export Excel")


@router.get("/{report_id}/export/json")
async def export_json(report_id: str):
    """Export analysis summary as JSON."""
    try:
        db = get_database()
        reports_collection = db.reports
        
        report = await reports_collection.find_one({"reportId": report_id})
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        export_service = ExportService()
        json_content = export_service.export_json_summary(
            summary=report.get("summary", {}),
            correlation=report.get("correlation", {}),
            insights=report.get("insights", []),
            quality_score=report.get("qualityScore", {}),
            filename=report.get("fileName", "data.csv"),
        )
        
        return StreamingResponse(
            io.BytesIO(json_content.encode()),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=kuya-summary-{report_id}.json"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"JSON export error: {e}")
        raise HTTPException(status_code=500, detail="Failed to export JSON")


@router.get("/{report_id}/export/html")
async def export_html(report_id: str):
    """Export full HTML report."""
    try:
        db = get_database()
        reports_collection = db.reports
        
        report = await reports_collection.find_one({"reportId": report_id})
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        export_service = ExportService()
        html_content = export_service.export_html_report(
            summary=report.get("summary", {}),
            correlation=report.get("correlation", {}),
            insights=report.get("insights", []),
            quality_score=report.get("qualityScore", {}),
            graphs=report.get("graphs", []),
            data_preview=report.get("cleanedDataHead", []),
            filename=report.get("fileName", "data.csv"),
        )
        
        return StreamingResponse(
            io.BytesIO(html_content.encode()),
            media_type="text/html",
            headers={
                "Content-Disposition": f"attachment; filename=kuya-report-{report_id}.html"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"HTML export error: {e}")
        raise HTTPException(status_code=500, detail="Failed to export HTML")


@router.get("/{report_id}/view")
async def view_html_report(report_id: str):
    """View HTML report in browser."""
    try:
        db = get_database()
        reports_collection = db.reports
        
        report = await reports_collection.find_one({"reportId": report_id})
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        export_service = ExportService()
        html_content = export_service.export_html_report(
            summary=report.get("summary", {}),
            correlation=report.get("correlation", {}),
            insights=report.get("insights", []),
            quality_score=report.get("qualityScore", {}),
            graphs=report.get("graphs", []),
            data_preview=report.get("cleanedDataHead", []),
            filename=report.get("fileName", "data.csv"),
        )
        
        return HTMLResponse(content=html_content)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"HTML view error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate HTML view")
