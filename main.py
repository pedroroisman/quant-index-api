
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bots import rsi_medium as rsi_bot
from bots import trend_swing as swing_bot
import importlib
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache: {ticker: {"data": ..., "timestamp": ...}}
CACHE = {}
CACHE_DURATION = timedelta(minutes=30)  # Recomendado para Alpha Vantage

@app.get("/live_signals")
def live_signals():
    importlib.reload(rsi_bot)
    importlib.reload(swing_bot)

    tickers = rsi_bot.TICKERS
    data = {}
    now = datetime.utcnow()

    for ticker in tickers:
        cached = CACHE.get(ticker)
        if cached and now - cached["timestamp"] < CACHE_DURATION:
            data[ticker] = cached["data"]
            continue

        try:
            rsi_index, rsi_note, rsi_conf = rsi_bot.get_rsi_index(ticker)
            price = rsi_bot.get_price(ticker)
            swing = swing_bot.get_swing_index(ticker)

            swing_valid = swing is not None and isinstance(swing, dict)

            result = {
                "Swing": {
                    "indice": swing["index"] if swing_valid else 0,
                    "note": swing["note"] if swing_valid else "Swing unavailable",
                    "confidence": swing["confidence"] if swing_valid else "low"
                },
                "Medium-Term": {
                    "indice": rsi_index,
                    "note": rsi_note,
                    "confidence": rsi_conf
                }
            }

            CACHE[ticker] = {"data": result, "timestamp": now}
            data[ticker] = result

        except Exception as e:
            data[ticker] = {
                "Swing": {"indice": 0, "note": f"Swing error: {e}", "confidence": "low"},
                "Medium-Term": {"indice": 0, "note": f"RSI error: {e}", "confidence": "low"}
            }

    return data
