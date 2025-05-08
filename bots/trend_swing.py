
import requests
from datetime import datetime

API_KEY = "2a0d5658f5204b06bb2d0ce50d9b7b16"

def trend_swing_index(ticker="AAPL"):
    url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=5min&outputsize=50&apikey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if "values" not in data or len(data["values"]) < 20:
            return {
                "ticker": ticker,
                "horizon": "Swing",
                "signal": 0,
                "note": data.get("message", "No data available, returning neutral signal"),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

        closes = [float(item["close"]) for item in data["values"][:20]]
        current_price = float(data["values"][0]["close"])
        average_price = sum(closes) / len(closes)
        diff = current_price - average_price

        signal = round(max(min(diff / average_price * 10, 1), -1), 2)

        return {
            "ticker": ticker,
            "horizon": "Swing",
            "signal": signal,
            "note": f"Price: {current_price}, Avg(20): {round(average_price, 2)}",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "horizon": "Swing",
            "signal": 0,
            "note": f"Error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
