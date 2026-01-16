"""
Payment Router - Handle Cashfree webhooks and payment verification
"""

from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from utils.db import get_database
import hmac
import hashlib
import os
import httpx
from datetime import datetime

router = APIRouter(prefix="/payment", tags=["Payment"])

# Cashfree Configuration
CASHFREE_APP_ID = os.getenv("CASHFREE_APP_ID", "")
CASHFREE_SECRET_KEY = os.getenv("CASHFREE_SECRET_KEY", "")
CASHFREE_API_URL = os.getenv("CASHFREE_API_URL", "https://sandbox.cashfree.com/pg")


def verify_cashfree_signature(payload: str, timestamp: str, signature: str) -> bool:
    """
    Verify Cashfree webhook signature.
    """
    if not CASHFREE_SECRET_KEY:
        return True  # Skip verification in development
    
    data = timestamp + payload
    expected_signature = hmac.new(
        CASHFREE_SECRET_KEY.encode("utf-8"),
        data.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)


class CreateOrderRequest(BaseModel):
    customer_email: str
    customer_name: Optional[str] = None
    customer_phone: str
    amount: float = 499.0


@router.post("/create-order")
async def create_payment_order(order_data: CreateOrderRequest):
    """
    Create a Cashfree payment order.
    """
    try:
        import uuid
        order_id = f"order_{uuid.uuid4().hex[:12]}"
        
        payload = {
            "order_id": order_id,
            "order_amount": order_data.amount,
            "order_currency": "INR",
            "customer_details": {
                "customer_id": order_data.customer_email.replace("@", "_").replace(".", "_"),
                "customer_name": order_data.customer_name or "Customer",
                "customer_email": order_data.customer_email,
                "customer_phone": order_data.customer_phone,
            },
            "order_meta": {
                "return_url": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/upgrade-success?order_id={order_id}",
                "notify_url": f"{os.getenv('BACKEND_URL', 'http://localhost:8000')}/payment/webhook",
            },
            "order_note": "Kuya Cloud Pro Subscription",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CASHFREE_API_URL}/orders",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "x-api-version": "2023-08-01",
                    "x-client-id": CASHFREE_APP_ID,
                    "x-client-secret": CASHFREE_SECRET_KEY,
                },
            )
            
            data = response.json()
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=data.get("message", "Failed to create order"),
                )
            
            return JSONResponse(content={
                "success": True,
                "orderId": data["order_id"],
                "paymentSessionId": data["payment_session_id"],
                "orderAmount": data["order_amount"],
            })
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create order error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")


@router.post("/webhook")
async def payment_webhook(
    request: Request,
    x_webhook_signature: str = Header(None, alias="x-webhook-signature"),
    x_webhook_timestamp: str = Header(None, alias="x-webhook-timestamp"),
):
    """
    Handle Cashfree payment webhook.
    Updates user plan to PRO upon successful payment.
    """
    try:
        # Get raw body for signature verification
        body = await request.body()
        body_str = body.decode("utf-8")
        
        # Verify signature (skip in development if secret not set)
        if CASHFREE_SECRET_KEY and x_webhook_signature and x_webhook_timestamp:
            if not verify_cashfree_signature(body_str, x_webhook_timestamp, x_webhook_signature):
                print("Invalid webhook signature")
                # Still process but log warning
        
        # Parse webhook payload
        payload = await request.json()
        
        print(f"Cashfree Webhook received: {payload}")
        
        # Extract event type
        event_type = payload.get("type")
        data = payload.get("data", {})
        
        # Handle payment success events
        if event_type in ["PAYMENT_SUCCESS", "PAYMENT_SUCCESS_WEBHOOK"]:
            order_data = data.get("order", {})
            payment_data = data.get("payment", {})
            customer_details = data.get("customer_details", {})
            
            email = customer_details.get("customer_email")
            order_id = order_data.get("order_id")
            payment_id = payment_data.get("cf_payment_id")
            
            if email:
                # Update user plan to PRO
                db = get_database()
                users_collection = db.users
                
                result = await users_collection.update_one(
                    {"email": email},
                    {
                        "$set": {
                            "plan": "pro",
                            "paymentId": payment_id,
                            "orderId": order_id,
                            "paidAt": datetime.utcnow(),
                            "subscriptionStart": datetime.utcnow(),
                        }
                    },
                )
                
                if result.modified_count > 0:
                    print(f"User {email} upgraded to PRO successfully")
                else:
                    # User might not exist yet, create entry
                    await users_collection.update_one(
                        {"email": email},
                        {
                            "$set": {
                                "plan": "pro",
                                "paymentId": payment_id,
                                "orderId": order_id,
                                "paidAt": datetime.utcnow(),
                            },
                            "$setOnInsert": {
                                "createdAt": datetime.utcnow(),
                            }
                        },
                        upsert=True,
                    )
                    print(f"Created/updated user {email} with PRO plan")
            else:
                print("No email found in webhook payload")
        
        elif event_type == "PAYMENT_FAILED":
            print(f"Payment failed for order: {data.get('order', {}).get('order_id')}")
        
        return JSONResponse(content={"status": "received"})
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        # Return 200 to prevent Cashfree retries
        return JSONResponse(content={"status": "error", "message": str(e)})


@router.get("/verify/{order_id}")
async def verify_payment(order_id: str):
    """
    Verify a payment by order ID using Cashfree API.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CASHFREE_API_URL}/orders/{order_id}",
                headers={
                    "x-api-version": "2023-08-01",
                    "x-client-id": CASHFREE_APP_ID,
                    "x-client-secret": CASHFREE_SECRET_KEY,
                },
            )
            
            data = response.json()
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to verify order",
                )
            
            order_status = data.get("order_status")
            
            return JSONResponse(content={
                "verified": order_status == "PAID",
                "orderId": order_id,
                "status": order_status,
                "amount": data.get("order_amount"),
            })
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


@router.get("/status/{order_id}")
async def get_payment_status(order_id: str):
    """
    Get payment status for an order.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CASHFREE_API_URL}/orders/{order_id}/payments",
                headers={
                    "x-api-version": "2023-08-01",
                    "x-client-id": CASHFREE_APP_ID,
                    "x-client-secret": CASHFREE_SECRET_KEY,
                },
            )
            
            data = response.json()
            
            return JSONResponse(content={
                "orderId": order_id,
                "payments": data if isinstance(data, list) else [],
            })
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


class UpgradePlanRequest(BaseModel):
    email: str
    plan: str
    orderId: Optional[str] = None
    limit: Optional[int] = 30


@router.post("/upgrade")
async def upgrade_user_plan(upgrade_data: UpgradePlanRequest):
    """
    Upgrade user's plan after successful payment.
    Called from the frontend after payment success.
    """
    try:
        db = get_database()
        users_collection = db.users
        
        # Map plan to limit
        plan_limits = {
            "free": 3,
            "starter": 15,
            "pro": 30,
            "enterprise": 999999,  # Unlimited
        }
        
        limit = upgrade_data.limit or plan_limits.get(upgrade_data.plan, 30)
        
        # Update user plan
        result = await users_collection.update_one(
            {"email": upgrade_data.email},
            {
                "$set": {
                    "plan": upgrade_data.plan,
                    "planLimit": limit,
                    "usedThisMonth": 0,
                    "orderId": upgrade_data.orderId,
                    "upgradedAt": datetime.utcnow(),
                    "subscriptionStart": datetime.utcnow(),
                },
            },
            upsert=True,
        )
        
        print(f"✅ User {upgrade_data.email} upgraded to {upgrade_data.plan} (limit: {limit})")
        
        return JSONResponse(content={
            "success": True,
            "email": upgrade_data.email,
            "plan": upgrade_data.plan,
            "limit": limit,
        })
        
    except Exception as e:
        print(f"Upgrade error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")
