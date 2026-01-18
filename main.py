import os, json, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
SECRET_KEY = "PRATIGYA-108"
AUTH_FILE = "authorized.json"

def load_auth():
    if not os.path.exists(AUTH_FILE):
        return {}
    return json.load(open(AUTH_FILE))

def save_auth(data):
    json.dump(data, open(AUTH_FILE, "w"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔐 Access ke liye Secret Key bhejiye")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    msg = update.message.text.strip()
    auth = load_auth()

    if user_id not in auth:
        if msg == SECRET_KEY:
            auth[user_id] = True
            save_auth(auth)
            await update.message.reply_text(
                "✅ Access Granted\nMain Pratigya hoon, made by Prashant Pandey."
            )
        else:
            await update.message.reply_text("❌ Galat Secret Key")
        return

    try:
        r = requests.get(f"https://duckduckgo.com/?q={msg}", timeout=5)
        answer = r.text[:700]
    except:
        answer = "Is prashn ka uttar main apni samajh se de rahi hoon."

    await update.message.reply_text(
        f"🧠 Pratigya:\n{answer}\n\n— made by Prashant Pandey"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
