# Snap Tale - UGC Automation Platform

> *Aimed to increase the social media image of Shopify-based brands.*

## 📌 Overview
**Snap Tale** is an automation platform for collecting user-generated content (UGC) tailored for e-commerce brands. It seamlessly integrates with Shopify, WhatsApp, and AI services to collect reviews and turn them into branded social media content.

---

## ✨ Features

- 🛍️ **Order Management**: Syncs with Shopify to track orders.
- 💬 **UGC Collection**: Automatically sends review requests via WhatsApp.
- 🤖 **AI Content Creation**: Generates visually appealing stories from reviews.
- ☁️ **Cloud Storage**: Saves UGC to Google Drive.
- 📊 **Real-time Dashboard**: Displays live order tracking and UGC status.

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Google Cloud Project with Drive API enabled
- Twilio WhatsApp Sandbox setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/snap-tale.git
cd snap-tale
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
nano .env  # Fill in your credentials
```

---

## ⚙️ Required .env Configuration

```ini
# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Shopify
SHOPIFY_API_KEY=your_api_key
SHOPIFY_PASSWORD=your_password
SHOPIFY_STORE_DOMAIN=your-store.myshopify.com

# Google AI
GEMINI_API_KEY=your_gemini_key
```

---

## 🚀 Running the Application

```bash
uvicorn main:app --reload
```

Access the dashboard at: [http://localhost:8000](http://localhost:8000)

---

## 📂 Project Structure

```
snap_tale/
├── frontend/        # Dashboard (index.html)
├── whatsapp/        # Twilio integration
│   ├── whatsapp_handler.py
│   └── whatsapp_webhook.py
├── utils/           # Core functions
│   ├── order_store.py
│   └── logger.py
├── story/           # Content generation
│   ├── caption_generator.py
│   └── story_generator.py
├── fonts/           # Brand fonts
├── ugc_images/      # Customer uploads
├── ugc_stories/     # Generated content
└── main.py          # FastAPI entrypoint
```

---

## 📦 Dependencies

```text
fastapi==0.109.1
uvicorn==0.27.0
python-dotenv==1.0.0
twilio==8.3.0
requests==2.31.0
google-api-python-client==2.118.0
google-auth-oauthlib==1.2.0
google-generativeai==0.3.2
Pillow==10.1.0
aiohttp==3.9.3
python-multipart==0.0.6
```

---

## 🔧 Troubleshooting

- **Issue**: Google Drive authentication fails  
  **Solution**: Delete `token.pickle` and re-authenticate with your Google account.

- **Issue**: WhatsApp messages not sending  
  **Solution**: Double-check Twilio credentials and confirm sandbox setup.

---

## 📜 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
