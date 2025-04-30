
import requests
import pandas as pd

def trend_swing_index(symbol: str, api_key: str) -> dict:
    try:
        url = (
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED"
            f"&symbol={symbol}&outputsize=compact&apikey={api_key}"
        )
        response = requests.get(url)
        data = response.json()

        df = pd.DataFrame(data["Time Series (Daily)"]).T
        df = df.astype(float)
        df = df.sort_index()

        df["EMA_rapida"] = df["4. close"].ewm(span=5, adjust=False).mean()
        df["EMA_lenta"] = df["4. close"].ewm(span=20, adjust=False).mean()

        last = df.iloc[-1]
        prev = df.iloc[-2]

        if prev["EMA_rapida"] < prev["EMA_lenta"] and last["EMA_rapida"] > last["EMA_lenta"]:
            indice = -1.0
        elif prev["EMA_rapida"] > prev["EMA_lenta"] and last["EMA_rapida"] < last["EMA_lenta"]:
            indice = 1.0
        else:
            diferencia = last["EMA_rapida"] - last["EMA_lenta"]
            rango = df["4. close"].max() - df["4. close"].min()
            normalizado = round(diferencia / rango, 4)
            indice = max(-1, min(1, -normalizado))

        return {
            "ticker": symbol,
            "horizon": "Swing",
            "indice": round(indice, 4)
        }

    except Exception as e:
        return {"error": str(e)}
