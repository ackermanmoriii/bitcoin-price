import pandas as pd
import requests
from flask import Flask

app = Flask(__name__)

def get_bitcoin_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    data = response.json()
    price = data['bpi']['USD']['rate_float']
    return price

@app.route('/')
def home():
    current_price = get_bitcoin_price()
    return f"Current Bitcoin price: ${current_price:,.2f} USD"

@app.route('/test')
def test_route():
    return "This is a simple test route!"

if __name__ == "__main__":
    app.run(debug=True)