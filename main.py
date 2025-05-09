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

                data[ticker] = {
                    "Swing": {
                        "indice": swing["index"] if swing else 0,
                        "note": f"Price: {swing['price']}, Avg(20): {swing['avg']}" if swing else "No data"
                    },
                    "Medium-Term": {
                        "indice": 0 if rsi is None else 1 if rsi > 70 else -1 if rsi < 30 else 0,
                        "note": f"RSI: {rsi:.2f} → {'Overbought' if rsi > 70 else 'Oversold' if rsi < 30 else 'Neutral range'}"
                    }
                }
            except Exception as e:
                data[ticker] = {
                    "Swing": {
                        "indice": 0,
                        "note": f"Error getting swing data: {e}"
                    },
                    "Medium-Term": {
                        "indice": 0,
                        "note": f"Error getting RSI: {e}"
                    }
                }

        return data

    except Exception as e:
        return {"error": f"Backend failure: {e}"}