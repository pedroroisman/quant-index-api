
import yfinance as yf

TICKERS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA']

def get_swing_index(symbol):
    try:
        df = yf.download(symbol, period="1mo", interval="1d", progress=False)
        closes = df['Close'].dropna()
        if len(closes) < 20:
            return None
        avg = closes[-20:].mean()
        price = closes.iloc[-1]
        index = round((price - avg) / avg, 2)
        return {"index": index, "price": round(price, 2), "avg": round(avg, 2)}
    except Exception as e:
        print(f"[SWING yfinance] Error con {symbol}: {e}")
        return None
