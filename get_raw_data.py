from datetime import datetime, timedelta
import requests
import os

from pydantic.error_wrappers import ValidationError
from financial.repository import FinancialDataRepository
from financial.database import engine
from financial import model
from financial import schema


api_domain = os.environ["ALPHAVANTAGE_DOMAIN"]
api_key = os.environ["ALPHAVANTAGE_APIKEY"]
proxies = {
   'http': os.environ["http_proxy"],
   'https': os.environ["https_proxy"],
}
SYMBOLS = ["IBM", "AAPL"]
financial_data_repository = FinancialDataRepository()
model.Base.metadata.create_all(bind=engine)

for symbol in SYMBOLS:
    url = f"{api_domain}/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize=compact"
    rsp = requests.get(url=url, proxies=proxies)

    if rsp.status_code != 200:
        print(rsp.text)
        exit(-1)

    try:
        data = rsp.json()["Time Series (Daily)"]
    except KeyError:
        print("Cannot found Time Series (Daily) data in the response")
        exit(-1)

    stock_quotes = []
    # start date is the date of 14 days ago
    start = (datetime.now() - timedelta(14)).strftime("%Y-%m-%d")
    for date, quotes in data.items():
        if date > start:
            try:
                open_price = quotes["1. open"]
                close_price = quotes["4. close"]
                volume = quotes["6. volume"]
                # validate stock_quotes value
                schema.FinancialData(
                    symbol=symbol,
                    date=date,
                    open_price=open_price,
                    close_price=close_price,
                    volume=volume
                )
                stock_quotes.append((
                    symbol,
                    date,
                    open_price,
                    close_price,
                    volume
                ))
            # skip invalid data
            except KeyError:
                print(f"Cannot find required key, skip: {date}|{quotes}")
            except ValidationError:
                print(f"data validation error, skip: {date}|{quotes}")

    financial_data_repository.upsert_financial_data(stock_quotes=stock_quotes)
