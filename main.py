
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bots import rsi_medium as rsi_bot
from bots import trend_swing as swing_bot
import importlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live_signals")
def live_signals():
    importlib.reload(rsi_bot)
    importlib.reload(swing_bot)

    tickers = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA"]
    data = {}

    for ticker in tickers:
        try:
            rsi_result = rsi_bot.get_rsi_index(ticker, api_key="2a0d5658f5204b06bb2d0ce50d9b7b16")
            swing_result = swing_bot.get_swing_index(ticker, api_key="2a0d5658f5204b06bb2d0ce50d9b7b16")

            data[ticker] = {
                "Swing": swing_result,
                "Medium-Term": rsi_result
            }
        except Exception as e:
            data[ticker] = {
                "Swing": {"indice": 0, "note": f"Swing error: {e}", "confidence": "low"},
                "Medium-Term": {"indice": 0, "note": f"RSI error: {e}", "confidence": "low"}
            }

    return data
