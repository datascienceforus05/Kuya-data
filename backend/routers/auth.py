"""
Auth Router - Handle user authentication and registration
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from utils.db import get_database

router = APIRouter(prefix="/auth", tags=["Auth"])


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    image: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr


@router.post("/register")
async def register_user(user: UserRegister):
    """
    Register a new user or update existing user info.
    Called from NextAuth.js signIn callback.
    """
    try:
        db = get_database()
        users_collection = db.users
        
        # Check if user already exists
        existing_user = await users_collection.find_one({"email": user.email})
        
        if existing_user:
            # Update user info (name, image might change)
            await users_collection.update_one(
                {"email": user.email},
                {
                    "$set": {
                        "name": user.name,
                        "image": user.image,
                        "lastLogin": datetime.utcnow(),
                    }
                },
            )
            return JSONResponse(
                content={
                    "message": "User updated",
                    "email": user.email,
                    "plan": existing_user.get("plan", "free"),
                }
            )
        
        # Create new user
        user_doc = {
            "name": user.name,
            "email": user.email,
            "image": user.image,
            "plan": "free",
            "createdAt": datetime.utcnow(),
            "lastLogin": datetime.utcnow(),
        }
        
        await users_collection.insert_one(user_doc)
        
        return JSONResponse(
            content={
                "message": "User registered",
                "email": user.email,
                "plan": "free",
            },
            status_code=201,
        )
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
async def login_user(user: UserLogin):
    """
    Validate user login.
    """
    try:
        db = get_database()
        users_collection = db.users
        
        existing_user = await users_collection.find_one({"email": user.email})
        
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update last login
        await users_collection.update_one(
            {"email": user.email},
            {"$set": {"lastLogin": datetime.utcnow()}},
        )
        
        return JSONResponse(
            content={
                "message": "Login successful",
                "email": user.email,
                "name": existing_user.get("name"),
                "plan": existing_user.get("plan", "free"),
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.get("/user/{email}")
async def get_user(email: str):
    """
    Get user profile by email.
    """
    try:
        db = get_database()
        users_collection = db.users
        
        user = await users_collection.find_one({"email": email})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert ObjectId and datetime for JSON serialization
        user["_id"] = str(user["_id"])
        if "createdAt" in user:
            user["createdAt"] = user["createdAt"].isoformat()
        if "lastLogin" in user:
            user["lastLogin"] = user["lastLogin"].isoformat()
        
        return JSONResponse(content=user)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get user error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")
