import requests
import time

API_KEY = "d0f2kn9r01qsv9eev9p0d0f2kn9r01qsv9eev9pg"
TICKERS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA']

def get_rsi(symbol):
    url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=D&indicator=rsi&timeperiod=14&token={API_KEY}"
    res = requests.get(url).json()
    rsi = res.get("rsi", [])
    return rsi[-1] if rsi else None

def get_price(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    res = requests.get(url).json()
    return res.get("c")

for ticker in TICKERS:
    try:
        rsi = get_rsi(ticker)
        price = get_price(ticker)
        print(f"{ticker} - RSI: {rsi}, Price: {price}")
        time.sleep(2.5)  # delay para no superar límites
    except Exception as e:
        print(f"Error con {ticker}: {e}")