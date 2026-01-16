"""
Admin Router - System monitoring, user management, and manual upgrades
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
from utils.db import get_database
from datetime import datetime, timedelta
import os
import pandas as pd
import io

router = APIRouter(prefix="/admin", tags=["Admin"])

# Admin credentials from environment
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "kuya_admin_2024")

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class UpgradeRequest(BaseModel):
    email: str
    plan: str
    limit: Optional[int] = None

async def verify_admin(x_admin_token: str = Header(None)):
    """Simple token verification for admin routes"""
    # In a real app, use JWT. For now, a simple check.
    expected_token = f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}"
    if x_admin_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized admin access")
    return True

@router.post("/login")
async def admin_login(data: AdminLoginRequest):
    """Verify admin credentials"""
    if data.username == ADMIN_USERNAME and data.password == ADMIN_PASSWORD:
        return {
            "success": True, 
            "token": f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}",
            "message": "Login successful"
        }
    raise HTTPException(status_code=401, detail="Invalid admin credentials")

@router.get("/stats")
async def get_system_stats(admin: bool = Depends(verify_admin)):
    """Get high-level system analytics"""
    try:
        db = get_database()
        
        # User stats
        total_users = await db.users.count_documents({})
        pro_users = await db.users.count_documents({"plan": "pro"})
        starter_users = await db.users.count_documents({"plan": "starter"})
        enterprise_users = await db.users.count_documents({"plan": "enterprise"})
        
        # Report stats
        total_reports = await db.reports.count_documents({})
        
        # Revenue estimate (very basic)
        # In a real app, we'd sum real transaction amounts.
        # Here we check how many users have 'paidAt'
        paid_users = await db.users.count_documents({"paidAt": {"$exists": True}})
        
        # Usage stats (last 30 days)
        last_30_days = datetime.utcnow() - timedelta(days=30)
        recent_reports = await db.reports.count_documents({"createdAt": {"$gte": last_30_days}})
        
        return {
            "users": {
                "total": total_users,
                "pro": pro_users,
                "starter": starter_users,
                "enterprise": enterprise_users,
                "free": total_users - pro_users - starter_users - enterprise_users
            },
            "reports": {
                "total": total_reports,
                "recent30Days": recent_reports
            },
            "revenue": {
                "estimatedTotal": paid_users * 499, # Assuming 499 per pro user
                "paidUsersCount": paid_users
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users")
async def list_users(admin: bool = Depends(verify_admin)):
    """List all registered users"""
    try:
        db = get_database()
        users_cursor = db.users.find().sort("createdAt", -1)
        users = []
        async for user in users_cursor:
            user["_id"] = str(user["_id"])
            # Format dates
            for date_field in ["createdAt", "lastLogin", "upgradedAt", "paidAt"]:
                if date_field in user and isinstance(user[date_field], datetime):
                    user[date_field] = user[date_field].isoformat()
            users.append(user)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upgrade-user")
async def admin_upgrade_user(data: UpgradeRequest, admin: bool = Depends(verify_admin)):
    """Manually upgrade or downgrade a user's plan"""
    try:
        db = get_database()
        
        plan_limits = {
            "free": 3,
            "starter": 15,
            "pro": 30,
            "enterprise": 999999
        }
        
        target_limit = data.limit if data.limit is not None else plan_limits.get(data.plan, 3)
        
        result = await db.users.update_one(
            {"email": data.email},
            {
                "$set": {
                    "plan": data.plan,
                    "planLimit": target_limit,
                    "upgradedAt": datetime.utcnow(),
                    "adminAction": True,
                    "adminNote": f"Manually set to {data.plan} by Admin"
                }
            },
            upsert=True
        )
        
        return {
            "success": True,
            "email": data.email,
            "newPlan": data.plan,
            "newLimit": target_limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reports/recent")
async def get_recent_reports(limit: int = 50, admin: bool = Depends(verify_admin)):
    """Get list of recent analysis reports across all users"""
    try:
        db = get_database()
        reports_cursor = db.reports.find({}, {
            "filename": 1, 
            "userEmail": 1, 
            "createdAt": 1, 
            "fileSize": 1,
            "summary.rows": 1,
            "summary.columns": 1
        }).sort("createdAt", -1).limit(limit)
        
        reports = []
        async for report in reports_cursor:
            report["_id"] = str(report["_id"])
            if "createdAt" in report and isinstance(report["createdAt"], datetime):
                report["createdAt"] = report["createdAt"].isoformat()
            reports.append(report)
        return reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/payments")
async def list_payments(admin: bool = Depends(verify_admin)):
    """List all successful payment transactions"""
    try:
        db = get_database()
        # Find users who have payment data
        cursor = db.users.find(
            {"paidAt": {"$exists": True}},
            {"email": 1, "paidAt": 1, "paymentId": 1, "plan": 1, "orderId": 1}
        ).sort("paidAt", -1)
        
        payments = []
        async for p in cursor:
            p["_id"] = str(p["_id"])
            if "paidAt" in p and isinstance(p["paidAt"], datetime):
                p["paidAt"] = p["paidAt"].isoformat()
            # In a real app, you'd store amount in the transaction, 
            # for now we assume 499 for pro
            p["amount"] = 499
            payments.append(p)
            
        return payments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics")
async def get_analytics_series(admin: bool = Depends(verify_admin)):
    """Get time-series data for users, reports, and payments (last 30 days)"""
    try:
        db = get_database()
        last_30_days = datetime.utcnow() - timedelta(days=30)
        
        # Helper for day-wise aggregation
        async def get_series(collection, date_field):
            pipeline = [
                {"$match": {date_field: {"$gte": last_30_days}}},
                {"$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": f"${date_field}"}},
                    "count": {"$sum": 1}
                }},
                {"$sort": {"_id": 1}}
            ]
            cursor = collection.aggregate(pipeline)
            return {item["_id"]: item["count"] async for item in cursor}

        async def get_revenue_series():
            pipeline = [
                {"$match": {"paidAt": {"$gte": last_30_days}}},
                {"$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$paidAt"}},
                    "revenue": {"$sum": 499} # Fixed fee for now
                }},
                {"$sort": {"_id": 1}}
            ]
            cursor = db.users.aggregate(pipeline)
            return {item["_id"]: item["revenue"] async for item in cursor}

        user_series = await get_series(db.users, "createdAt")
        report_series = await get_series(db.reports, "createdAt")
        revenue_series = await get_revenue_series()
        
        # Combine all dates into a single chart-friendly format
        all_dates = sorted(list(set(list(user_series.keys()) + list(report_series.keys()) + list(revenue_series.keys()))))
        
        chart_data = []
        for d in all_dates:
            chart_data.append({
                "date": d,
                "users": user_series.get(d, 0),
                "reports": report_series.get(d, 0),
                "revenue": revenue_series.get(d, 0)
            })
            
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/{target}")
async def export_data_to_csv(target: str, admin: bool = Depends(verify_admin)):
    """Export platform data to CSV format"""
    try:
        db = get_database()
        data = []
        filename = f"kuya_{target}_{datetime.now().strftime('%Y%m%d')}.csv"
        
        if target == "users":
            cursor = db.users.find()
            async for item in cursor:
                item["_id"] = str(item["_id"])
                data.append(item)
        
        elif target == "reports":
            cursor = db.reports.find({}, {"reportId": 1, "filename": 1, "userEmail": 1, "createdAt": 1, "fileSize": 1})
            async for item in cursor:
                item["_id"] = str(item["_id"])
                data.append(item)
                
        elif target == "payments":
            cursor = db.users.find({"paidAt": {"$exists": True}}, {"email": 1, "paidAt": 1, "paymentId": 1, "orderId": 1, "plan": 1})
            async for item in cursor:
                item["_id"] = str(item["_id"])
                item["amount"] = 499
                data.append(item)
        else:
            raise HTTPException(status_code=400, detail="Invalid export target")

        if not data:
            # Create a minimal empty dataframe with expected columns if no data
            df = pd.DataFrame()
        else:
            df = pd.DataFrame(data)
            # Remove MongoDB internal or nested fields if necessary
            if "_id" in df.columns:
                df = df.drop(columns=["_id"])

        # Convert to CSV in memory
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
