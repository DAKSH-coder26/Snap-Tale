from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
client = Client(account_sid, auth_token)

def send_ugc_request(order_id, customer_name, phone_number):
    to_number = f"whatsapp:{phone_number}"
    message = (
        f"Hi {customer_name} 👋\n\n"
        f"Your order **#{order_id}** was just delivered! 🎁\n"
        "We'd love to feature your feedback. Please send us:\n"
        " 1) A photo wearing/using the product\n"
        " 2) A short review or message\n\n"
        "Your story might be featured on our social media! 📸✨"
    )

    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number
    )

    print(f"[WhatsApp] 📩 UGC request sent to {customer_name} ({phone_number}) ✅")