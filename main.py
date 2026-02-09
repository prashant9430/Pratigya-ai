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

# ========== ENV ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
CONTACT_NUMBER = os.getenv("CONTACT_NUMBER")
PHOTO_URL = os.getenv("PHOTO_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

# ========== MEMORY SYSTEM ==========
user_memory = {}
user_names = {}
greeted_today = {}

def remember_user(user_id, text):
    if user_id not in user_memory:
        user_memory[user_id] = []
    user_memory[user_id].append(text)

def get_memory(user_id):
    return "\n".join(user_memory.get(user_id, [])[-6:])

def extract_name(text):
    text_low = text.lower()
    triggers = ["i am", "i'm", "my name is", "mai", "main"]
    for t in triggers:
        if t in text_low:
            name = text_low.split(t)[-1].strip().split()[0]
            return name.capitalize()
    return None

def smart_emoji(text):
    t = text.lower()
    if any(w in t for w in ["sad", "alone", "cry", "upset"]):
        return "😔"
    if any(w in t for w in ["happy", "great", "love", "awesome"]):
        return "😊"
    if any(w in t for w in ["angry", "mad"]):
        return "🙂"
    return ""

# ========== START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📞 Contact", callback_data="show_contact")],
        [InlineKeyboardButton("📸 Follow Insta", url="https://www.instagram.com/_prashant__pandey/")]
    ]

    message = "Hi, I am *Pratigya-AI* 🍃\nA Human-like AI Friend."

    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption=message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========== BUTTON ==========
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_caption(caption=f"📞 Contact: {CONTACT_NUMBER}")

# ========== AI REPLY ==========
def get_emotional_reply(user_id, text):
    memory_text = get_memory(user_id)
    name = user_names.get(user_id, "")
    emoji = smart_emoji(text)

    system_prompt = f"""
You are Pratigya, a real human-like girl chatting on Telegram.

Do NOT sound like an AI.
Talk in soft Hindi/Hinglish like a caring friend.

User name: {name}

Recent chats:
{memory_text}

Use natural emotions and friendly tone.
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )

        reply = response.output[0].content[0].text.strip()
        return reply + " " + emoji

    except Exception as e:
        print("OpenAI Error:", e)
        return "Thoda sa issue aa gaya… ek sec 🙂"

# ========== CHAT ==========
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text
    today = datetime.now().date()

    # Name detect
    name = extract_name(user_text)
    if name:
        user_names[user_id] = name

    # Daily greeting
    if user_id not in greeted_today or greeted_today[user_id] != today:
        hour = datetime.now().hour
        if hour < 12:
            await update.message.reply_text("Good Morning ☀️")
        elif hour > 21:
            await update.message.reply_text("Good Night 🌙")
        greeted_today[user_id] = today

    remember_user(user_id, user_text)

    # Typing effect
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(2)

    reply = get_emotional_reply(user_id, user_text)
    remember_user(user_id, reply)

    await update.message.reply_text(reply)

# ========== WEATHER ==========
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()
    if "main" in data:
        return f"{city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
    return "City not found ❌"

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args)
    await update.message.reply_text(get_weather(city))

# ========== NEWS ==========
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get("articles", [])[:5]
    return "\n".join(f"{i+1}. {a['title']}" for i, a in enumerate(articles))

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_news())

# ========== APP ==========
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
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

print("✅ Pratigya AI Bot is LIVE (Ultra Human Mode)")
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========== BUTTON ==========
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_contact":
        await query.edit_message_caption(
            caption=f"📞 Contact: {CONTACT_NUMBER}"
        )

# ========== AI REPLY (FIXED) ==========
def get_emotional_reply(text):
    system_prompt = (
        "You are Pratigya AI, a sweet emotional intelligent girl. "
        "You talk in soft Hindi/Hinglish. "
        "You reply warmly, politely and emotionally like a real human."
    )

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )
        return response.output_text

    except Exception as e:
        print("OpenAI Error:", e)
        return "😅 Thodi dikkat aa rahi hai, thodi der baad try karo"

# ========== CHAT ==========
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = get_emotional_reply(user_text)
    await update.message.reply_text(reply)

# ========== WEATHER ==========
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()
    if "main" in data:
        return f"{city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
    return "City not found ❌"

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /weather Patna")
        return
    city = " ".join(context.args)
    await update.message.reply_text(get_weather(city))

# ========== NEWS ==========
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get("articles", [])[:5]
    return "\n".join(f"{i+1}. {a['title']}" for i, a in enumerate(articles))

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_news())

# ========== APP ==========
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
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
