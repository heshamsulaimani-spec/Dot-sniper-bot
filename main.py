import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
   raise ValueError("BOT_TOKEN not set!")

# Flask for Render health check
flask_app = Flask(__name__)
app = flask_app # Render needs 'app'

@flask_app.route('/')
def home():
   return "Bot is Live!"

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
   if not context.args or len(context.args) < 5:
       await update.message.reply_text("استخدم: /buy DOT 4.25 3.9 4.5 4.8")
       return
   symbol = context.args[0]
   await update.message.reply_text(f"تم ✅ {symbol} - جاهز للشراء: {context.args[1:]}")

def run_bot():
   print("Starting bot polling...")
   application = ApplicationBuilder().token(BOT_TOKEN).build()
   application.add_handler(CommandHandler("buy", buy))
   application.run_polling()
   print("Bot stopped")

# Start bot in background thread
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
   flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
