
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bots.rsi_medium import rsi_medium_index
from random import uniform

app = FastAPI()

# Habilitar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/indices")
def obtener_indices():
    acciones = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA", "META", "GOOGL", "NFLX"]
    horizontes = ["Intraday", "Swing", "Medium-Term"]

    resultado = []

    for accion in acciones:
        estrategias = []
        for horizonte in horizontes:
            indice_simulado = round(uniform(-1, 1), 2)
            estrategias.append({
                "horizonte": horizonte,
                "indice": indice_simulado
            })

        resultado.append({
            "ticker": accion,
            "estrategias": estrategias
        })

    return {"acciones": resultado}

@app.get("/indice_medium-term/{ticker}")
def obtener_indice_rsi(ticker: str):
    resultado = rsi_medium_index(ticker)

    return {
        "indice": resultado.get("signal", 0),
        "note": resultado.get("note", "")
    }
