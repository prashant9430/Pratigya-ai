import os
import requests
import openai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# ---------------- ENV Variables ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
CONTACT_NUMBER = os.getenv("CONTACT_NUMBER")
PHOTO_URL = os.getenv("PHOTO_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Example: https://yourapp.onrender.com

openai.api_key = OPENAI_API_KEY

# ---------------- /start Command ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Hi, I am Pratigya-AI.🍃\n"
        "Made by PRASHANT PANDEY\n"
        "Insta profile:- _prashant__pandey_"
    )

    keyboard = [
        [InlineKeyboardButton("📞 Contact", callback_data="show_contact")],
        [InlineKeyboardButton("📸 Follow Insta", url="https://www.instagram.com/_prashant__pandey/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=PHOTO_URL,
        caption=message,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ---------------- Button Click Handler ----------------
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show_contact":
        await query.edit_message_caption(
            caption=f"My contact number: {CONTACT_NUMBER}",
            parse_mode="Markdown"
        )

# ---------------- Emotional AI Reply ----------------
def get_emotional_reply(user_msg):
    SYSTEM_PROMPT = """
    You are Pratigya AI, a friendly emotional-intelligent girl.
    - Always respond with empathy and care.
    - Use friendly, informal Hindi/Hinglish.
    - Respect privacy, and maintain positivity.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content']
    except:
        return "Sorry, kuch samajh nahi paayi 😅"

# ---------------- Weather Command ----------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()
    if "main" in data:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Weather in {city}: {temp}°C, {desc}"
    return "City not found!"

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Provide city. Example: /weather Patna")
        return
    city = " ".join(context.args)
    info = get_weather(city)
    await update.message.reply_text(info)

# ---------------- News Command ----------------
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get("articles", [])[:5]
    news_text = ""
    for i, art in enumerate(articles, 1):
        news_text += f"{i}. {art['title']}\n"
    return news_text or "No news found!"

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_text = get_news()
    await update.message.reply_text(news_text)

# ---------------- Chat Message Handler ----------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.strip()
    reply = get_emotional_reply(user_msg)
    await update.message.reply_text(reply)

# ---------------- Bot Setup ----------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("news", news))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))

# ---------------- Webhook for Render ----------------
PORT = int(os.environ.get("PORT", 10000))
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=BOT_TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
)

print("Pratigya AI Telegram Bot (Webhook) is running...")async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show_contact":
        await query.edit_message_caption(caption=f"My contact number: {CONTACT_NUMBER}", parse_mode="Markdown")

# ---------------- Emotional AI Reply ----------------
def get_emotional_reply(user_msg):
    SYSTEM_PROMPT = """
    You are Pratigya AI, a friendly emotional-intelligent girl.
    - Always respond with empathy and care.
    - Use friendly, informal Hindi/Hinglish.
    - Respect privacy, and maintain positivity.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content']
    except:
        return "Sorry, kuch samajh nahi paayi 😅"

# ---------------- Weather Command ----------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()
    if "main" in data:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Weather in {city}: {temp}°C, {desc}"
    return "City not found!"

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Provide city. Example: /weather Patna")
        return
    city = " ".join(context.args)
    info = get_weather(city)
    await update.message.reply_text(info)

# ---------------- News Command ----------------
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get("articles", [])[:5]
    news_text = ""
    for i, art in enumerate(articles, 1):
        news_text += f"{i}. {art['title']}\n"
    return news_text or "No news found!"

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_text = get_news()
    await update.message.reply_text(news_text)

# ---------------- Message Handler ----------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.strip()
    reply = get_emotional_reply(user_msg)
    await update.message.reply_text(reply)

# ---------------- Bot Setup ----------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("news", news))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))

# ---------------- Webhook for Render ----------------
PORT = int(os.environ.get("PORT", 10000))
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=BOT_TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
)

print("Pratigya AI Telegram Bot (Webhook) is running...")        [InlineKeyboardButton("📸 Follow Insta", url="https://www.instagram.com/_prashant__pandey/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(photo=PHOTO_URL, caption=message, parse_mode="Markdown", reply_markup=reply_markup)

# ---------------- Button Click Handler ----------------
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "show_contact":
        await query.edit_message_caption(caption=f"My contact number: {CONTACT_NUMBER}", parse_mode="Markdown")

# ---------------- Emotional AI Reply ----------------
def get_emotional_reply(user_msg):
    SYSTEM_PROMPT = """
    You are Pratigya AI, a friendly emotional-intelligent girl.
    - Always respond with empathy and care.
    - Use friendly, informal Hindi/Hinglish.
    - Respect privacy, and maintain positivity.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content']
    except:
        return "Sorry, kuch samajh nahi paayi 😅"

# ---------------- Weather Command ----------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()
    if "main" in data:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Weather in {city}: {temp}°C, {desc}"
    return "City not found!"

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not user_access.get(user_id, False):
        await update.message.reply_text("🔒 Enter secret key first!")
        return
    if len(context.args) == 0:
        await update.message.reply_text("Provide city. Example: /weather Patna")
        return
    city = " ".join(context.args)
    info = get_weather(city)
    await update.message.reply_text(info)

# ---------------- News Command ----------------
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get("articles", [])[:5]
    news_text = ""
    for i, art in enumerate(articles, 1):
        news_text += f"{i}. {art['title']}\n"
    return news_text or "No news found!"

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not user_access.get(user_id, False):
        await update.message.reply_text("🔒 Enter secret key first!")
        return
    news_text = get_news()
    await update.message.reply_text(news_text)

# ---------------- Secret Key & Name Capture ----------------
async def access_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Already unlocked
    if user_access.get(user_id, False):
        if awaiting_name.get(user_id, False):
            user_name[user_id] = text
            awaiting_name[user_id] = False
            await update.message.reply_text(f"Nice to meet you, {text}! 🌸 You can now chat with me.")
            return
        # Normal chat → AI reply
        reply = get_emotional_reply(text)
        await update.message.reply_text(reply)
        return

    # Secret key check
    if text == SECRET_KEY:
        user_access[user_id] = True
        awaiting_name[user_id] = True
        await update.message.reply_text("✅ Access granted! First, tell me your name. What is your name?")
        return
    else:
        await update.message.reply_text("🔒 Please enter the secret key to use Pratigya AI.")

# ---------------- Bot Setup ----------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("news", news))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), access_check))

# ---------------- Webhook for Render ----------------
PORT = int(os.environ.get("PORT", 10000))
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=BOT_TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
)

print("Pratigya AI Telegram Bot (Webhook) is running...")def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()
    if "main" in data:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Weather in {city}: {temp}°C, {desc}"
    return "City not found!"

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not user_access.get(user_id, False):
        await update.message.reply_text("🔒 Enter secret key first!")
        return
    if len(context.args) == 0:
        await update.message.reply_text("Provide city. Example: /weather Patna")
        return
    city = " ".join(context.args)
    info = get_weather(city)
    await update.message.reply_text(info)

# ---------------- News Command ----------------
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    articles = requests.get(url).json().get("articles", [])[:5]
    news_text = ""
    for i, art in enumerate(articles, 1):
        news_text += f"{i}. {art['title']}\n"
    return news_text or "No news found!"

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not user_access.get(user_id, False):
        await update.message.reply_text("🔒 Enter secret key first!")
        return
    news_text = get_news()
    await update.message.reply_text(news_text)

# ---------------- Secret Key & Name Capture ----------------
async def access_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Already unlocked
    if user_access.get(user_id, False):
        if awaiting_name.get(user_id, False):
            user_name[user_id] = text
            awaiting_name[user_id] = False
            await update.message.reply_text(f"Nice to meet you, {text}! 🌸 You can now chat with me.")
            return
        # Normal chat → AI reply
        reply = get_emotional_reply(text)
        await update.message.reply_text(reply)
        # Save to Google Sheet
        sheet.append_row([user_id, user_name.get(user_id, "Unknown"), text])
        return

    # Secret key check
    if text == SECRET_KEY:
        user_access[user_id] = True
        awaiting_name[user_id] = True
        await update.message.reply_text("✅ Access granted! First, tell me your name. What is your name?")
        return
    else:
        await update.message.reply_text("🔒 Please enter the secret key to use Pratigya AI.")

# ---------------- Bot Setup ----------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("news", news))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), access_check))

# ---------------- Webhook for Render ----------------
PORT = int(os.environ.get("PORT", 10000))
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=BOT_TOKEN,
    webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}"
)

print("Pratigya AI Telegram Bot (Webhook) is running...")
