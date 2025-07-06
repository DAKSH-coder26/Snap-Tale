import requests
import os
from dotenv import load_dotenv
from utils.order_store import add_order

load_dotenv()

SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_PASSWORD = os.getenv("SHOPIFY_PASSWORD")
SHOPIFY_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")

def fetch_shopify_orders():
    url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOPIFY_DOMAIN}/admin/api/2024-04/orders.json?status=any"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[Shopify] ❌ Failed to fetch orders: {response.status_code}")
        return

    data = response.json()
    for order in data.get("orders", []):
        order_id = order.get("name")
        name = order["customer"]["first_name"] + " " + order["customer"]["last_name"]
        phone = order["phone"] or order["customer"].get("phone") or "unknown"

        add_order(order_id, name.strip(), phone.strip())

    print("[Shopify] ✅ Synced orders from Shopify")

if __name__ == "__main__":
    fetch_shopify_orders()
