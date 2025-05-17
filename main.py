from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 👈 Importá esto
from bots import rsi_medium, trend_swing

app = FastAPI()

# 👇 Agregá esta configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # También podés usar ["https://quant-index-react.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TICKERS = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA"]

@app.get("/live_signals")
def get_live_signals():
    results = {}
    for ticker in TICKERS:
        results[ticker] = {
            "1-5 days": trend_swing.get_swing_index(ticker),
            "7-30 days": rsi_medium.get_rsi_index(ticker)
        }
    return results
