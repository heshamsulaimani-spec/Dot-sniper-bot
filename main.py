import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

@app.route('/')
def home():
   return "Bot is running - Live OK!"

async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
   try:
       args = context.args
       if len(args) < 5:
           await update.message.reply_text("الصيغة: /buy DOT 4.25 3.9 4.5 4.8")
           return
       coin = args[0].upper()
       entry, sl, tp1, tp2 = args[1], args[2], args[3], args[4]
       msg = f"✅ تم تفعيل الصفقة\n🪙 {coin}\n📥 دخول: {entry}\n🛑 وقف: {sl}\n🎯 هدف1: {tp1}\n🎯 هدف2: {tp2}\n\nالبوت يراقب الآن..."
       await update.message.reply_text(msg)
   except Exception as e:
       print(f"Error: {e}")
       await update.message.reply_text(f"خطأ: {e}")

def run_bot():
   print("Starting polling...")
   # هذا السطر هو الحل - job_queue(None)
   application = ApplicationBuilder().token(BOT_TOKEN).job_queue(None).build()
   application.add_handler(CommandHandler("buy", buy_command))
   application.run_polling()

threading.Thread(target=run_bot, daemon=True).start()
