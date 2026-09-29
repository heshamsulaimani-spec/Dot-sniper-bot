from flask import Flask
from threading import Thread
import os
from telegram.ext import Updater, CommandHandler

app = Flask(__name__)
@app.route('/')
def home():
   return "Dot-sniper-bot is LIVE!"

def run_web():
   port = int(os.environ.get("PORT", 10000))
   app.run(host="0.0.0.0", port=port)

Thread(target=run_web, daemon=True).start()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def start(update, context):
   update.message.reply_text("أبشر! البوت اشتغل وصار LIVE ✅")

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()
