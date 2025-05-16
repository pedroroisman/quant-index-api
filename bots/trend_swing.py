
import requests
import pandas as pd

API_KEY = "2a0d5658f5204b06bb2d0ce50d9b7b16"

def get_swing_index(symbol, suavizar=True, multiplicador=5):
    try:
        url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=30&apikey={API_KEY}"
        res = requests.get(url).json()
        values = res.get("values", [])
        if len(values) < 21:
            return None

        df = pd.DataFrame(values)
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["close"] = pd.to_numeric(df["close"])
        df.sort_values("datetime", inplace=True)

        if suavizar:
            precio_actual = df["close"].iloc[-3:].mean()
        else:
            precio_actual = df["close"].iloc[-1]

        promedio = df["close"].iloc[-20:].mean()
        diff = precio_actual - promedio
        index = round(max(min(diff / promedio * multiplicador, 1), -1), 1)

        note = f"Price: {round(precio_actual, 2)}, Avg(20): {round(promedio, 2)}"
        confidence = "high" if abs(index) == 1 else "moderate"

        return {
            "index": index,
            "price": round(precio_actual, 2),
            "avg": round(promedio, 2),
            "note": note,
            "confidence": confidence
        }

    except Exception as e:
        print(f"[SWING] Error con {symbol}: {e}")
        return None
