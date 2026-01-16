"""
Kuya Cloud - FastAPI Backend
Data cleaning, EDA, and report generation API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, report, payment, auth, admin
import uvicorn

app = FastAPI(
    title="Kuya Cloud API",
    description="API for automated data cleaning and exploratory data analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
# CORS Configuration
origins = [
    "http://localhost:3000",
    "https://kuya-cloud.vercel.app",
]

# Add FRONTEND_URL from env if set
import os
env_frontend = os.getenv("FRONTEND_URL")
if env_frontend:
    origins.append(env_frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel subdomains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(report.router)
app.include_router(payment.router)
app.include_router(auth.router)
app.include_router(admin.router)


def cleanup_old_files():
    """Delete files in uploads directory older than 10 days"""
    import os
    import time
    
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        return
        
    current_time = time.time()
    ten_days_ago = current_time - (10 * 24 * 60 * 60)
    
    print("Running cleanup task for old files...")
    count = 0
    for filename in os.listdir(upload_dir):
        if filename == ".gitkeep":
            continue
            
        file_path = os.path.join(upload_dir, filename)
        try:
            if os.path.isfile(file_path):
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < ten_days_ago:
                    os.remove(file_path)
                    count += 1
                    print(f"Deleted old file: {filename}")
        except Exception as e:
            print(f"Error deleting {filename}: {e}")
            
    print(f"Cleanup complete. Removed {count} files.")


@app.on_event("startup")
async def startup_event():
    cleanup_old_files()


@app.get("/")
async def root():
    return {
        "message": "Welcome to Kuya Cloud API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/user/{email}")
async def get_user_by_email(email: str):
    """Get user profile by email - for frontend compatibility."""
    from utils.db import get_database
    from fastapi.responses import JSONResponse
    from datetime import datetime as dt
    
    try:
        db = get_database()
        users_collection = db.users
        
        user = await users_collection.find_one({"email": email})
        
        if not user:
            # Return default free user if not found
            return JSONResponse(content={
                "email": email,
                "plan": "free",
                "planLimit": 3,
                "usedThisMonth": 0,
                "name": email.split("@")[0],
            })
        
        # Serialize for JSON
        user["_id"] = str(user["_id"])
        
        # Handle datetime fields
        for field in ["createdAt", "lastLogin", "upgradedAt", "subscriptionStart", "paidAt"]:
            if field in user and isinstance(user[field], dt):
                user[field] = user[field].isoformat()
        
        # Ensure plan info exists
        if "plan" not in user:
            user["plan"] = "free"
        if "planLimit" not in user:
            plan_limits = {"free": 3, "starter": 15, "pro": 30, "enterprise": 999999}
            user["planLimit"] = plan_limits.get(user["plan"], 3)
        # Calculate real-time usage from reports
        try:
            reports_collection = db.reports
            now = dt.utcnow()
            start_of_month = dt(now.year, now.month, 1)
            
            real_usage = await reports_collection.count_documents({
                "userEmail": email,
                "createdAt": {"$gte": start_of_month}
            })
            user["usedThisMonth"] = real_usage
        except Exception as ex:
            print(f"Usage calc error: {ex}")
            if "usedThisMonth" not in user:
                user["usedThisMonth"] = 0
        
        return JSONResponse(content=user)
        
    except Exception as e:
        print(f"Get user error: {str(e)}")
        # Return default free user on error
        return JSONResponse(content={
            "email": email,
            "plan": "free",
            "planLimit": 3,
            "usedThisMonth": 0,
        })


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
