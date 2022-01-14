import urllib.request
import json
import pprintpp
import datetime as dt
import pandas as pd
import time

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
        print(start)

        # create a Python list from JSON string
        data_list = json.loads(cropped_str)

        for i in range(10):
            name = data_list[i]["name"]
            mcap = data_list[i]['quote']['USD']['market_cap']
            print(f"The Market Cap of {name} on {date} is {mcap}")
            rows_list.append({"Name": name ,"MCap": mcap, "Date": date.strftime("%d-%m-%Y")})
            time.sleep(1)
        print(rows_list)
        df = pd.DataFrame(rows_list, columns=["Date", "Name", "MCap"]) 
        df.to_csv("data/initial/mcap.csv")

def main():
    mcap_fetcher()

if __name__ == "__main__":
    main()

