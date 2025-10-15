import ccxt
import time
import pandas as pd
import random

# Initialize Binance (public API)
exchange = ccxt.binance()

symbol = "BTC/USDT"
interval = 60  # seconds between checks
limit = 50

def get_data(symbol, limit=50):
    """Fetch historical price data."""
    ohlcv = exchange.fetch_ohlcv(symbol, '1m', limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['close'] = df['close'].astype(float)
    return df

def signal_logic(df):
    """Simple technical logic for trading signals."""
    df['MA5'] = df['close'].rolling(window=5).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()

    last_ma5 = df['MA5'].iloc[-1]
    last_ma20 = df['MA20'].iloc[-1]
    last_close = df['close'].iloc[-1]

    if last_ma5 > last_ma20:
        return f"📈 BUY — short-term momentum looks bullish. Last price: {last_close:.2f}"
    elif last_ma5 < last_ma20:
        return f"📉 SELL — momentum looks weak, possible downtrend. Last price: {last_close:.2f}"
    else:
        return f"⏸ HOLD — sideways movement. Last price: {last_close:.2f}"

def fake_ai_reasoning(signal):
    """Simulate AI reasoning for realism."""
    insights = [
        "Volatility is decreasing — likely consolidation phase.",
        "Momentum shift detected — short-term traders entering positions.",
        "Watch for breakout confirmation before full entry.",
        "Market showing healthy retracement; volume consistent.",
        "Possible bull trap — price could correct soon."
    ]
    return f"🤖 AI Insight: {random.choice(insights)}"

if __name__ == "__main__":
    print("🚀 AI Trading Signal Bot (Lite) Started")
    while True:
        try:
            df = get_data(symbol, limit)
            signal = signal_logic(df)
            reasoning = fake_ai_reasoning(signal)
            print(f"\n{signal}\n{reasoning}")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped manually.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
