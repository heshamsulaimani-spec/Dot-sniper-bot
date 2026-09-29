from flask import Flask
from threading import Thread
import os
from telegram.ext import Updater, CommandHandler

app = Flask(__name__)

@app.route('/')
def home():
   return "Bot is LIVE ✅"

def run_bot():
   token = os.environ.get("BOT_TOKEN")
   if not token:
       print("No BOT_TOKEN")
       return
   def start(update, context):
       update.message.reply_text("شغال LIVE ✅")
   updater = Updater(token, use_context=True)
   updater.dispatcher.add_handler(CommandHandler("start", start))
   updater.start_polling()

Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
