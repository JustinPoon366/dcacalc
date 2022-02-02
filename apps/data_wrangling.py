import pandas as pd
from multiprocessing import Value
from apps import fetch_data as fd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Assets citation
# https://www.flaticon.com/packs/trading-8?word=trading
# https://www.flaticon.com/packs/business-12?word=trading
# https://www.flaticon.com/packs/stock-market-5?word=stocks


def purchased_crypto(df, apr, rewards_freq, investment, investment_period, commission, dca_strategy = "Increment"):
    """Function that takes investment amount, investment period, APR and frequency of rewards distribution"""
    #Create a column with the DCA increment at the appropriate date
    
    #Daily
    if investment_period == "Daily":
        if dca_strategy == "Lump_Sum":
            num_days = len(df)
            increment = investment/num_days
        elif dca_strategy == "Increment":
            increment = investment
        df.insert(1, "Fiat Increment", increment)
    #Weekly
    if investment_period == "Weekly":
        if dca_strategy == "Lump_Sum":
            num_weeks = round(len(df)/7)
            increment = investment/num_weeks
        elif dca_strategy == "Increment":
            increment = investment
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
        if dca_strategy == "Lump_Sum":
            num_months = (df.last_valid_index().year - df.first_valid_index().year) * 12 + (df.last_valid_index().month - df.first_valid_index().month)
            increment = investment/num_months
        elif dca_strategy == "Increment":
            increment = investment
        #Create a column where the value is the increment
        df["Fiat Increment"] = increment
        #Create an index temporarily
        df.insert(0, 'Index', range(0,len(df)))
        #Slice it for the thirtieth row
        df[["Fiat Increment", "Index"]] = df[["Fiat Increment", "Index"]].loc[df.index.day == 1]
        df["Fiat Increment"] = df["Fiat Increment"].fillna(0)
        df = df.drop(columns="Index")
    #Lump Sum
    if investment_period == "Lump Sum":
        df["Fiat Increment"] = 0
        increment = investment
        df.loc[df.index[0], "Fiat Increment"] = investment

    #Work out the amount of crypto you would recieve each date (does not consider fees yet) by dividing the open price by the fiat increment
    df["Token Recieved"] = df["Fiat Increment"] / df["Open"] * (1 - commission / 100)
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

    #Format Increment for the card
    increment = f"${increment:,.2f}"

    return df, increment

def find_return_value(df):
    final_date = df.index[-1]
    final_value = df["Cumulative Fiat Value (Staked)"][final_date] #final portfolio value (staked)
    final_value = f"${final_value:,.2f}"
    return final_value

def find_final_date(df):
    final_date = df.index[-1]
    final_date = final_date.strftime('%d-%m-%Y')
    return final_date

def find_maximum_percent_loss(df):
    min_pl = df.PL.min()
    min_pl = f"{min_pl:,.2f}%"
    return min_pl


def final_stats(df, investment_period):
    final_date = find_final_date(df)
    final_value = find_return_value(df)
    min_pl = df.PL.min()
    min_pl = f"{min_pl:,.2f}%"

    df_profit_loss_absolute = df["Cumulative Fiat Value (Staked)"] - df["Cumulative Fiat Invested"]
    min_pl_abs = df_profit_loss_absolute.min()
    min_pl_abs = f"${min_pl_abs:,.2f}"
    min_date_abs = "(" + df_profit_loss_absolute.idxmin().strftime('%d %b %Y') + ")"

    max_pl_abs = df_profit_loss_absolute.max()
    max_pl_abs = f"${max_pl_abs:,.2f}"
    max_date_abs = "(" + df_profit_loss_absolute.idxmax().strftime('%d %b %Y') + ")"

    min_date = "(" + df["PL"].idxmin().strftime('%d %b %Y') + ")"
    max_pl = df.PL.max()
    max_pl = f"{max_pl:,.2f}%"
    max_date = "(" + df["PL"].idxmax().strftime('%d %b %Y') + ")"

    total_invested = df["Cumulative Fiat Invested"].iloc[-1]
    total_invested = f"${total_invested:,.2f}"
    
    if investment_period == "Daily":
        total_time = df.last_valid_index() - df.first_valid_index() 
        total_time = total_time.days
        total_time = f"{total_time} Days"
    
    elif investment_period == "Weekly":
        total_time = df.last_valid_index() - df.first_valid_index()     
        total_time = total_time.days // 7
        total_time = f"{total_time} Weeks"

    elif investment_period == "Monthly" or investment_period == "Lump Sum":
        total_time = (df.last_valid_index().year - df.first_valid_index().year) * 12 + (df.last_valid_index().month - df.first_valid_index().month)
        total_time = f"{total_time} Months"
    
    return final_value, final_date, min_pl, min_date, max_pl, max_date, min_pl_abs, max_pl_abs, total_invested, total_time, min_date_abs, max_date_abs

def main():
    #Input the start and end date in the YYYY-MM-DD format
    start, end = "2016-01-15", "2022-01-11"
    #Input the pairing
    crypto, fiat = "ETH", "USD"
    #Input the investment amount ($), investment period (Daily, Weekly, Monthly)
    investment, investment_period, dca_strategy = 100, "Daily", "Increment"
    #Input the commission
    commission = 0.1
    #Input the staking returns (%), rewards frequency (Monthly)
    apr, rewards_freq = 5, "Monthly"
    
    prices = fd.get_crypto_price(crypto, fiat, start, end)
    df, increment = purchased_crypto(prices, apr, rewards_freq, investment, investment_period, commission, dca_strategy)

    print(df)
    fv, final_date, min_pl, min_date, max_pl, max_date, min_pl_abs, max_pl_abs, total_invested, total_time = final_stats(df, investment_period)


    print(fv, final_date, min_pl, min_date, max_pl, max_date, min_pl_abs, max_pl_abs, total_invested, total_time)

    
if __name__== "__main__":
    main()