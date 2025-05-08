from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bots.trend_swing import trend_swing_index
from bots.rsi_medium import rsi_medium_index

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/indice_swing/{ticker}")
def indice_swing(ticker: str):
    return trend_swing_index(ticker)

@app.get("/indice_medium/{ticker}")
def indice_medium(ticker: str):
    return rsi_medium_index(ticker)
