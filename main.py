import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
   return "Bot is Live and Running!"

async def start(update, context):
   await update.message.reply_text("البوت شغال 100% ✅ قول /buy")

def run_flask():
   port = int(os.environ.get("PORT", 10000))
   flask_app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
   # شغل موقع Flask في الخلفية
   threading.Thread(target=run_flask, daemon=True).start()

   # شغل البوت في الواجهة الرئيسية
   app = ApplicationBuilder().token(BOT_TOKEN).build()
   app.add_handler(CommandHandler("start", start))
   print("Bot started polling...")
   app.run_polling()
