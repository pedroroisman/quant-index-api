
import yfinance as yf
import pandas as pd

def rsi_medium_index(symbol: str) -> dict:
    try:
        df = yf.download(symbol, period="6mo", interval="1d")

        if df.empty or "Close" not in df:
            return {
                "ticker": symbol,
                "horizon": "Medium-Term",
                "indice": 0,
                "note": "No data available, returning neutral signal"
            }

        # Calcular RSI de 14 días
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        rsi_actual = rsi.iloc[-1]

        # Convertir RSI a índice de -1 a 1
        if rsi_actual < 30:
            indice = -1.0
        elif rsi_actual > 70:
            indice = 1.0
        else:
            indice = (rsi_actual - 50) / 20  # RSI de 50 da 0, 60 da 0.5, 40 da -0.5, etc.
            indice = max(-1, min(1, round(indice, 4)))

        return {
            "ticker": symbol,
            "horizon": "Medium-Term",
            "indice": indice
        }

    except Exception as e:
        return {
            "ticker": symbol,
            "horizon": "Medium-Term",
            "indice": 0,
            "note": "Error fetching data, defaulted to neutral",
            "detail": str(e)
        }
