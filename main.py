
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bots import rsi_medium as rsi_bot
from bots import trend_swing as swing_bot
import importlib
import math

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

    tickers = rsi_bot.TICKERS
    data = {}
    for ticker in tickers:
        try:
            rsi = rsi_bot.get_rsi(ticker)
            price = rsi_bot.get_price(ticker)
            swing = swing_bot.get_swing_index(ticker)

            rsi_valid = rsi is not None and not math.isnan(rsi)
            swing_valid = swing is not None

            data[ticker] = {
                "Swing": {
                    "indice": swing["index"] if swing_valid else 0,
                    "note": f"Price: {swing['price']}, Avg(20): {swing['avg']}" if swing_valid else "Data unavailable"
                },
                "Medium-Term": {
                    "indice": 0 if not rsi_valid else 1 if rsi > 70 else -1 if rsi < 30 else 0,
                    "note": f"RSI: {rsi:.2f} → {'Overbought' if rsi > 70 else 'Oversold' if rsi < 30 else 'Neutral range'}" if rsi_valid else "RSI unavailable"
                }
            }
        except Exception as e:
            data[ticker] = {
                "Swing": {"indice": 0, "note": f"Swing error: {e}"},
                "Medium-Term": {"indice": 0, "note": f"RSI error: {e}"}
            }

    return data
