import datetime as dt
import inspect
import pandas as pd
import yfinance as yf
import urllib.request
import json
import time
import inspect

CRYPTO_LIST = [
    "BTC",
    "ETH",
    "BNB",
    "ADA", 
    "SOL",
    "LUNA",
    "DOGE",
    "DOT",
    "AVAX",
    "MATIC",
    "ATOM",
    "CRO",
    "LINK",
    "LRC"
]

STOCK_LIST = [
]

def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }
    
def get_crypto_price(ticker="ETH", fiat="AUD", start=None, end=None):
    """Found from: https://medium.com/codex/10-best-resources-to-fetch-cryptocurrency-data-in-python-8400cf0d0136"""
    if start == None:
        start = end - dt.timedelta(365)
    else:
        start = dt.datetime.strptime(start, "%Y-%m-%d")
    if ticker in CRYPTO_LIST:
        df = yf.download(f'{ticker}-{fiat}', start=start, end=end)
    if ticker in STOCK_LIST:
        df = yf.download(f'{ticker}', start=start, end=end)
    df = df["Open"].to_frame()
    return df

def date_handler(date):
    date = date.strftime("%Y%m%d")
    return date

def mcap_fetcher():
    start = "2014-01-01" #No data from 1 Jan 2013
    end = dt.date.today()

    total_range = pd.date_range(start,end,freq='M')
    
    rows_list = []

    for date in total_range:
        timestamp = date_handler(date)
        # use urllib to get HTML data
        url = f"https://coinmarketcap.com/historical/{timestamp}/"
        contents = urllib.request.urlopen(url)
        bytes_str = contents.read()

        # decode bytes string
        data_str = bytes_str.decode("utf-8")

        # crop the raw JSON string out of the website HTML
        start_str = '"listingHistorical":{"data":'
        start = data_str.find(start_str)+len(start_str)
        end = data_str.find(',"page":1,"sort":""')
        cropped_str = data_str[start:end]

        # create a Python list from JSON string
        data_list = json.loads(cropped_str)

        for i in range(10):
            name = data_list[i]["name"]
            mcap = data_list[i]['quote']['USD']['market_cap']
            print(f"The Market Cap of {name} on {date} is {mcap}")
            rows_list.append({"Name": name ,"MCap": mcap, "Date": date.strftime("%d-%m-%Y")})
            time.sleep(1)
        df = pd.DataFrame(rows_list, columns=["Date", "Name", "MCap"]) 
        df.to_csv("data/initial/mcap.csv")

def tradfi(ticker):
    #Input the start and end date in the YYYY-MM-DD format
    start, end = "2015-01-15", "2021-2-2"
    #Input the pairing
    df = yf.download(f'{ticker}', start=start, end=end)
    print(df.head(5))


def main():
    #Input the start and end date in the YYYY-MM-DD format
    start, end = "2015-01-15", "2021-2-2"
    #Input the pairing
    crypto, fiat = "BTC", "USD"

    prices = get_crypto_price(crypto, fiat, start, end)
    print(prices)

if __name__== "__main__":
    main()
