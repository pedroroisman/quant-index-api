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

@app.get("/indice_swing")
def calcular_indice_swing():
    return trend_swing_index("AAPL")

@app.get("/indice_medium")
def calcular_indice_medium():
    return rsi_medium_index("AAPL")