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
