import os
import logging
import requests
import numpy as np
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ================= إعدادات الفيراري =================
TOKEN = os.getenv("BOT_TOKEN")

# هنا تقدر توصلها 100 عملة بضغطة زر - بس زيد الاسم!
COINS = [
   "BTC","ETH","OP","RENDER","QNT","AVAX","SOL","DOT","LINK","BNB",
   "TAO","ARB","SEI","SUI","INJ","NEAR","FIL","FET","ADA","ZRO",
   "DYDX","AEVO","LTC"
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_rsi(prices, period=14):
   try:
       deltas = np.diff(prices)
       gain = (deltas[deltas>0]).sum()/period
       loss = (-deltas[deltas<0]).sum()/period
       if loss == 0: return 70
       rs = gain/loss
       return 100 - (100/(1+rs))
   except: return 50

def analyze_coin(symbol):
   try:
       # سحب شموع 1 ساعة مجانا من بينانس
       url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1h&limit=100"
       data = requests.get(url, timeout=10).json()
       closes = [float(x[4]) for x in data]
       volumes = [float(x[5]) for x in data]

       price = closes[-1]
       rsi = get_rsi(np.array(closes))
       vol_avg = np.mean(volumes[-20:])
       vol_now = volumes[-1]

       score = 0
       reason = ""

       # منطق الفيراري: RSI + سيولة + ترند
       if rsi < 35 and vol_now > vol_avg*1.3:
           score = 90
           reason = f"RSI منخفض {rsi:.1f} + دخول سيولة قوي"
       elif rsi < 45 and closes[-1] > np.mean(closes[-20:]):
           score = 75
           reason = f"ارتداد من تشبع بيعي RSI {rsi:.1f}"
       elif rsi > 70:
           score = 10
           reason = f"متضخم RSI {rsi:.1f} - لا تدخل"

       return {"symbol":symbol, "price":price, "rsi":rsi, "score":score, "reason":reason}
   except Exception as e:
       return None

async def scan_market(context: ContextTypes.DEFAULT_TYPE):
   chat_id = context.job.chat_id
   opportunities = []

   for coin in COINS:
       res = analyze_coin(coin)
       if res and res['score'] >= 70:
           opportunities.append(res)

   if not opportunities:
       return # لا يزعجك اذا مافي فرص قوية

   msg = f"🔥 **فيراري لقت {len(opportunities)} فرص الآن - فحص {len(COINS)} عملة** 🔥\n\n"
   for opp in sorted(opportunities, key=lambda x: x['score'], reverse=True)[:5]:
       msg += f"🟢 **{opp['symbol']}** @ ${opp['price']:.3f}\n"
       msg += f" قوة: {opp['score']}% | {opp['reason']}\n"
       msg += f" وقف مقترح: {opp['price']*0.96:.3f}\n\n"

   await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await update.message.reply_text(
       f"فيراري جاهزة! 🏎️💨\nأراقب لك {len(COINS)} عملة كل 5 دقايق.\nتبغى أبدأ المسح الآن؟ أرسل /scan"
   )
   # شغل المسح التلقائي كل 5 دقايق
   if not context.chat_data.get('running'):
       context.job_queue.run_repeating(scan_market, interval=300, first=10, chat_id=update.effective_chat.id)
       context.chat_data['running'] = True
       await update.message.reply_text("✅ تم تشغيل المسح التلقائي كل 5 دقائق.")

async def scan_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await update.message.reply_text(f"جاري مسح {len(COINS)} عملة...")
   context.job_queue.run_once(scan_market, when=1, chat_id=update.effective_chat.id)

def main():
   app = Application.builder().token(TOKEN).job_queue(None).build()
   # هذا السطر هو اللي يصلح الخطأ الأحمر اللي صورته
   app.add_handler(CommandHandler("start", start))
   app.add_handler(CommandHandler("scan", scan_now))
   app.run_polling(stop_signals=None, close_loop=False)

if __name__ == "__main__":
   main()
