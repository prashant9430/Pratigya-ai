import os
import requests
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

# ========== OPENAI CLIENT ==========
client = OpenAI(api_key=OPENAI_API_KEY)

# ========== START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Hi, I am *Pratigya-AI* 🍃\n\n"
        "Made by *Prashant Pandey*\n"
        "Insta: @_prashant__pandey_"
    )

    keyboard = [
        [InlineKeyboardButton("📞 Contact", callback_data="show_contact")],
        [InlineKeyboardButton("📸 Follow Insta", url="https://www.instagram.com/_prashant__pandey/")]
    ]

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
