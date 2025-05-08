
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bots.rsi_medium import rsi_medium_index
from bots.trend_swing import trend_swing_index
import time

app = FastAPI()

# CORS para permitir acceso desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live_signals")
def obtener_live_signals():
    tickers = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA"]
    result = {}

    for ticker in tickers:
        swing = trend_swing_index(ticker)
        time.sleep(1)  # Evita exceder límite de API gratuita
        medium = rsi_medium_index(ticker)
        time.sleep(1)

        result[ticker] = {
            "Swing": {
                "indice": swing.get("signal", 0),
                "note": swing.get("note", "")
            },
            "Medium-Term": {
                "indice": medium.get("signal", 0),
                "note": medium.get("note", "")
            }
        }

    return result
