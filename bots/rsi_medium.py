import requests

API_KEY = "d0f6bbhr01qsv9efl33gd0f6bbhr01qsv9efl340"
TICKERS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA']

def get_rsi(symbol):
    try:
        url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=D&indicator=rsi&timeperiod=14&token={API_KEY}"
        res = requests.get(url).json()
        print(f"[RSI RAW] {symbol}: {res}")  # Debug
        rsi = res.get("rsi", [])
        return rsi[-1] if rsi else None
    except Exception as e:
        print(f"[RSI] Error con {symbol}: {e}")
        return None

def get_price(symbol):
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        res = requests.get(url).json()
        print(f"[PRICE RAW] {symbol}: {res}")  # Debug
        return res.get("c")
    except Exception as e:
        print(f"[PRICE] Error con {symbol}: {e}")
        return None
