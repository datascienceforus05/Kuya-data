import { NextRequest, NextResponse } from "next/server";

const CASHFREE_APP_ID = process.env.CASHFREE_APP_ID || "";
const CASHFREE_SECRET_KEY = process.env.CASHFREE_SECRET_KEY || "";
const CASHFREE_API_URL = process.env.CASHFREE_API_URL || (process.env.NODE_ENV === "production"
    ? "https://api.cashfree.com/pg/orders"
    : "https://sandbox.cashfree.com/pg/orders");

interface CreateOrderPayload {
    customerEmail: string;
    customerName: string;
    customerPhone: string;
    amount: number;
    planId?: string;
    planName?: string;
}

export async function POST(request: NextRequest) {
    try {
        const body: CreateOrderPayload = await request.json();
        const { customerEmail, customerName, customerPhone, amount, planId, planName } = body;

        if (!customerEmail || !customerPhone) {
            return NextResponse.json(
                { error: "Customer email and phone are required" },
                { status: 400 }
            );
        }

        if (!amount || amount < 1) {
            return NextResponse.json(
                { error: "Invalid amount" },
                { status: 400 }
            );
        }

        // Generate unique order ID
        const orderId = `order_${Date.now()}_${Math.random().toString(36).substring(7)}`;

        // Create order with Cashfree
        const orderPayload = {
            order_id: orderId,
            order_amount: amount,
            order_currency: "INR",
            customer_details: {
                customer_id: customerEmail.replace(/[^a-zA-Z0-9]/g, "_"),
                customer_name: customerName || "Customer",
                customer_email: customerEmail,
                customer_phone: customerPhone || "+919999999999",
            },
            order_meta: {
                return_url: `${process.env.NEXT_PUBLIC_APP_URL || "https://kuyacloud.vercel.app"}/upgrade-success?order_id=${orderId}&plan=${planId || "pro"}`,
                notify_url: `${process.env.NEXT_PUBLIC_API_URL || "https://kuya-data-backend.onrender.com"}/payment/webhook`,
            },
            order_note: `Kuya Cloud ${planName || "Subscription"} - ₹${amount}/month`,
        };

        const response = await fetch(CASHFREE_API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-version": "2023-08-01",
                "x-client-id": CASHFREE_APP_ID,
                "x-client-secret": CASHFREE_SECRET_KEY,
            },
            body: JSON.stringify(orderPayload),
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("Cashfree order creation failed:", data);
            return NextResponse.json(
                { error: data.message || "Failed to create order" },
                { status: response.status }
            );
        }

        return NextResponse.json({
            success: true,
            orderId: data.order_id,
            paymentSessionId: data.payment_session_id,
            orderAmount: data.order_amount,
        });
    } catch (error) {
        console.error("Payment order creation error:", error);
        return NextResponse.json(
            { error: "Internal server error" },
            { status: 500 }
        );
    }
}
