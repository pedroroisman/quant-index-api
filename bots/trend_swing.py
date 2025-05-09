import requests
import time

API_KEY = "d0f2kn9r01qsv9eev9p0d0f2kn9r01qsv9eev9pg"
TICKERS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA']

for ticker in TICKERS:
    try:
        url = f"https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=D&count=20&token={API_KEY}"
        res = requests.get(url).json()
        if res.get("s") == "ok":
            closes = res["c"]
            avg = sum(closes) / len(closes)
            price = closes[-1]
            index = round((price - avg) / avg, 2)
            print(f"{ticker} - Swing Index: {index} | Price: {price}, Avg(20): {avg}")
        else:
            print(f"Datos no disponibles para {ticker}")
        time.sleep(2.5)
    except Exception as e:
        print(f"Error con {ticker}: {e}")