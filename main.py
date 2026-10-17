import os
import time
import requests
import ccxt
import pandas as pd
import ta
from datetime import datetime

# ياخذها من Render تلقائي
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# الـ 23 عملة كلها
COINS = [
   "BTC/USDT","ETH/USDT","OP/USDT","RENDER/USDT","QNT/USDT","AVAX/USDT","SOL/USDT","DOT/USDT","LINK/USDT","BNB/USDT",
   "TAO/USDT","ARB/USDT","SEI/USDT","SUI/USDT","INJ/USDT","NEAR/USDT","FIL/USDT","FET/USDT","ADA/USDT","ZRO/USDT",
   "DYDX/USDT","AEVO/USDT","LTC/USDT"
]

exchange = ccxt.binance()

def send_telegram(text):
   url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
   try:
       requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
   except Exception as e:
       print(f"telegram error: {e}")

def check_all():
   for symbol in COINS:
       try:
           bars = exchange.fetch_ohlcv(symbol, '15m', limit=100)
           df = pd.DataFrame(bars, columns=['time','open','high','low','close','volume'])
           df['rsi'] = ta.momentum.RSIIndicator(df['close'], 14).rsi()
           df['ema20'] = ta.trend.EMAIndicator(df['close'], 20).ema_indicator()
           df['vol_avg'] = df['volume'].rolling(20).mean()
           last = df.iloc[-1]

           rsi = last['rsi']
           trend = "Bearish" if last['close'] < last['ema20'] else "Bullish"
           vol_conf = last['volume'] / last['vol_avg'] if last['vol_avg'] > 0 else 1

           signal = None
           if rsi < 40 and trend == "Bearish" and vol_conf > 1.0:
               signal = "🔴 EXIT SIGNAL - Sell your holdings"
           elif rsi < 35 and trend == "Bullish" and vol_conf > 1.2:
               signal = "🟢 BUY SIGNAL - Opportunity"

           if signal:
               conf = round(50 + abs(last['close']-last['ema20'])/last['close']*500 + vol_conf*5, 1)
               msg = f"""🤖 dot-bot | {symbol}
Signal: {signal}
Current price: {last['close']:.4f}
RSI(14): {rsi:.2f} | 15m trend: {trend}
Volume confirmation: {vol_conf:.2f}x 20-candle average
Confidence: {conf}%
Candle: {datetime.utcfromtimestamp(last['time']/1000)} UTC"""
               send_telegram(msg)
               print(f"sent {symbol}")
       except Exception as e:
           print(f"error {symbol}: {e}")
       time.sleep(1)

if __name__ == "__main__":
   send_telegram(f"البوت اشتغل ✅ - أراقب الآن {len(COINS)} عملة كل 15 دقيقة")
   while True:
       check_all()
       time.sleep(900)
