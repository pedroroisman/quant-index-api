
import requests
import pandas as pd
from datetime import datetime

API_KEY = "2a0d5658f5204b06bb2d0ce50d9b7b16"

def get_swing_index(symbol):
    try:
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=30&apikey={API_KEY}"
        res = requests.get(url).json()
        values = res.get("values", [])
        if len(values) < 20:
            return None
        df = pd.DataFrame(values)
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["close"] = pd.to_numeric(df["close"])
        df.sort_values("datetime", inplace=True)
        last_price = df["close"].iloc[-1]
        avg = df["close"].iloc[-20:].mean()
        index = round((last_price - avg) / avg, 2)
        return {"index": index, "price": round(last_price, 2), "avg": round(avg, 2)}
    except Exception as e:
        print(f"[SWING] Error con {symbol}: {e}")
        return None
