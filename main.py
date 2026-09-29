import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

BOT_TOKEN = os.getenv("BOT_TOKEN")
flask_app = Flask(__name__)
app = flask_app

@flask_app.route('/')
def home():
   return "Bot is Live!"

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await update.message.reply_text(f"تم ✅ الامر: {context.args}")

def run_bot():
   print("Starting bot polling...")
   application = ApplicationBuilder().token(BOT_TOKEN).build()
   application.add_handler(CommandHandler("buy", buy))
   application.run_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
   flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
