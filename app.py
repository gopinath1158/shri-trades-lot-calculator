from flask import Flask, render_template, request
import requests

app = Flask(__name__)

ASSETS = {
    "XAUUSD": {"symbol": "XAUUSD", "contract": 100},
    "BTCUSD": {"symbol": "BTCUSDT", "contract": 1},
    "ETHUSD": {"symbol": "ETHUSDT", "contract": 1},
    "SOLUSD": {"symbol": "SOLUSDT", "contract": 1},
    "USDJPY": {"symbol": "USDJPY", "contract": 100000}
}

def get_price(symbol):
    try:
        if "USDT" in symbol:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            data = requests.get(url).json()
            return float(data['price'])
    except:
        return 0
    return 1

@app.route("/", methods=["GET","POST"])
def index():
    result = None
    if request.method == "POST":
        asset = request.form["asset"]
        capital = float(request.form["capital"])
        risk = float(request.form["risk"])
        sl = float(request.form["sl"])
        rr = float(request.form["rr"])
        leverage = float(request.form["leverage"])

        price = get_price(ASSETS[asset]["symbol"])
        contract = ASSETS[asset]["contract"]

        risk_amount = capital * risk / 100
        lot = risk_amount / sl
        tp = sl * rr
        profit = tp * lot
        margin = (lot * contract) / leverage

        result = {
            "asset": asset,
            "price": round(price,2),
            "risk": round(risk_amount,2),
            "lot": round(lot,3),
            "tp": round(tp,2),
            "profit": round(profit,2),
            "margin": round(margin,2)
        }

    return render_template("index.html", result=result, assets=ASSETS)

if __name__ == "__main__":
    app.run(debug=True)