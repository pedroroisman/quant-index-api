
import yfinance as yf
import pandas as pd

def trend_swing_index(symbol: str) -> dict:
    try:
        df = yf.download(symbol, period="3mo", interval="1d")

        if df.empty or "Close" not in df:
            return {
                "ticker": symbol,
                "horizon": "Swing",
                "indice": 0,
                "note": "No data available, returning neutral signal"
            }

        df["EMA_rapida"] = df["Close"].ewm(span=5, adjust=False).mean()
        df["EMA_lenta"] = df["Close"].ewm(span=20, adjust=False).mean()

        last = df.iloc[-1]
        prev = df.iloc[-2]

        if prev["EMA_rapida"] < prev["EMA_lenta"] and last["EMA_rapida"] > last["EMA_lenta"]:
            indice = -1.0
        elif prev["EMA_rapida"] > prev["EMA_lenta"] and last["EMA_rapida"] < last["EMA_lenta"]:
            indice = 1.0
        else:
            diferencia = last["EMA_rapida"] - last["EMA_lenta"]
            rango = df["Close"].max() - df["Close"].min()
            normalizado = round(diferencia / rango, 4)
            indice = max(-1, min(1, -normalizado))

        return {
            "ticker": symbol,
            "horizon": "Swing",
            "indice": round(indice, 4)
        }

    except Exception as e:
        return {
            "ticker": symbol,
            "horizon": "Swing",
            "indice": 0,
            "note": "Error fetching data, defaulted to neutral",
            "detail": str(e)
        }
