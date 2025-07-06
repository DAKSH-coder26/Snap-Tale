from fastapi_utils.tasks import repeat_every
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from whatsapp.whatsapp_handler import send_ugc_request
from utils.order_store import load_orders, mark_order_delivered, add_order
from utils.logger import read_log, log_initial_request
from whatsapp.whatsapp_webhook import router as whatsapp_router
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()
app.include_router(whatsapp_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")
@app.get("/orders")
def get_pending_orders():
    orders = load_orders()
    pending = [
        { "order_id": oid, **data }
        for oid, data in orders.items()
        if data.get("delivery") == 0
    ]
    return pending

@app.get("/ugc_logs")
def get_logged_orders():
    return read_log()

@app.post("/create_order")
async def create_order(req: Request):
    data = await req.json()
    add_order(data["order_id"], data["customer_name"], data["phone_number"])
    return {"status": "order created"}

@app.post("/mark_delivered")
def mark_as_delivered(order_id: str):
    order = mark_order_delivered(order_id)
    if not order:
        return JSONResponse({"error": "Order not found"}, status_code=404)

    send_ugc_request(order_id, order["customer_name"], order["phone_number"])
    log_initial_request(order_id, order["customer_name"], order["phone_number"])
    return {"status": "marked as delivered and message sent"}

@app.get("/sync_orders")
def sync_orders_from_shopify():
    api_key = os.getenv("SHOPIFY_API_KEY")
    password = os.getenv("SHOPIFY_PASSWORD")
    store = os.getenv("SHOPIFY_STORE_DOMAIN")

    url = f"https://{api_key}:{password}@{store}/admin/api/2023-07/orders.json?status=any&financial_status=paid"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch from Shopify", "status": response.status_code}

    shopify_orders = response.json().get("orders", [])
    new_count = 0

    for order in shopify_orders:
        order_id = order.get("name")
        customer = order.get("customer", {})
        name = f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip()
        phone = customer.get("phone") or order.get("shipping_address", {}).get("phone", "")
        fulfillment_status = order.get("fulfillment_status")

        if not phone:
            continue

        existing = load_orders()

        if order_id not in existing:
            # new order
            add_order(order_id, name, phone)
            new_count += 1
        else:
            # already exists
            order_data = existing[order_id]
            if fulfillment_status == "fulfilled" and order_data.get("delivery") == 0:
                print(f"[Shopify Sync] ✅ Order {order_id} marked as fulfilled — triggering delivery pipeline")
                mark_order_delivered(order_id)
                send_ugc_request(order_id, name, phone)
                log_initial_request(order_id, name, phone)

    return {"status": "sync complete", "new_orders_added": new_count}
@app.on_event("startup")
@repeat_every(seconds=15) 
def periodic_sync_orders() -> None:
    print("🔄 Auto-syncing orders from Shopify...")
    try:
        sync_orders_from_shopify()
    except Exception as e:
        print(f"⚠️ Error during auto-sync: {e}")