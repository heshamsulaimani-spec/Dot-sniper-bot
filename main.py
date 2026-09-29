import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
   raise ValueError("BOT_TOKEN not set!")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
   return "Bot is Live!"

async def buy(update, context):
   if not context.args or len(context.args) < 5:
       await update.message.reply_text("الاستخدام: /buy DOT 4.25 3.9 4.5 4.8")
       return
   coin = context.args[0]
   await update.message.reply_text(f"✅ تم استلام صفقة {coin} - البوت يتابعها الآن!")

def run_bot():
   print("Starting bot polling...")
   app = ApplicationBuilder().token(BOT_TOKEN).build()
   app.add_handler(CommandHandler("buy", buy))
   app.run_polling()

if __name__ == '__main__':
   threading.Thread(target=run_bot, daemon=True).start()
   port = int(os.environ.get("PORT", 10000))
   flask_app.run(host='0.0.0.0', port=port)
