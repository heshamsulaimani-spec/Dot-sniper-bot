import os
import logging
import requests
import ccxt
import pandas as pd
import ta
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ============ إعداداتك ============
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # حطه في Render اذا مو موجود

COINS = [
    "BTC/USDT","ETH/USDT","OP/USDT","RENDER/USDT","QNT/USDT","AVAX/USDT","SOL/USDT","DOT/USDT","LINK/USDT","BNB/USDT",
    "TAO/USDT","ARB/USDT","SEI/USDT","SUI/USDT","INJ/USDT","NEAR/USDT","FIL/USDT","FET/USDT","ADA/USDT","ZRO/USDT",
    "DYDX/USDT","AEVO/USDT","LTC/USDT"
]

logging.basicConfig(level=logging.INFO)
exchange = ccxt.binance()

def send_log(msg):
    print(msg)

async def check_market(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
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
            
            signal_text = None
            if rsi < 42 and trend == "Bearish" and vol_conf > 1.0:
                signal_text = "🔴 EXIT SIGNAL - Sell your holdings"
            elif rsi < 35 and trend == "Bullish" and vol_conf > 1.2:
                signal_text = "🟢 BUY SIGNAL - Opportunity"

            if signal_text:
                conf = round(50 + vol_conf*8 + abs(last['close']-last['ema20'])/last['close']*200, 1)
                conf = min(conf, 89.9)
                msg = f"""🤖 dot-bot | {symbol}
Signal: {signal_text}
Spot exit warning only — no short selling.
Current price: {last['close']:.4f}
RSI(14): {rsi:.2f} | 15m trend: {trend}
Volume confirmation: {vol_conf:.2f}x 20-candle average
Confidence: {conf}% (EMA distance + volume)
Candle: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC"""
                await context.bot.send_message(chat_id=chat_id, text=msg)
        except Exception as e:
            print(f"Error {symbol}: {e}")
        await context.job_queue.run_once(lambda: None, 1) # راحة ثانية بين العملات

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"فيراري شغالة! 🏎️ أراقب {len(COINS)} عملة كل 15 دقيقة.\nارسل /scan عشان افحص الآن.")
    if not context.chat_data.get('running'):
        context.job_queue.run_repeating(check_market, interval=900, first=5, chat_id=update.effective_chat.id)
        context.chat_data['running'] = True

async def scan_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"جاري فحص {len(COINS)} عملة الآن...")
    await check_market(context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("scan", scan_now))
    app.run_polling()

if __name__ == "__main__":
    main()
