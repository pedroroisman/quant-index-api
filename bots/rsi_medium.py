
import requests
import time

TICKERS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA']
API_KEY = "6I2S3R4VPPES4U0O"  # Reemplazar por tu clave real

def get_rsi(symbol, interval="daily", time_period=14):
    try:
        url = f"https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval={interval}&time_period={time_period}&series_type=close&apikey={API_KEY}"
        res = requests.get(url).json()
        key = f"Technical Analysis: RSI"
        rsi_series = res.get(key, {})
        if not rsi_series:
            return None
        latest_rsi = list(rsi_series.values())[0]
        time.sleep(12)  # Para evitar rate-limit por minuto
        return float(latest_rsi["RSI"])
    except Exception as e:
        print(f"[RSI Alpha] Error con {symbol}: {e}")
        return None

def get_price(symbol):
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        res = requests.get(url).json()
        price = res.get("Global Quote", {}).get("05. price", None)
        time.sleep(12)
        return float(price) if price else None
    except Exception as e:
        print(f"[PRICE Alpha] Error con {symbol}: {e}")
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
