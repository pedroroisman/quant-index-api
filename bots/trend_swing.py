
import requests
import json
from datetime import datetime, timedelta
import os

CACHE_DIR = "cache"
CACHE_DURATION_MINUTES = 20

def load_cache(symbol: str, datatype: str):
    filename = os.path.join(CACHE_DIR, f"{symbol}_{datatype}.json")
    if not os.path.exists(filename):
        return None
    modified_time = datetime.fromtimestamp(os.path.getmtime(filename))
    if datetime.now() - modified_time > timedelta(minutes=CACHE_DURATION_MINUTES):
        return None
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception:
        return None

def save_cache(symbol: str, datatype: str, data: dict):
    os.makedirs(CACHE_DIR, exist_ok=True)
    filename = os.path.join(CACHE_DIR, f"{symbol}_{datatype}.json")
    with open(filename, "w") as f:
        json.dump(data, f)

def get_swing_index(symbol: str, api_key: str):
    cached = load_cache(symbol, "swing")
    if cached:
        print(f"[SWING CACHE] Using cached data for {symbol}")
        return cached

    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=30&apikey={api_key}"
    try:
        res = requests.get(url)
        data = res.json()
        if "values" not in data:
            print(f"[SWING TwelveData Error] {data.get('message', 'Unknown error')} ({symbol})")
            return {"indice": 0, "note": "Swing unavailable", "confidence": "low"}

        prices = [float(item["close"]) for item in data["values"][:20]]
        if len(prices) < 20:
            return {"indice": 0, "note": "Insufficient data", "confidence": "low"}

        promedio = sum(prices) / len(prices)
        actual = float(data["values"][0]["close"])
        diff = actual - promedio
        indice = round(diff / promedio * 5, 2)
        indice = max(min(indice, 1), -1)

        note = f"Price: {actual:.2f}, Avg(20): {promedio:.2f}"
        confidence = "moderate"
        if abs(indice) >= 0.9:
            confidence = "high"
        elif abs(indice) < 0.3:
            confidence = "low"

        result = {
            "indice": indice,
            "note": note,
            "confidence": confidence
        }

        save_cache(symbol, "swing", result)
        return result

    except Exception as e:
        print(f"[SWING Error] {symbol}: {e}")
        return {"indice": 0, "note": "Swing error", "confidence": "low"}
