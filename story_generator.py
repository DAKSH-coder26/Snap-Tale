import os
import json
import random
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from datetime import datetime

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts")
FONTS = {
    "classic": os.path.join(FONT_DIR, "libre_baskerville.ttf"),
    "modern": os.path.join(FONT_DIR, "montserrat.ttf"),
    "neon": os.path.join(FONT_DIR, "pacifico.ttf"),
    "type": os.path.join(FONT_DIR, "special_elite.ttf"),
    "strong": os.path.join(FONT_DIR, "anton.ttf"),
}

COLOR_PALETTES = {
    "light": ("#FFFFFF", "rgba(0, 0, 0, 150)"),
    "dark": ("#000000", "rgba(255, 255, 255, 150)"),
    "gold": ("#FFD700", "rgba(0, 0, 0, 100)"),
    "pink": ("#FF69B4", "rgba(0, 0, 0, 100)"),
    "cyan": ("#00FFFF", "rgba(0, 0, 0, 100)")
}

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def ask_gemini_for_formatting(caption, image_path):
    try:
        model = genai.GenerativeModel("gemini-pro-vision")
        img_data = Image.open(image_path)

        prompt = f"""
You're a visual designer. Analyze the image and caption below and suggest formatting as JSON:
{{
  "font_style": "modern",
  "palette": "pink",
  "font_size_multiplier": 1.0
}}

Caption: "{caption}"
Only output the JSON.
"""

        response = model.generate_content([prompt, img_data])
        raw = response.text.strip()

        try:
            json_start = raw.find('{')
            json_end = raw.rfind('}') + 1
            return json.loads(raw[json_start:json_end])
        except Exception as e:
            print(f"[Gemini] ⚠️ JSON parsing failed: {e}\nRaw: {raw}")
            raise

    except Exception as e:
        print(f"[Gemini] ⚠️ Formatting fallback: {e}")
        return {
            "font_style": "modern",
            "palette": random.choice(list(COLOR_PALETTES.keys())),
            "font_size_multiplier": 1.0
        }

def generate_story_image(image_path, caption, font_style="modern", save_dir="ugc_stories", order_id=None):
    if not caption or caption.lower().startswith("thanks for"):
        print("[UGC] ⚠️ Skipping story generation due to fallback caption.")
        return None

    os.makedirs(save_dir, exist_ok=True)

    try:
        img = Image.open(image_path).convert("RGB")
    except (UnidentifiedImageError, FileNotFoundError, AttributeError) as e:
        print(f"[StoryGen] ❌ Failed to open image ({image_path}): {e}")
        return None

    config = ask_gemini_for_formatting(caption, image_path)
    font_style = config.get("font_style", "modern")
    palette_key = config.get("palette", "light")
    multiplier = config.get("font_size_multiplier", 1.0)

    draw = ImageDraw.Draw(img, "RGBA")
    font_path = FONTS.get(font_style, FONTS["modern"])
    font_size = int(img.width * 0.05 * multiplier)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"[StoryGen] ⚠️ Font fallback: {e}")
        font = ImageFont.load_default()

    text_color, bg_color = COLOR_PALETTES.get(palette_key, COLOR_PALETTES["light"])

    lines = []
    max_width = int(img.width * 0.8)
    words = caption.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textlength(test_line, font=font) < max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    padding = 20
    line_height = font.getbbox("A")[3] + 10
    text_block_height = line_height * len(lines)
    x = int(img.width * 0.1)
    y = img.height - text_block_height - 3 * padding

    draw.rectangle(
        [(x - padding, y - padding), (x + max_width + padding, y + text_block_height + padding)],
        fill=bg_color
    )

    for i, line in enumerate(lines):
        draw.text((x, y + i * line_height), line, font=font, fill=text_color)

    filename = f"story_{order_id or datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    output_path = os.path.join(save_dir, filename)
    img.save(output_path)
    print(f"[Story] ✅ Saved story image to {output_path}")
    return output_path
