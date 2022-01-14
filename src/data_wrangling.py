from multiprocessing import Value
from fetch_data import *

def purchased_crypto(df, apr, rewards_freq, investment=0, investment_period=""):
    """Function that takes investment amount, investment period, APR and frequency of rewards distribution"""

    #Create a column with the DCA increment at the appropriate date
    
    #Daily
    if investment_period == "Daily":
        num_days = len(df)
        increment = investment/num_days
        df.insert(1, "Fiat Increment", increment)
    #Weekly
    if investment_period == "Weekly":
        num_weeks = round(len(df)/7)
        increment = investment/num_weeks
        #Create a column where the value is the increment
        df["Fiat Increment"] = increment
        #Create an index temporarily
        df.insert(0, 'Index', range(0,len(df)))
        #Slice it for the seventh row
        df[["Fiat Increment", "Index"]] = df[["Fiat Increment", "Index"]].loc[df['Index'] % 7 == 0]
        df["Fiat Increment"] = df["Fiat Increment"].fillna(0)
        df = df.drop(columns="Index")
    #Monthly
    if investment_period == "Monthly":
        num_months = round(len(df)/30)
        increment = investment/num_months
        #Create a column where the value is the increment
        df["Fiat Increment"] = increment
        #Create an index temporarily
        df.insert(0, 'Index', range(0,len(df)))
        #Slice it for the thirtieth row
        df[["Fiat Increment", "Index"]] = df[["Fiat Increment", "Index"]].loc[df['Index'] % 30 == 0]
        df["Fiat Increment"] = df["Fiat Increment"].fillna(0)
        df = df.drop(columns="Index")

    #Work out the amount of crypto you would recieve each date (does not consider fees yet) by dividing the open price by the fiat increment
    df["Token Recieved"] = df["Fiat Increment"] / df["Open"]
    #Work Out Cumulative Fiat Invested
    df["Cumulative Fiat Invested"] = df["Fiat Increment"].cumsum()
    #Calculate the total tokens held at each date
    df["Cumulative Tokens"] = df["Token Recieved"].cumsum()

    #Create a column that calculates the staking rewards
    #Increase cumulative tokens at the start of every month
    if rewards_freq == "Monthly":
        # df['Final Cumulative Tokens'] = (df['Cumulative Tokens'] * df['Stake Rate'].shift().add(1).cumprod().fillna(1)).cumsum()
        num_months = round(len(df)/30)
        #Create a column where the value is the increment
        df["Staking Increment"] = apr / 12 / 100
        #Create an index temporarily
        df.insert(0, 'Index', range(0,len(df)))
        #Slice it for the thirtieth row
        df[["Staking Increment", "Index"]] = df[["Staking Increment", "Index"]].loc[df['Index'] % 30 == 0]
        df["Staking Increment"] = df["Staking Increment"].fillna(0)
        df = df.drop(columns="Index")
        df["Cum Staking Returns"] = df['Staking Increment'].shift().add(1).cumprod().fillna(1)
        df["Cumulative Tokens (Staked)"] = df['Cumulative Tokens'] * df["Cum Staking Returns"]


    #Calculate the the fiat value of the total holdings
    df["Cumulative Fiat Value"] = df["Cumulative Tokens"] * df["Open"]
    #Calculate the fiat value with staking
    df["Cumulative Fiat Value (Staked)"] = df["Cumulative Tokens (Staked)"] * df["Open"]
    #Create a column where the index is the date
    df["Date"] = df.index
    #Create a column for the net loss/gain (%)
    df["PL"] = (df["Cumulative Fiat Value (Staked)"] - df["Cumulative Fiat Invested"]) / df["Cumulative Fiat Invested"] * 100
    return df

def final_stats(df):
    final_date = df.index[-1]
    fv = df["Cumulative Fiat Value (Staked)"][final_date] #final portfolio value (staked)
    fv = f"${fv:,.2f}"
    final_date = final_date.strftime('%d-%m-%Y')
    min_pl = df.PL.min()
    min_pl = f"{min_pl:,.2f}%"
    min_date = "(" + df["PL"].idxmin().strftime('%d %b %Y') + ")"
    max_pl = df.PL.max()
    max_pl = f"{max_pl:,.2f}%"
    max_date = "(" + df["PL"].idxmax().strftime('%d %b %Y') + ")"
    return fv, final_date, min_pl, min_date, max_pl, max_date

def main():
    #Input the start and end date in the YYYY-MM-DD format
    start, end = "2016-01-15", "2022-01-11"
    #Input the pairing
    crypto, fiat = "ETH", "USD"
    #Input the investment amount ($), investment period (Daily, Weekly, Monthly)
    investment, investment_period = 10000, "Monthly"

    #Input the staking returns (%), rewards frequency (Monthly)
    apr, rewards_freq = 5, "Monthly"
    
    prices = get_crypto_price(crypto, fiat, start, end)
    df = purchased_crypto(prices, apr, rewards_freq, investment, investment_period)
    
    fv, final_date, min_pl, min_date, max_pl, max_date = final_stats(df)

    print(fv, final_date, min_pl, min_date, max_pl, max_date)
if __name__== "__main__":
    main()