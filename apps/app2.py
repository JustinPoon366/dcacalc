from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app

layout = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4(["What is Dollar Cost Averaging?"])], style={'text-align':'center'}
                ),
                dbc.CardBody([
                        html.Div(["""Dollar cost averaging consists in investing a fixed amount of fiat currency (such as USD), into cryptocurrency, on regular time intervals. It is often abbreviated to "DCA" for convenience. """]),
                        html.Br(),
                        html.Div(["Purchasing $100 every week, for example, would be dollar cost averaging."]),
                        html.Br(),
                        html.Div(["This strategy is mostly used by investors that are looking to invest in crypto for the long-term, since it reduces short-term volatility"]),
                        html.Br(),
                        html.Div([
                            html.Div("Credit: Much of the information on this page has been adapted from ", style={"display":"inline-block", "white-space":"pre"}),
                            dbc.CardLink("https://dcabtc.com/", href="https://dcabtc.com/", style={"display":"inline-block"}),
                        ], style={"white-space":"no-wrap"}),
                ])
            ], color="light"),
            html.Br(),
            dbc.Card([
                dbc.CardHeader([
                    html.H4(["Pros and Cons of Dollar Cost Averaging"])], style={'text-align':'center'}
                ),
                dbc.CardBody([
                        html.H5("Pros of Dollar Cost Averaging"),
                        html.Br(),
                        html.H6("1) Eliminates the risk of only buying market tops", style={"font-weight":"bold"}),
                        html.Div("Given that purchses are spread across regular intervals it is very unlikely that you would only purchase assets at their highest price."),
                        html.Br(),
                        html.Div("This is key for crypto, which can drop -50% from its highest price in a matter of weeks, as was the case in January 2018, May 2021 and January 2022."),
                        html.Br(),
                        html.H6("2) Doesn’t require large amounts of upfront capital", style={"font-weight":"bold"}),
                        html.Div("Since DCA strategies are involve making small, yet regular, purchases, you will not have to commit large amounts of capital from the beginning."),
                        html.Br(),
                        html.Div("This is an especially useful if you don’t feel comfortable with investing all your savings into crypto, and instead allocate a small portion from your paycheck every payday."),
                        html.Br(),
                        html.H6("3) Gives you time to understand cryptocurrencies", style={"font-weight":"bold"}),
                        html.Div("Everyone that held Bitcoin for more than 3 years, is in profit on their initial purchase. However, many people panic sell just shortly after making their purchase."),
                        html.Br(),
                        html.Div("These investors often do so because they did not take the time to properly understand crypto, and react emotionally after a sharp BTC price decline."),
                        html.Br(),
                        html.Div("In order to avoid making the same mistake, it is crucial that you understand the value proposition of Bitcoin and that it should NOT be seen as a get rich quick scheme."),
                        html.Br(),
                        html.H5("Cons of Dollar Cost Averaging"),
                        html.Br(),
                        html.H6("1) Eliminates possibility of buying exact bottoms", style={"font-weight":"bold"}),
                        html.Div("While dollar cost averaging prevents you from allocating all your capital at the exact top, unfortunately it does the same for the bottom."),
                        html.Br(),
                        html.Div("If you follow a dollar cost averaging strategy, it is impossible to allocate all your funds at the exact bottom. Some purchases will have always be made at a higher price, if the strategy was executed properly."),
                        html.Br(),
                        html.H6("2) Takes time to get desired exposure", style={"font-weight":"bold"}),
                        html.Div("The very core of a DCA strategy, regular small purchases, mean that it will take some time to get your desired exposure."),
                        html.Br(),
                        html.H6("3) Potentially lower performance in strong bull market", style={"font-weight":"bold"}),
                        html.Div("If crypto is in a strong bull market, certainly the best move would be to make the entire purchase at once, since the next time you would dollar cost average, price is likely higher."),
                        html.Br(),
                        html.Div("This is a major downside of the DCA approach."),
                        html.Br(),
                        html.Div("However, on the other hand, how do you know for sure if Bitcoin is in a bull cycle? What if price just showed some strength, and retraces the entire rally by the end of the month? Also, how can you be sure that you're not investing into the top of a bull cycle?"),
                ])
            ], color="light")
        ], width="8")
    ], justify="center")
])


@app.callback(
    Output('app-1-display-value', 'children'),
    Input('app-1-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)