import os
import threading
from flask import Flask
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route('/')
def home():
   return "Bot is Live!"

def start(update, context):
   update.message.reply_text("البوت شغال 100% ✅")

def run_bot():
   updater = Updater(BOT_TOKEN, use_context=True)
   dp = updater.dispatcher
   dp.add_handler(CommandHandler("start", start))
   # هنا حط باقي أوامر توصيات الدوت حقتك
   updater.start_polling()
   updater.idle()

if __name__ == "__main__":
   # شغل البوت في الخلفية
   threading.Thread(target=run_bot).start()
   # شغل الموقع عشان Render يشوفه Live
   port = int(os.environ.get("PORT", 10000))
   app.run(host='0.0.0.0', port=port)
