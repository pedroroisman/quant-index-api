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
    try:
        importlib.reload(rsi_bot)
        importlib.reload(swing_bot)

        tickers = getattr(rsi_bot, "TICKERS", ["AAPL"])
        data = {}

        for ticker in tickers:
            try:
                rsi = rsi_bot.get_rsi(ticker)
                price = rsi_bot.get_price(ticker)
                swing = swing_bot.get_swing_index(ticker)

                swing_index = swing.get("index") if swing and "index" in swing else 0
                price_note = (
                    f"Price: {swing['price']}, Avg(20): {swing['avg']}"
                    if swing and "price" in swing and "avg" in swing
                    else "Data unavailable"
                )

                rsi_index = (
                    0 if rsi is None else 1 if rsi > 70 else -1 if rsi < 30 else 0
                )
                rsi_note = (
                    f"RSI: {rsi:.2f} → "
                    + (
                        "Overbought" if rsi > 70 else
                        "Oversold" if rsi < 30 else
                        "Neutral range"
                    )
                    if rsi is not None
                    else "RSI unavailable"
                )

                data[ticker] = {
                    "Swing": {
                        "indice": swing_index,
                        "note": price_note
                    },
                    "Medium-Term": {
                        "indice": rsi_index,
                        "note": rsi_note
                    }
                }

            except Exception as e:
                data[ticker] = {
                    "Swing": {
                        "indice": 0,
                        "note": f"Swing error: {e}"
                    },
                    "Medium-Term": {
                        "indice": 0,
                        "note": f"RSI error: {e}"
                    }
                }

        return data

    except Exception as e:
        return {"error": f"Global backend error: {e}"}