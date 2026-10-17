import os, asyncio, ccxt, threading
import pandas as pd
import ta
from telegram import Bot
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

class H(BaseHTTPRequestHandler):
   def do_GET(self):
       self.send_response(200)
       self.end_headers()
       self.wfile.write(b"Bot is running")
   def log_message(self, *args):
       pass

def run_web():
   port = int(os.environ.get("PORT", 10000))
   HTTPServer(('0.0.0.0', port), H).serve_forever()

threading.Thread(target=run_web, daemon=True).start()

exchange = ccxt.binance()
bot = Bot(token=TOKEN)
COINS = ["WLD/USDT","FIL/USDT","QNT/USDT","BTC/USDT","ETH/USDT","SOL/USDT","OP/USDT","AVAX/USDT","DOT/USDT","LINK/USDT","BNB/USDT","ARB/USDT"]

def signal(s):
   try:
       b = exchange.fetch_ohlcv(s, '15m', limit=100)
       df = pd.DataFrame(b, columns=['t','o','h','l','c','v'])
       c = df['c']
       rsi = ta.momentum.RSIIndicator(c, 14).rsi().iloc[-1]
       ema = ta.trend.EMAIndicator(c, 20).ema_indicator().iloc[-1]
       p = c.iloc[-1]
       low = df['l'].tail(20).min()
       if rsi < 38 and p <= low * 1.015 and p > ema:
           return f"🟢 {s.replace('/USDT','')} دخول {p:.4f} هدف {p*1.018:.4f} وقف {p*0.99:.4f}"
   except:
       pass

async def main():
   await bot.send_message(chat_id=CHAT_ID, text="✅ البوت اشتغل - هذه آخر مرة نعدل الكود")
   while True:
       for coin in COINS:
           m = signal(coin)
           if m:
               await bot.send_message(chat_id=CHAT_ID, text=m)
           await asyncio.sleep(2)
       await asyncio.sleep(180)

asyncio.run(main())
