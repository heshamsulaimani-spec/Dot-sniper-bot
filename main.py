from flask import Flask
from threading import Thread
import os
from telegram.ext import Updater, CommandHandler

# موقع عشان Render يبقى أخضر
app = Flask(__name__)
@app.route('/')
def home():
   return "Dot-sniper-bot is LIVE! ✅"

def run_web():
   port = int(os.environ.get("PORT", 10000))
   app.run(host="0.0.0.0", port=port)

def run_bot():
   token = os.environ.get("BOT_TOKEN")
   if not token:
       print("No BOT_TOKEN found")
       return
   def start(update, context):
       update.message.reply_text("أبشر! البوت شغال LIVE ✅")
   updater = Updater(token, use_context=True)
   updater.dispatcher.add_handler(CommandHandler("start", start))
   updater.start_polling()
   updater.idle()

Thread(target=run_web, daemon=True).start()
Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
   run_web()
