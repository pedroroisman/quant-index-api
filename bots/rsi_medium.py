
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

def get_rsi_index(symbol: str, api_key: str):
    cached = load_cache(symbol, "rsi")
    if cached:
        print(f"[RSI CACHE] Using cached data for {symbol}")
        return cached

    url = f"https://api.twelvedata.com/rsi?symbol={symbol}&interval=1day&apikey={api_key}&outputsize=100"
    try:
        res = requests.get(url)
        data = res.json()
        if "values" not in data:
            print(f"[RSI TwelveData Error] {data.get('message', 'Unknown error')} ({symbol})")
            return {"indice": 0, "note": "RSI unavailable", "confidence": "low"}

        rsi_value = float(data["values"][0]["rsi"])
        note = f"RSI: {rsi_value:.2f}"
        confidence = "low"
        indice = 0

        if rsi_value < 35:
            indice = round((35 - rsi_value) / 35, 2)
            note += " → Oversold"
            confidence = "moderate" if indice < 0.7 else "high"
        elif rsi_value > 65:
            indice = round((rsi_value - 65) / 35, 2)
            note += " → Overbought"
            confidence = "moderate" if indice < 0.7 else "high"
        else:
            note += " → Neutral range"

        result = {
            "indice": min(indice, 1),
            "note": note,
            "confidence": confidence
        }

        save_cache(symbol, "rsi", result)
        return result

    except Exception as e:
        print(f"[RSI Error] {symbol}: {e}")
        return {"indice": 0, "note": "RSI error", "confidence": "low"}
