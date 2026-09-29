import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
   return "Bot is Alive!"

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
   if len(context.args) < 5:
       await update.message.reply_text("الصيغة: /buy DOT 4.25 3.9 4.5 4.8 5.2")
       return
   try:
       coin = context.args[0].upper()
       entry, sl, t1, t2 = context.args[1], context.args[2], context.args[3], context.args[4]
       t3 = context.args[5] if len(context.args) > 5 else ""

       r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=10)
       btc_price = float(r.json()['price'])

       msg = f"🚀 {coin}\nدخول: {entry}\nوقف: {sl}\nاهداف: {t1} - {t2} {t3}\nBTC: {btc_price}$"
       if btc_price < 60000:
           msg += "\n⚠️ بيتكوين خطر"
       await update.message.reply_text(msg)
   except Exception as e:
       await update.message.reply_text(f"خطأ: {e}")

def run_flask():
   port = int(os.environ.get("PORT", 10000))
   flask_app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
   threading.Thread(target=run_flask, daemon=True).start()
   app = ApplicationBuilder().token(BOT_TOKEN).build()
   app.add_handler(CommandHandler("buy", buy))
   app.run_polling()
