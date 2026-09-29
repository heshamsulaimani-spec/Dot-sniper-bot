import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
   return "Bot is Live!"

async def buy(update, context):
   try:
       # /buy DOT 4.25 3.9 4.5 4.8
       args = context.args
       if len(args) < 5:
           await update.message.reply_text("الطريقة: /buy العملة سعر_الدخول ستوب هدف1 هدف2")
           return
       coin, entry, stop, tp1, tp2 = args[0], args[1], args[2], args[3], args[4]
       msg = f"✅ تم تسجيل صفقة {coin}\nدخول: {entry}\nستوب: {stop}\nأهداف: {tp1} - {tp2}\n\nالبوت شغال ويتابعها الآن..."
       await update.message.reply_text(msg)
   except Exception as e:
       await update.message.reply_text(f"خطأ: {e}")

def run_bot():
   app = ApplicationBuilder().token(BOT_TOKEN).build()
   app.add_handler(CommandHandler("buy", buy))
   print("Bot polling started...")
   app.run_polling()

if __name__ == '__main__':
   # شغل البوت في ثريد ثاني
   threading.Thread(target=run_bot, daemon=True).start()
   # شغل Flask عشان Render ما يطفي الخدمة
   port = int(os.environ.get("PORT", 10000))
   app_flask.run(host='0.0.0.0', port=port)
