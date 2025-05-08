
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bots.rsi_medium import rsi_medium_index
from bots.trend_swing import trend_swing_index

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
        result[ticker] = {
            "Swing": {
                "indice": trend_swing_index(ticker).get("signal", 0),
                "note": trend_swing_index(ticker).get("note", "")
            },
            "Medium-Term": {
                "indice": rsi_medium_index(ticker).get("signal", 0),
                "note": rsi_medium_index(ticker).get("note", "")
            }
        }

    return result
