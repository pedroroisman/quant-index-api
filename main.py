from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Orden(BaseModel):
    tipo: str
    precio_objetivo: float

class InputDatos(BaseModel):
    precio_actual: float
    ordenes: List[Orden]

@app.post("/indice")
def calcular_indice(input_datos: InputDatos):
    precio_actual = input_datos.precio_actual
    ordenes = input_datos.ordenes
    delta_factor = 0.1

    indices_parciales = []

    for orden in ordenes:
        delta = orden.precio_objetivo * delta_factor
        distancia = abs(precio_actual - orden.precio_objetivo)
        if distancia > delta:
            continue

        proximidad = 1 - (distancia / delta)
        indice_parcial = -proximidad if orden.tipo == "compra" else proximidad
        indices_parciales.append(indice_parcial)

    if not indices_parciales:
        return {"indice": 0}

    indice_total = sum(indices_parciales) / len(indices_parciales)
    return {"indice": round(indice_total, 4)}
