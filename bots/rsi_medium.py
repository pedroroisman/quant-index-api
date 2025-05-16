
import requests

TICKERS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA']
API_KEY = "2a0d5658f5204b06bb2d0ce50d9b7b16"

def get_rsi(symbol, interval="1day", time_period=14):
    try:
        url = f"https://api.twelvedata.com/rsi?symbol={symbol}&interval={interval}&time_period={time_period}&apikey={API_KEY}"
        res = requests.get(url).json()
        rsi_value = res.get("values", [])[0].get("rsi") if res.get("values") else None
        return float(rsi_value) if rsi_value else None
    except Exception as e:
        print(f"[RSI] Error con {symbol}: {e}")
        return None

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        price = res.get("price")
        return float(price) if price else None
    except Exception as e:
        print(f"[PRICE] Error con {symbol}: {e}")
        return None

def get_rsi_index(symbol):
    rsi = get_rsi(symbol)
    if rsi is None:
        return 0, "RSI unavailable"
    if rsi < 30:
        return -1.0, f"RSI: {rsi:.2f} → Oversold"
    elif rsi > 70:
        return 1.0, f"RSI: {rsi:.2f} → Overbought"
    else:
        index = (rsi - 50) / 20
        index = max(-1, min(1, round(index, 2)))
        label = "Neutral range"
        return index, f"RSI: {rsi:.2f} → {label}"
