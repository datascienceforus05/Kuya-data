"""
Upload Router - Using kuya-data library for file processing
https://pypi.org/project/kuya-data/
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, Any
import kuya as ky
from kuya.core import KuyaDataFrame
import pandas as pd
import numpy as np
import io
import uuid
import json
import math
from datetime import datetime

from services.kuya_service import KuyaDataService
from utils.db import get_database

router = APIRouter(prefix="/upload", tags=["Upload"])


from utils.json_utils import sanitize_for_json


@router.post("")
async def upload_file(
    file: UploadFile = File(...),
    email: Optional[str] = Form(None),
    features: Optional[str] = Form("all"),
    target_column: Optional[str] = Form(None),
):
    """
    Upload a CSV or Excel file for analysis using kuya-data library.
    
    Uses:
    - ky.quick_clean() for one-command cleaning
    - df.smart_analysis() for AI-powered insights
    - df.quality_report() for data quality scoring
    - df.magic_analyze() for comprehensive analysis
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_ext = file.filename.lower().split(".")[-1]
    if file_ext not in ["csv", "xls", "xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only CSV and Excel files are supported.",
        )

    try:
        # Parse features
        selected_features = ["all"]
        if features and features != "all":
            try:
                selected_features = json.loads(features)
            except:
                selected_features = ["all"]

        # Check Plan Limits
        if email:
            db = get_database()
            user = await db.users.find_one({"email": email})
            if user:
                plan = user.get("plan", "free")
                
                # Get usage directly from reports count to be safe
                now = datetime.utcnow()
                start_of_month = datetime(now.year, now.month, 1)
                used_this_month = await db.reports.count_documents({
                    "userEmail": email,
                    "createdAt": {"$gte": start_of_month}
                })
                
                limits = {"free": 3, "starter": 15, "pro": 30, "enterprise": 999999}
                limit = limits.get(plan, 3)
                
                if used_this_month >= limit:
                    raise HTTPException(
                        status_code=403, 
                        detail=f"Plan limit reached ({used_this_month}/{limit}). Please upgrade to continue."
                    )
        
        run_all = "all" in selected_features or "magic" in selected_features
        
        # Read file content
        content = await file.read()
        
        # Use kuya.load() for auto-detection (but we need BytesIO for in-memory)
        if file_ext == "csv":
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))

        if df.empty:
            raise HTTPException(status_code=400, detail="File is empty")

        if len(df) > 100000:
            raise HTTPException(
                status_code=400, 
                detail="File too large. Maximum 100,000 rows supported."
            )

        # Generate Report ID early
        report_id = f"rpt-{uuid.uuid4().hex[:8]}"

        # Save file locally for re-analysis
        import os
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, f"{report_id}.{file_ext}")
        with open(file_path, "wb") as f:
            f.write(content)

        # Store original for comparison
        original_df = df.copy()
        
        # Initialize Kuya Service
        kuya_service = KuyaDataService(df)

        # Process features using the service
        results = kuya_service.process_features(selected_features, target_column)
        
        # Extract results
        cleaning_log = results["cleaning_log"]
        cleaned_df = results["cleaned_df"]
        summary = results["summary"]
        correlation = results["correlation"]
        quality_score = results["quality_score"]
        smart_analysis = results["smart_analysis"]
        magic_result = results["magic_result"]
        insights = results["insights"]
        duplicates_info = results["duplicates_info"]
        recommendations = results["recommendations"]
        graphs = results["graphs"]
        
        # 🔥 Extract NEW PILLARS
        columnAnalysis = results["columnAnalysis"]
        healthScore = results["healthScore"]
        engineeringSuggestions = results["engineeringSuggestions"]
        mlReadiness = results["mlReadiness"]
        targetAnalysis = results["targetAnalysis"]
        
        # ==================== SAVE TO DATABASE ====================
        try:
            db = get_database()
            reports_collection = db.reports
            
            report_doc = sanitize_for_json({
                "reportId": report_id,
                "userEmail": email,
                "fileName": file.filename,
                "fileExt": file_ext, # Save extension
                "createdAt": datetime.utcnow(),
                "library": "kuya-data 0.1.1",
                "selectedFeatures": selected_features,
                "targetColumn": target_column,
                "summary": summary,
                "correlation": correlation,
                "graphs": graphs,
                "insights": insights,
                "cleanedDataHead": cleaned_df.head(20).to_dict(orient="records"),
                "cleaningLog": cleaning_log,
                "qualityScore": quality_score,
                "duplicates": duplicates_info,
                "recommendations": recommendations,
                "smartAnalysis": smart_analysis,
                # 🔥 NEW PILLARS
                "columnAnalysis": columnAnalysis,
                "healthScore": healthScore,
                "engineeringSuggestions": engineeringSuggestions,
                "mlReadiness": mlReadiness,
                "targetAnalysis": targetAnalysis,
            })
            
            await reports_collection.insert_one(report_doc)
            print(f"✅ Report {report_id} saved (using kuya-data library)")

            # Update user usage stats
            if email:
                users_collection = db.users
                await users_collection.update_one(
                    {"email": email},
                    {"$inc": {"usedThisMonth": 1}}
                )
        except Exception as e:
            print(f"❌ Failed to save report: {e}")

        # ==================== PREPARE RESPONSE ====================
        response_data = sanitize_for_json({
            "success": True,
            "reportId": report_id,
            "selectedFeatures": selected_features,
            "fileName": file.filename,
            "library": "kuya-data 0.1.1",
            "summary": summary,
            "correlation": correlation,
            "graphs": graphs,
            "cleanedDataHead": cleaned_df.head(10000).to_dict(orient="records"),
            "insights": insights,
            "cleaningLog": cleaning_log,
            "qualityScore": quality_score,
            "duplicates": duplicates_info,
            "recommendations": recommendations,
            # 🔥 NEW PILLARS
            "columnAnalysis": columnAnalysis,
            "healthScore": healthScore,
            "engineeringSuggestions": engineeringSuggestions,
            "mlReadiness": mlReadiness,
            "targetAnalysis": targetAnalysis,
        })

        return JSONResponse(content=response_data)

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="File is empty or corrupted")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Could not parse file")
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.get("/features")
async def get_available_features():
    """Get available kuya-data features."""
    return JSONResponse(content={
        "library": "kuya-data 0.1.1",
        "pypi": "https://pypi.org/project/kuya-data/",
        "features": [
            {"id": "cleaning", "name": "Quick Clean", "icon": "🧹", "description": "ky.quick_clean() - One command cleaning", "kuya_method": "ky.quick_clean(df)"},
            {"id": "eda", "name": "Summary Stats", "icon": "📊", "description": "df.summary() - Full descriptive summary", "kuya_method": "df.summary()"},
            {"id": "correlation", "name": "Correlation", "icon": "🔗", "description": "df.correlation_report() - Correlation insights", "kuya_method": "df.correlation_report()"},
            {"id": "quality", "name": "Quality Report", "icon": "🏆", "description": "df.quality_report() - Quality scoring", "kuya_method": "df.quality_report()"},
            {"id": "smart", "name": "Smart Analysis", "icon": "🧠", "description": "df.smart_analysis() - AI-powered insights", "kuya_method": "df.smart_analysis()"},
            {"id": "magic", "name": "Magic Analyze", "icon": "🪄", "description": "df.magic_analyze() - Complete analysis", "kuya_method": "df.magic_analyze()"},
            {"id": "insights", "name": "Auto Insights", "icon": "💡", "description": "df.auto_insights() - Automated insights", "kuya_method": "df.auto_insights()"},
            {"id": "duplicates", "name": "Duplicates", "icon": "📋", "description": "df.detect_duplicates() - Find duplicates", "kuya_method": "df.detect_duplicates()"},
            {"id": "viz", "name": "Visualizations", "icon": "📈", "description": "df.corr_heatmap(), df.quick_plot()", "kuya_method": "df.quick_plot()"},
        ]
    })
