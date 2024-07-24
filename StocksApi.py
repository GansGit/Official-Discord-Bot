from cogs.Config import Config
import requests

URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={Config.get_config("keys")["alphavantage"]}'


def get_data():
    request = requests.get(URL)
    data = request.json()
    print(data)

get_data()