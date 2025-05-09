import requests

API_KEY = "d0f2kn9r01qsv9eev9p0d0f2kn9r01qsv9eev9pg"
TICKERS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA']

def get_swing_index(ticker: str):
    try:
        url = f"https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=D&count=20&token={API_KEY}"
        res = requests.get(url).json()

        if res.get("s") != "ok":
            return None

        closes = res["c"]
        avg = sum(closes) / len(closes)
        price = closes[-1]
        index = round((price - avg) / avg, 2)

        return {"index": index, "price": price, "avg": round(avg, 2)}
    except Exception as e:
        print(f"[Swing] Error con {ticker}: {e}")
        return None
