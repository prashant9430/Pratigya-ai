from telegram.ext import Updater, MessageHandler, Filters
import os
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Telegram Bot Token
SECRET_KEY = os.environ.get("SECRET_KEY")  # Secret Key

def reply(update, context):
    text = update.message.text

    # Secret key check
    if not text.startswith(SECRET_KEY):
        update.message.reply_text("❌ Access Denied. Secret key required.")
        return

    question = text.replace(SECRET_KEY, "").strip()

    if not question:
        update.message.reply_text("❓ Question likhiye secret key ke baad")
        return

    # Simple online research (DuckDuckGo API – free)
    url = "https://api.duckduckgo.com/"
    params = {
        "q": question,
        "format": "json"
    }

    r = requests.get(url, params=params).json()

    answer = r.get("AbstractText")

    if answer:
        update.message.reply_text(answer)
    else:
        update.message.reply_text("🤖 Is prashn ka exact answer nahi mila.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
