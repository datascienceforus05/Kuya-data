"""
Auth Router - Handle user authentication and registration with Email/Password
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import os
from utils.db import get_database

router = APIRouter(prefix="/auth", tags=["Auth"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-kuya-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

security = HTTPBearer()


# --- Models ---

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


# --- Helper Functions ---

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return current user"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        db = get_database()
        user = await db.users.find_one({"email": email})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# --- Endpoints ---

@router.post("/register")
async def register_user(user: UserRegister):
    """
    Register a new user with email and password.
    """
    try:
        db = get_database()
        users_collection = db.users
        
        # Check if user already exists
        existing_user = await users_collection.find_one({"email": user.email})
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        hashed_password = hash_password(user.password)
        
        # Create new user
        user_doc = {
            "name": user.name,
            "email": user.email,
            "password": hashed_password,
            "plan": "free",
            "analysisCount": 0,
            "createdAt": datetime.utcnow(),
            "lastLogin": datetime.utcnow(),
        }
        
        await users_collection.insert_one(user_doc)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return JSONResponse(
            content={
                "message": "Registration successful",
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "name": user.name,
                    "email": user.email,
                    "plan": "free",
                }
            },
            status_code=201,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
async def login_user(user: UserLogin):
    """
    Login with email and password.
    """
    try:
        db = get_database()
        users_collection = db.users
        
        existing_user = await users_collection.find_one({"email": user.email})
        
        if not existing_user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not verify_password(user.password, existing_user.get("password", "")):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Update last login
        await users_collection.update_one(
            {"email": user.email},
            {"$set": {"lastLogin": datetime.utcnow()}},
        )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return JSONResponse(
            content={
                "message": "Login successful",
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "name": existing_user.get("name"),
                    "email": user.email,
                    "plan": existing_user.get("plan", "free"),
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current logged-in user info using JWT token.
    """
    return JSONResponse(
        content={
            "name": current_user.get("name"),
            "email": current_user.get("email"),
            "plan": current_user.get("plan", "free"),
            "analysisCount": current_user.get("analysisCount", 0),
        }
    )


@router.get("/user/{email}")
async def get_user(email: str):
    """
    Get user profile by email. (Public - for checking plan, etc.)
    """
    try:
        db = get_database()
        users_collection = db.users
        
        user = await users_collection.find_one({"email": email})
        
        if not user:
            # Return default free user if not found
            return JSONResponse(content={
                "email": email,
                "plan": "free",
                "analysisCount": 0,
            })
        
        return JSONResponse(content={
            "name": user.get("name"),
            "email": user.get("email"),
            "plan": user.get("plan", "free"),
            "analysisCount": user.get("analysisCount", 0),
        })
        
    except Exception as e:
        print(f"Get user error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")
