
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from random import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/indices")
def obtener_indices():
    acciones = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA"]
    horizontes = ["Intraday", "Swing", "Medium-Term"]

    resultado = []

    for accion in acciones:
        data = {
            "ticker": accion,
            "estrategias": []
        }
        for horizonte in horizontes:
            indice_simulado = round(-1 + 2 * random(), 2)
            data["estrategias"].append({
                "horizonte": horizonte,
                "indice": indice_simulado
            })
        resultado.append(data)

    return {"acciones": resultado}
