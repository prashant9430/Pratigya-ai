import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
from openai import OpenAI

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "तुम Pratigya AI हो, जिसे Prashant Pandey ने बनाया है। सरल हिन्दी में उत्तर दो।"
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    await update.message.reply_text(
        response.choices[0].message.content
    )

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    await app.initialize()
    await app.start()
    await app.bot.set_webhook("https://pratigya-ai.onrender.com")
    await app.stop()  # Render webhook ke liye required
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
