from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bots import rsi_medium, trend_swing

app = FastAPI()

# CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o reemplazá con ["https://quant-index-react.vercel.app"] si querés limitar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TICKERS = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA"]
API_KEY = "2a0d5658f5204b06bb2d0ce50d9b7b16"  # reemplazá si usás otra

@app.get("/live_signals")
def get_live_signals():
    results = {}
    for ticker in TICKERS:
        results[ticker] = {
            "1-5 days": trend_swing.get_swing_index(ticker, API_KEY),
            "7-30 days": rsi_medium.get_rsi_index(ticker, API_KEY)
        }
    return results
