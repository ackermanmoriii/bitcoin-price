import pandas as pd
import requests

def get_bitcoin_price():
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    data = response.json()
    price = data['bpi']['USD']['rate_float']
    return price

if __name__ == "__main__":
    current_price = get_bitcoin_price()
    print(f"Current Bitcoin price: ${current_price:,.2f} USD")