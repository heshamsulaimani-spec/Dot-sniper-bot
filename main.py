from flask import Flask
from threading import Thread
import os
from telegram.ext import Updater, CommandHandler

# --- هذا عشان Render ما يطفي الموقع ---
app = Flask(__name__)
@app.route('/')
def home():
   return "Ferrari Bot is LIVE!"

def run_web():
   port = int(os.environ.get("PORT", 10000))
   app.run(host="0.0.0.0", port=port)

Thread(target=run_web, daemon=True).start()

# --- هذا كود البوت حقك ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")

def start(update, context):
   update.message.reply_text("أهلا! بوت الفيراري شغال LIVE ✅")

def main():
   updater = Updater(BOT_TOKEN, use_context=True)
   dp = updater.dispatcher
   dp.add_handler(CommandHandler("start", start))

   # هنا تقدر تضيف باقي أوامر بوتك القديمة
   # dp.add_handler(...)

   updater.start_polling()
   updater.idle()

if __name__ == "__main__":
   main()
