import os
import requests
import asyncio
from datetime import datetime
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
CONTACT_NUMBER = os.getenv("CONTACT_NUMBER")
PHOTO_URL = os.getenv("PHOTO_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

# ===== MEMORY =====
user_memory = {}
user_names = {}
greeted_today = {}

def remember(user_id, text):
    user_memory.setdefault(user_id, []).append(text)

def last_memory(user_id):
    return "\n".join(user_memory.get(user_id, [])[-5:])

def extract_name(text):
    t = text.lower()
    for key in ["my name is", "i am", "i'm", "mai", "main"]:
        if key in t:
            return t.split(key)[-1].strip().split()[0].capitalize()
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
def ai_reply(user_id, text):
    memory = last_memory(user_id)
    name = user_names.get(user_id, "")

    prompt = f"""
You are Pratigya, a real human-like girl chatting on Telegram.
Talk in soft Hindi/Hinglish like a caring friend.

User name: {name}
Recent chats:
{memory}
"""

    try:
        r = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        )
        return r.output[0].content[0].text.strip()
    except Exception as e:
        print(e)
        return "Thoda sa issue aa gaya… 🙂"

# ===== CHAT =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    today = datetime.now().date()

    # name save
    name = extract_name(text)
    if name:
        user_names[user_id] = name

    # greet once daily
    if greeted_today.get(user_id) != today:
        hour = datetime.now().hour
        greet = "Good Morning ☀️" if hour < 12 else "Good Night 🌙"
        await update.message.reply_text(greet)
        greeted_today[user_id] = today

    remember(user_id, text)

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(2)

    reply = ai_reply(user_id, text)
    remember(user_id, reply)

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

print("✅ Pratigya AI Bot is LIVE")
