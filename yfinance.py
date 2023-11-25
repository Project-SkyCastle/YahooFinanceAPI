from fastapi import FastAPI, Response
import uvicorn
import requests
import json
from pathlib import Path
from dotenv import dotenv_values
import os


base_path = Path()
envars = base_path.cwd() / '.env'
print(envars)
print(os.path.dirname(os.path.abspath(__file__)))
config = dict(dotenv_values(envars))
# config = dict(dotenv_values(".env"))
app = FastAPI()
url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-chart"

@app.get("/")
async def root():
    return {"message": "/price/{ticker} for price data"}


@app.get("/price/{ticker}")
async def get_price(ticker: str):
    querystring = {
        "interval": "1mo",
        "symbol": ticker,
        "range": "5y"
    }

    headers = {
        "X-RapidAPI-Key": config["X-RapidAPI-Key"],
        "X-RapidAPI-Host": config["X-RapidAPI-Host"],
    }

    response = requests.get(url, headers=headers, params=querystring)

    return json.dumps({
        'date': response.json()['chart']['result'][0]['timestamp'],
        'price': response.json()['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)
