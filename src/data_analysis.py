import fetch_data as fd
import data_wrangling as dw
import pandas as pd
import seaborn as sns
import yfinance as yf
import plotly_express as px


sns.set_theme(style="darkgrid")

def calculate_returns(df, crypto):
    investment = df["Fiat Increment"].sum()
    tt = sum(df["Token Recieved"])
    fvi = tt * df["Open"].iloc[-1]
    roi = f"{(fvi-investment)/investment * 100:.2f}%"
    print(f"Total {crypto}: ", tt)
    print(f"Total amount invested is:", investment)
    print("Final Value of Investment:", fvi)
    print("Return on investment: ", roi)

def px_timeseries(crypto, df, investment_period):
    #Adjust the data
    df = df.melt(
    id_vars='Date', 
    value_vars=["Cumulative Fiat Value", "Cumulative Fiat Invested"])
    fig = px.line(df, 
        x="Date", 
        y="value", 
        title=f'Dollar Cost Averaging Using {investment_period} Increments', color="variable")
    fig.show()

def px_log_timeseries(df, investment_period):
    """https://towardsdatascience.com/visualization-with-plotly-express-comprehensive-guide-eb5ee4b50b57"""
    fig = px.line(df, 
        x="Date", 
        y="Cumulative Fiat Value", 
        title=f'Dollar Cost Averaging Using {investment_period} Increments - Log Graph', hover_data=['Cumulative Fiat Invested', "Cumulative Fiat Value"], log_y=True)
    fig.show()


def data_visualisation(crypto, df, investment_period):
    px_timeseries(crypto, df, investment_period)
    px_log_timeseries(df, investment_period)
#%%
def main():
    #Input the start and end date in the YYYY-MM-DD format
    start, end = "2016-01-15", "2021-11-25"
    #Input the pairing
    crypto, fiat = "LRC", "USD"
    #Input the investment amount ($), investment period (Daily, Weekly, Monthly)
    investment, investment_period = 20000, "Monthly"
    
    prices = fd.get_crypto_price(crypto, fiat, start, end)
    results = dw.purchased_crypto(prices, investment, investment_period)
    calculate_returns(results, crypto)
    data_visualisation(crypto, results, investment_period)  


if __name__== "__main__":
    main()
# %%
