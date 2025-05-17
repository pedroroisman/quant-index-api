from fastapi import FastAPI
from bots import rsi_medium, trend_swing

app = FastAPI()

TICKERS = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA"]

@app.get("/live_signals")
def get_live_signals():
    results = {}
    for ticker in TICKERS:
        results[ticker] = {
            "Swing": trend_swing.get_swing_index(ticker),
            "Medium-Term": rsi_medium.get_rsi_index(ticker)
        }
    return results
