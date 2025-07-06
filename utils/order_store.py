import json
import os

ORDER_FILE = "orders.json"

def load_orders():
    if not os.path.exists(ORDER_FILE):
        return {}
    with open(ORDER_FILE, "r") as f:
        return json.load(f)

def save_orders(orders):
    with open(ORDER_FILE, "w") as f:
        json.dump(orders, f, indent=2)

def mark_order_delivered(order_id):
    orders = load_orders()
    if order_id not in orders:
        print(f"[Orders] ❌ Order ID '{order_id}' not found.")
        return None

    orders[order_id]["delivery"] = 1
    save_orders(orders)
    print(f"[Orders] ✅ Marked order '{order_id}' as delivered.")
    return { "order_id": order_id, **orders[order_id] }

def add_order(order_id, customer_name, phone_number):
    orders = load_orders()
    if order_id in orders:
        print(f"[Orders] ⚠️ Order ID '{order_id}' already exists.")
        return
    orders[order_id] = {
        "customer_name": customer_name,
        "phone_number": phone_number,
        "delivery": 0
    }
    save_orders(orders)
    print(f"[Orders] Added new order '{order_id}'.")

def get_all_orders():
    orders = load_orders()
    return [
        { "order_id": oid, **data }
        for oid, data in orders.items()
        if data.get("delivery") == 0
    ]

def get_customer_by_phone(phone_number):
    orders = load_orders()
    for order_id, data in orders.items():
        if data["phone_number"] == phone_number:
            return { "order_id": order_id, **data }
    return None
