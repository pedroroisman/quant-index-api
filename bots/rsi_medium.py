
import requests
import time

TICKERS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA']
API_KEY = "2a0d5658f5204b06bb2d0ce50d9b7b16"

def get_rsi(symbol, interval="1day", time_period=14):
    try:
        url = f"https://api.twelvedata.com/rsi?symbol={symbol}&interval={interval}&time_period={time_period}&apikey={API_KEY}"
        res = requests.get(url).json()
        if "status" in res and res["status"] == "error":
            print(f"[RSI TwelveData Error] {res.get('message', 'Unknown error')} ({symbol})")
            return None
        values = res.get("values", [])
        if not values:
            return None
        return float(values[0]["rsi"])
    except Exception as e:
        print(f"[RSI] Error con {symbol}: {e}")
        return None

def get_price(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        if "status" in res and res["status"] == "error":
            print(f"[PRICE TwelveData Error] {res.get('message', 'Unknown error')} ({symbol})")
            return None
        return float(res["price"])
    except Exception as e:
        print(f"[PRICE] Error con {symbol}: {e}")
        return None

def get_rsi_index(symbol):
    rsi = get_rsi(symbol)
    if rsi is None:
        return 0, "RSI unavailable", "low"

    if rsi < 35:
        index = round((rsi - 50) / 15, 1)
    elif rsi > 65:
        index = round((rsi - 50) / 15, 1)
    else:
        index = 0

    index = max(-1, min(1, index))
    label = (
        "Overbought" if index == 1 else
        "Oversold" if index == -1 else
        "Neutral range"
    )
    confidence = "high" if abs(index) == 1 else "moderate" if index != 0 else "low"
    return index, f"RSI: {rsi:.2f} → {label}", confidence
