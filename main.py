import os
import asyncio
import requests
from datetime import datetime
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PHOTO_URL = os.getenv("PHOTO_URL")
CONTACT_NUMBER = os.getenv("CONTACT_NUMBER")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ===== MEMORY =====
memory = {}
names = {}

def remember(uid, text):
    memory.setdefault(uid, []).append(text)

def last_msgs(uid):
    return "\n".join(memory.get(uid, [])[-6:])

def extract_name(text):
    t = text.lower()
    for k in ["my name is", "i am", "i'm", "mai", "main"]:
        if k in t:
            return t.split(k)[-1].strip().split()[0].capitalize()
    return None

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📞 Contact", callback_data="contact")],
        [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/_prashant__pandey/")]
    ]

    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption="Hi, I am *Pratigya-AI* 🍃\nYour human-like AI friend.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ===== BUTTON =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "contact":
        await q.edit_message_caption(caption=f"📞 Contact: {CONTACT_NUMBER}")

# ===== AI REPLY =====
def ai_reply(uid, text):
    chat_memory = last_msgs(uid)
    name = names.get(uid, "")

    prompt = f"""
You are Pratigya, a sweet human-like girl chatting on Telegram.
Talk in soft Hindi/Hinglish like a real caring friend.
Never sound like AI.

User name: {name}

Recent chats:
{chat_memory}

User: {text}
Pratigya:
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini Error:", e)
        return "Network thoda slow hai… ek sec 🙂"

# ===== CHAT =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    text = update.message.text

    name = extract_name(text)
    if name:
        names[uid] = name

    remember(uid, text)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(2)

    reply = ai_reply(uid, text)
    remember(uid, reply)

    await update.message.reply_text(reply)

# ===== WEATHER =====
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()
    if "main" in data:
        msg = f"{city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
    else:
        msg = "City not found ❌"
    await update.message.reply_text(msg)

# ===== NEWS =====
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    arts = requests.get(url).json().get("articles", [])[:5]
    msg = "\n".join(f"{i+1}. {a['title']}" for i, a in enumerate(arts))
    await update.message.reply_text(msg)

# ===== APP =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("news", news))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

PORT = int(os.environ.get("PORT", 10000))

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=BOT_TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
)

print("✅ Pratigya AI Bot is LIVE (Gemini Mode)")
