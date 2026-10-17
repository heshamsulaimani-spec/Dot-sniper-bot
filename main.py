import os, asyncio, ccxt
import pandas as pd
import ta
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# كل عملاتك
COINS = ["WLD/USDT","FIL/USDT","QNT/USDT","DYDX/USDT","AEVO/USDT","BTC/USDT","ETH/USDT","SOL/USDT","OP/USDT","RENDER/USDT","AVAX/USDT","DOT/USDT","LINK/USDT","BNB/USDT","TAO/USDT","ARB/USDT","SEI/USDT","SUI/USDT","INJ/USDT","NEAR/USDT","FET/USDT","ADA/USDT","ZRO/USDT","LTC/USDT"]

exchange = ccxt.binance()
bot = Bot(token=TOKEN)

def scalp_signal(symbol):
   try:
       bars = exchange.fetch_ohlcv(symbol, '15m', limit=100)
       df = pd.DataFrame(bars, columns=['t','o','h','l','c','v'])
       close = df['c']

       rsi = ta.momentum.RSIIndicator(close, 14).rsi().iloc[-1]
       ema20 = ta.trend.EMAIndicator(close, 20).ema_indicator().iloc[-1]
       price = close.iloc[-1]
       vol = df['v'].iloc[-1]
       vol_avg = df['v'].rolling(20).mean().iloc[-1]

       low_20 = df['l'].tail(20).min()

       # شرط اضرب واهرب: RSI نازل + قريب من دعم + فوليوم عالي
       is_near_support = price <= low_20 * 1.01  # قريب 1% من قاع 20 شمعة
       vol_ok = vol > vol_avg * 1.1

       if rsi < 38 and is_near_support and vol_ok and price > ema20:
           entry = price
           target = entry * 1.018  # هدف 1.8%
           stop = entry * 0.99     # وقف 1%
           return f"🟢 سكالب {symbol.replace('/USDT','')} \nدخول: {entry:.4f}\nهدف: {target:.4f} (+1.8%)\nوقف: {stop:.4f} (-1%)\nRSI: {rsi:.1f} - اضرب واهرب!"

       if rsi > 65 and price < ema20:
           return f"🔴 خروج {symbol.replace('/USDT','')} | السعر {price:.4f} | RSI {rsi:.1f}"

   except Exception as e:
       print(f"{symbol} error {e}")
   return None

async def loop():
   await bot.send_message(chat_id=CHAT_ID, text=f"✅ بوت اضرب واهرب اشتغل!\nيراقب {len(COINS)} عملة\nWLD, FIL, QNT, DYDX...")
   while True:
       for coin in COINS:
           msg = scalp_signal(coin)
           if msg:
               await bot.send_message(chat_id=CHAT_ID, text=msg)
               await asyncio.sleep(2)
           await asyncio.sleep(2)
       await asyncio.sleep(180) # يفحص كل 3 دقايق

if __name__ == "__main__":
   asyncio.run(loop())
    
