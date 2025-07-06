import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

def generate_caption_from_review(customer_name: str, raw_review: str) -> str:
    prompt = f"""
You are an expert Instagram caption writer for D2C fashion brands.

Your task is to **convert real customer reviews** into short, authentic Instagram captions — while staying close to the original tone and wording.

🎯 Output Format:
{customer_name} says: “<caption>”

📏 Rules:
- Use the customer's **original words and phrases** wherever possible (light rewording only)
- Keep the core meaning and tone intact
- Max 25 words
- Use appropriate hashtags (1-3), only if they match tone
- Don't use any emojis
- Don't fake positivity — if it's mixed or average, be subtle
- If the review is very negative or sarcastic → just output: {customer_name} says: “Thanks for the feedback!”
- Never invent praise or compliments

📝 Raw Review:
\"\"\"{raw_review}\"\"\"
"""

    try:
        response = model.generate_content(prompt)
        caption = response.text.strip()

        if not caption.lower().startswith(f"{customer_name.lower()} says:"):
            print("[Caption] ⚠️ Invalid format, falling back to default.")
            return f"{customer_name} says: “Thanks for the feedback!”"

        print(f"[Caption] ✅ {caption}")
        return caption

    except Exception as e:
        print(f"[Caption] ❌ Error generating caption: {e}")
        return f"{customer_name} says: “Thanks for the feedback!”"  
if __name__ == '__main__':
    generate_caption_from_review(
    raw_review="I recently got this t-shirt and honestly, I wasn't expecting much at this price point — but wow, was I wrong. The material is super soft and breathable, and it fits like a glove without being too tight or too baggy. I've worn it twice already and it hasn't lost shape after washing, which is a huge plus. The color is exactly as shown online and didn't fade. Even my friends noticed and asked where I got it from. It's the kind of t-shirt you can wear casually at home or even style up with a jacket for a day out. Definitely going to order more in other colors!",
    customer_name="Daksh Bajaj"
)

