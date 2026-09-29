import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
   return "Bot is Live!"

async def start(update, context):
   await update.message.reply_text("البوت شغال 100% ✅")

def run_bot():
   application = ApplicationBuilder().token(BOT_TOKEN).build()
   application.add_handler(CommandHandler("start", start))
   # هنا اضف باقي اوامر الدوت
   application.run_polling()

if __name__ == "__main__":
   threading.Thread(target=run_bot, daemon=True).start()
   port = int(os.environ.get("PORT", 10000))
   app_flask.run(host='0.0.0.0', port=port)
