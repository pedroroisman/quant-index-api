
import requests
import pandas as pd
import time

API_KEY = "6I2S3R4VPPES4U0O"  # Reemplazar por tu clave real

def get_swing_index(symbol, multiplicador=5):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
        res = requests.get(url).json()
        series = res.get("Time Series (Daily)", {})
        if not series or len(series) < 20:
            return None
        df = pd.DataFrame(series).T
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df["close"] = pd.to_numeric(df["4. close"])

        precio_actual = df["close"].iloc[-3:].mean()
        promedio = df["close"].iloc[-20:].mean()
        diff = precio_actual - promedio
        index = round(max(min(diff / promedio * multiplicador, 1), -1), 1)

        note = f"Price: {round(precio_actual, 2)}, Avg(20): {round(promedio, 2)}"
        confidence = "high" if abs(index) == 1 else "moderate"

        time.sleep(12)
        return {
            "index": index,
            "price": round(precio_actual, 2),
            "avg": round(promedio, 2),
            "note": note,
            "confidence": confidence
        }

    except Exception as e:
        print(f"[SWING Alpha] Error con {symbol}: {e}")
        return None
