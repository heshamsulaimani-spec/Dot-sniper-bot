import os, requests, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

app_flask = Flask(__name__)
@app_flask.route('/')
def home():
   return "Bot is Alive!"

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
   try:
       args = context.args
       if len(args) < 5:
           await update.message.reply_text("الصيغة: /buy DOT 4.25 3.9 4.5 4.8 5.2")
           return

       coin = args[0].upper()
       entry, sl, t1, t2 = args[1], args[2], args[3], args[4]
       t3 = args[5] if len(args)>5 else ""

       btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
       btc_price = float(btc.json()['price'])

       msg = f"🚀 {coin}\nدخول: {entry}\nوقف: {sl}\nاهداف: {t1} - {t2} {t3}\nبيتكوين: {btc_price}$"

       if btc_price < 60000:
           msg += "\n⚠️ بيتكوين في خطر - انتبه"

       await update.message.reply_text(msg)
   except Exception as e:
       await update.message.reply_text(f"خطأ: {e}")

def run_flask():
   port = int(os.environ.get("PORT", 10000))
   app_flask.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
   threading.Thread(target=run_flask, daemon=True).start()
   app = ApplicationBuilder().token(BOT_TOKEN).build()
   app.add_handler(CommandHandler("buy", buy))
   print("Bot started...")
   app.run_polling()
