
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bots.rsi_medium import rsi_medium_index
from bots.trend_swing import trend_swing_index
import time

app = FastAPI()

# Cache en memoria: {ticker: {"data": {...}, "timestamp": ...}}
cache = {}

# Tiempo de validez del cache (en segundos)
CACHE_TTL = 120  # 2 minutos

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live_signals")
def obtener_live_signals():
    tickers = ["AAPL", "TSLA", "AMZN"]
    result = {}

    for ticker in tickers:
        now = time.time()
        # Usar cache si existe y no venció
        if ticker in cache and now - cache[ticker]["timestamp"] < CACHE_TTL:
            result[ticker] = cache[ticker]["data"]
            continue

        # Si no hay cache válido, obtener datos en vivo
        swing = trend_swing_index(ticker)
        time.sleep(4)
        medium = rsi_medium_index(ticker)
        time.sleep(4)

        data = {
            "Swing": {
                "indice": swing.get("signal", 0),
                "note": swing.get("note", "")
            },
            "Medium-Term": {
                "indice": medium.get("signal", 0),
                "note": medium.get("note", "")
            }
        }

        # Guardar en cache
        cache[ticker] = {"data": data, "timestamp": now}
        result[ticker] = data

    return result
