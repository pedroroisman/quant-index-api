
import yfinance as yf

TICKERS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA']

def get_rsi(symbol, period=14):
    try:
        df = yf.download(symbol, period="1mo", interval="1d", progress=False)
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1].item() if not rsi.empty else None
    except Exception as e:
        print(f"[RSI yfinance] Error con {symbol}: {e}")
        return None

def get_price(symbol):
    try:
        df = yf.download(symbol, period="1d", interval="1m", progress=False)
        return df['Close'].iloc[-1].item() if not df.empty else None
    except Exception as e:
        print(f"[PRICE yfinance] Error con {symbol}: {e}")
        return None
