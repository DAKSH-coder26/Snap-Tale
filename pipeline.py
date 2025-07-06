from story.caption_generator import generate_caption_from_review
from story.story_generator import generate_story_image
from story.drive_uploader import upload_to_drive
from utils.logger import update_log_entry
from utils.order_store import get_customer_by_phone

def process_user_submission(phone_number, image_path, review_text):
    
    customer = get_customer_by_phone(phone_number)
    if not customer:
        print(f"[UGC] ⚠️ Unknown number: {phone_number}")
        return

    order_id = customer["order_id"]
    customer_name = customer["customer_name"]
    print(f"[UGC] Processing submission from {customer_name}")

    caption = generate_caption_from_review(customer_name, review_text)

    if caption.lower().startswith("thanks for"):
        print("[UGC] ⚠️ Skipping story generation due to fallback caption.")
        update_log_entry(order_id, raw_review=review_text, drive_link="review awaited")
        return

    final_image = generate_story_image(
        image_path=image_path,
        caption=caption,
        order_id=order_id
    )

    drive_link = upload_to_drive(final_image, order_id, customer_name) if final_image else "review awaited"

    update_log_entry(order_id, raw_review=review_text, drive_link=drive_link)
