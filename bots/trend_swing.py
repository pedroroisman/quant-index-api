import requests

API_KEY = "2a0d5658f5204b06bb2d0ce50d9b7b16"

def trend_swing_index(ticker="AAPL"):
    url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=5min&outputsize=50&apikey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if "values" not in data:
            return {
                "ticker": ticker,
                "horizon": "Swing",
                "indice": 0,
                "note": data.get("message", "No data available, returning neutral signal")
            }

        # Tomamos los últimos 20 valores y calculamos la media de cierre
        closes = [float(item["close"]) for item in data["values"][:20]]
        current_price = float(data["values"][0]["close"])
        average_price = sum(closes) / len(closes)

        diff = current_price - average_price
        spread = abs(diff) / average_price

        # Normalizamos a -1 a 1
        indice = round(max(min(diff / average_price * 10, 1), -1), 2)

        return {
            "ticker": ticker,
            "horizon": "Swing",
            "indice": indice,
            "note": f"Price: {current_price}, Avg(20): {round(average_price, 2)}"
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "horizon": "Swing",
            "indice": 0,
            "note": f"Error: {str(e)}"
        }