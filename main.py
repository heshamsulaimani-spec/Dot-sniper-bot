import os
import logging
import requests
import numpy as np
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
COINS = ["BTC","ETH","OP","RENDER","QNT","AVAX","SOL","DOT","LINK","BNB","TAO","ARB","SEI","SUI","INJ","NEAR","FIL","FET","ADA","ZRO","DYDX","AEVO","LTC"]

logging.basicConfig(level=logging.INFO)

def get_rsi(prices):
   try:
       deltas = np.diff(prices)
       gain = deltas[deltas>0].sum()/14
       loss = -deltas[deltas<0].sum()/14
       if loss == 0: return 70
       return 100 - (100/(1+gain/loss))
   except: return 50

def analyze_coin(symbol):
   try:
       url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1h&limit=100"
       data = requests.get(url, timeout=10).json()
       closes = [float(x[4]) for x in data]
       volumes = [float(x[5]) for x in data]
       price = closes[-1]
       rsi = get_rsi(np.array(closes))
       vol_avg = np.mean(volumes[-20:])
       score = 0
       reason = ""
       if rsi < 35 and volumes[-1] > vol_avg*1.3:
           score = 90
           reason = f"RSI {rsi:.1f} + سيولة"
       elif rsi < 45 and closes[-1] > np.mean(closes[-20:]):
           score = 75
           reason = f"ارتداد RSI {rsi:.1f}"
       return {"symbol":symbol, "price":price, "score":score, "reason":reason}
   except: return None

async def scan_market(context):
   opportunities = []
   for coin in COINS:
       res = analyze_coin(coin)
       if res and res['score'] >= 70:
           opportunities.append(res)
   if not opportunities: return
   msg = f"🔥 فيراري لقت {len(opportunities)} فرص من {len(COINS)} عملة 🔥\n\n"
   for opp in sorted(opportunities, key=lambda x: x['score'], reverse=True)[:5]:
       msg += f"🟢 {opp['symbol']} @ ${opp['price']:.3f} - قوة {opp['score']}% ({opp['reason']})\n\n"
   await context.bot.send_message(chat_id=context.job.chat_id, text=msg)

async def start(update, context):
   await update.message.reply_text(f"فيراري جاهزة! أراقب {len(COINS)} عملة. /scan للمسح الآن")
   if not context.chat_data.get('running'):
       context.job_queue.run_repeating(scan_market, interval=300, first=10, chat_id=update.effective_chat.id)
       context.chat_data['running'] = True

async def scan_now(update, context):
   await update.message.reply_text(f"جاري مسح {len(COINS)} عملة...")
   context.job_queue.run_once(scan_market, when=1, chat_id=update.effective_chat.id)

def main():
   app = Application.builder().token(TOKEN).build()
   app.add_handler(CommandHandler("start", start))
   app.add_handler(CommandHandler("scan", scan_now))
   # هذا السطر هو اللي يصلح الخطأ الأحمر حقك بدون ما نطفي البوت
   app.run_polling(stop_signals=None, close_loop=False)

if __name__ == "__main__":
   main()
