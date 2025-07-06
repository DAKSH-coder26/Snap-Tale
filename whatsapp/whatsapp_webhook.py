from fastapi import APIRouter, Request, Form
import os
from uuid import uuid4
from pipeline import process_user_submission
from dotenv import load_dotenv
import aiohttp
import base64

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

router = APIRouter()

@router.post("/webhook/whatsapp")
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(default=""),
    From: str = Form(default=""),
    NumMedia: int = Form(default=0),
    MediaUrl0: str = Form(default=""),
    MediaContentType0: str = Form(default=""),
):
    print(f"[WhatsApp-In] Msg from {From} | Media count: {NumMedia}")

    customer_number = From.replace("whatsapp:", "")
    review = Body.strip()
    image_path = None

    if NumMedia and MediaContentType0.startswith("image"):
        img_filename = f"ugc_images/{uuid4().hex}.jpg"
        os.makedirs("ugc_images", exist_ok=True)

        auth_str = f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()
        headers = {"Authorization": f"Basic {auth_b64}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(MediaUrl0, headers=headers) as resp:
                if resp.status == 200:
                    with open(img_filename, "wb") as f:
                        f.write(await resp.read())
                    image_path = img_filename
                    print(f"[WhatsApp-In] 📸 Image saved as {img_filename}")
                else:
                    print(f"[WhatsApp-In] ❌ Failed to download image (HTTP {resp.status})")
                    return {"status": "Failed to download image"}

    if review or image_path:
        process_user_submission(customer_number, image_path, review)
        return "Thanks! We've received your submission 🙏"

    return "Please send an image and a short review 💬📸"
