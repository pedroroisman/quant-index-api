import requests
from datetime import datetime

API_KEY = "2a0d5658f5204b06bb2d0ce50d9b7b16"

def rsi_medium_index(ticker="AAPL"):
    url = f"https://api.twelvedata.com/rsi?symbol={ticker}&interval=1day&outputsize=100&time_period=14&apikey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if "values" not in data or not data["values"]:
            return {
                "ticker": ticker,
                "horizon": "Medium-Term",
                "signal": 0,
                "note": data.get("message", "No data available, returning neutral signal"),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

        latest_rsi = float(data["values"][0]["rsi"])

        if latest_rsi < 30:
            signal = round((30 - latest_rsi) / 30 * -1, 2)
            note = f"RSI: {latest_rsi} → Oversold"
        elif latest_rsi > 70:
            signal = round((latest_rsi - 70) / 30 * 1, 2)
            note = f"RSI: {latest_rsi} → Overbought"
        else:
            signal = 0
            note = f"RSI: {latest_rsi} → Neutral range"

        return {
            "ticker": ticker,
            "horizon": "Medium-Term",
            "signal": signal,
            "note": note,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "horizon": "Medium-Term",
            "signal": 0,
            "note": f"Error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
