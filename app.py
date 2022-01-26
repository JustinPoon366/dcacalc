import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
import datetime as dt

from dash.dependencies import Input, Output, State, ClientsideFunction
import data_wrangling as dw
import fetch_data as fd
import dash_bootstrap_components as dbc
from scipy import signal

from fetch_data import STOCK_LIST, CRYPTO_LIST


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = 'Crypto Dollar Cost Calculator'
server = app.server

TIME_PERIOD = [
    "Daily",
    "Weekly",
    "Monthly", 
    "Lump Sum"
]

colors = {
    "background":"rgb(82, 82, 82)",
    "fig_background": "rgba(0,0,0,0)"
    }

def blank_fig():
    """Create an empty space when loading the graph"""
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None, plot_bgcolor=colors["fig_background"], paper_bgcolor=colors["fig_background"],)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig

def generate_line_graph(df):
    fig = go.Figure() #initialise the figure
    last_row = df.iloc[-1]
    adj_df = df.iloc[::5, :]
    adj_df = adj_df.append(last_row)
    fig.update_xaxes(hoverformat="%-d/%-m/%Y") #update the date format (incl. hover info)

    fig.add_trace(go.Scatter(
        name="Portfolio Value ($)",
        line = dict(width=2, color="#16c784"), 
        x=adj_df["Date"], 
        y=adj_df["Cumulative Fiat Value (Staked)"], 
        showlegend=False,
        hoverinfo='skip', #skip the default hover text
        hovertemplate=
        "Portfolio Value ($): %{y:,.2f}<br>" + 
        "<extra></extra>" #removes the trace name/index
        ))
    fig.add_trace(go.Scatter(
        name="Amount invested ($)",
        line = dict(width=0.2, color="#16c784"),
        x=df["Date"], 
        y=df["Cumulative Fiat Invested"],
        showlegend=False,
        hovertemplate=
        "Amount Invested ($): %{y:,.2f}<br>" +
        "<extra></extra>"
        ))
    fig.update_layout(
        hovermode="x unified",
        hoverlabel_bgcolor="White",
        margin=dict(t=20),
        plot_bgcolor=colors["fig_background"],
        paper_bgcolor=colors["fig_background"],
        yaxis_tickprefix = '$',
        yaxis_tickformat = ',',
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            dtick="M3",
            tickformat="%b\n%Y",
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
        ),
    ),
        yaxis=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor="rgb(204, 204, 204)",
            showline=False,
            zerolinecolor=colors["fig_background"],
            linecolor='rgb(204, 204, 204)',
            showticklabels=True,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
        ),
    ))
    return fig


control_card = dbc.Card(children=
        [   
        dbc.CardHeader("Calculator Settings", style={"font-size":"20px"}),    
        dbc.CardBody(
            [
                dbc.Label("Select Crypto"),
                dcc.Dropdown(
                id='crypto-dropdown',
                options= [{'label': k, 'value': k} for k in CRYPTO_LIST + STOCK_LIST],
                value='BTC', 
                persistence_type="session"
                ),
                dbc.Label("DCA Strategy"),
                dbc.RadioItems(
                    options=[
                        {"label": "Investment Increment Known", "value": "Increment"},
                        {"label": "Total Amount to Invest Known", "value": "Lump_Sum"},
                    ],
                    value="Increment",
                    id="dca-strategy-radio-items",
                    inline=True,
                ),
                dbc.Label("Enter Investment Frequency"),
                dcc.Dropdown(
                    id='time-period-dropdown',
                    options= [{'label': k, 'value': k} for k in TIME_PERIOD],
                    value='Weekly', 
                    persistence_type="session"
                ),
                dbc.Label("Enter Amount"),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText("$", style={"background-color":"#b58900", "color":"#fff"}),
                        dbc.Input(
                            id = 'investment-amount',  
                            type="number",
                            value=100,
                            min=0,
                            debounce=True,
                            required=True,
                            style={"background-color":"#fff"}),
                        dbc.InputGroupText(".00", style={"background-color":"#b58900", "color":"#fff"}),
                    ]
                ),
                dbc.Label("Enter Investment Date Range"),
                dbc.Row([dcc.DatePickerRange(
                    id="my-date-picker-range", 
                    calendar_orientation="horizontal", 
                    reopen_calendar_on_clear=True, 
                    updatemode="singledate", 
                    start_date= dt.datetime.strptime("2016-01-15", "%Y-%m-%d").date(), 
                    end_date= dt.datetime.now().date()
                )]),
                dbc.Label("Enter Annual Staking Returns"),
                dbc.InputGroup(children=
                    [
                        dbc.Input(
                            id = 'staking-returns',  
                            type="number",
                            value=0,
                            min=0,
                            debounce=True,
                            required=True,
                            style={"background-color":"#fff"}
                            ),
                        dbc.InputGroupText("%", style={"background-color":"#b58900", "color":"#fff"}),
                    ]),
                dbc.Label("Enter Rewards Frequency"),
                dcc.Dropdown(
                    id='staking-time-period-dropdown',
                    options= [{'label': "Monthly", 'value': "Monthly"}],
                    value='Monthly', 
                    disabled=True),
            ]),
        ], color="light"
)

graph_card = dbc.Card([
    dbc.CardHeader(["Portfolio Value Over Time"],style={"font-size":"20px"}),
    dbc.CardBody
    ([
        dcc.Graph
            (
                id='display-selected-values',
                responsive=True,
                figure=blank_fig(),
                
            ),
    ],
    style={"height": "450px"}
    )
])


def stat_card(id_value, description, image, id_date="", id_freq=""):
    stat_cards= dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dbc.CardImg(
                    src=image,
                    style={"height": "40px", "width":"40px"}, className="img-fluid align-middle"),
                style={"height": "100%", "padding": "0.5rem 0rem 0rem 1rem"}, width={"size": 3}),
                dbc.Col([
                    dbc.Label(description, style={"font-size":"18px"}),
                    html.Div(id=id_value),
                    html.Div(id=id_date, style={"font-size": "12px", "color":"grey"}),
                    html.Div(id=id_freq, style={"font-size": "12px", "color":"grey"})
                ], width={"size": 9})
            ], style={"height":"100%"})    
        ],style={"height": "100px", "padding": "1rem 2rem"})
    ], color="light")
    return stat_cards

coffee_card= dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                dcc.Link([
                    dbc.CardImg(
                        src="https://img.buymeacoffee.com/api/?name=Justin+Poon&size=300&bg-image=bmc&background=5F7FFF",
                        style={"height": "50px", "width":"50px", "border-radius":"50%"}, className="img-fluid align-middle")
                ], href="https://www.buymeacoffee.com/dcacrypto"),
            style={"height": "100%"}, width={"size": 3}),
            dbc.Col([
                dbc.NavLink("Help me pay for server costs and buy me a coffee!", href="https://www.buymeacoffee.com/dcacrypto", style={"padding":"0rem 0rem"}),
            ], width={"size": 9})
        ], style={"height":"100%"})    
    ],style={"height": "100px", "padding": "1rem 2rem"})
], color="light")


header = html.H4('Crypto Dollar Cost Average Calculator', className="text-center mt-3 mb-4")

app.layout = html.Div(id="output-clientside", children=[
    dbc.Card(
        dbc.CardBody([
            dbc.Row(header),
            dbc.Row([
                dbc.Col(stat_card("final-return-value", "Total Portfolio Value", "/assets/images/bill.png"), width={"size": 3}),
                dbc.Col(stat_card('min-return-percentage', "Maximum Loss (%)", "/assets/images/loss.png", "min-return-date"), width={"size": 3}),
                dbc.Col(stat_card('max-return-percentage', "Maximum Gain (%)", "/assets/images/rocket.png", "max-return-date"), width={"size": 3}),
                dbc.Col(coffee_card, width={"size": 3})
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(stat_card("increment", "Investment Increment", "/assets/images/deposit.png", id_freq="investment-period"), width={"size": 3}),
                dbc.Col(stat_card('min-return-absolute', "Maximum Loss ($)", "/assets/images/euro-down.png"), width={"size": 3}),
                dbc.Col(stat_card('max-return-absolute', "Maximum Gain ($)", "/assets/images/pound-up.png"), width={"size": 3}),
                dbc.Col(stat_card('amount_invested', "Total Fiat Invested ($)", "/assets/images/money-bag.png"), width={"size": 3}),
            ]),
            html.Br(),
            dbc.Row(children=[
                dbc.Col(control_card, width={"size": 3}),
                dbc.Col(graph_card,width={"size": 9})
            ])
        ]), 
        # html.Footer([
            
        # ])
    )], className="gradient_background")


@app.callback(
    dash.dependencies.Output('display-selected-values', 'figure'),
    dash.dependencies.Output('final-return-value', 'children'),
    dash.dependencies.Output('min-return-percentage', 'children'),
    dash.dependencies.Output('min-return-date', 'children'),
    dash.dependencies.Output('max-return-percentage', 'children'),
    dash.dependencies.Output('max-return-date', 'children'),
    dash.dependencies.Output('investment-period', 'children'),
    dash.dependencies.Output('increment', 'children'),
    dash.dependencies.Output('min-return-absolute', 'children'),
    dash.dependencies.Output('max-return-absolute', 'children'),
    dash.dependencies.Output('amount_invested', 'children'),
    [dash.dependencies.Input('crypto-dropdown', 'value'),
    dash.dependencies.Input('time-period-dropdown', 'value'),
    dash.dependencies.Input('investment-amount', 'value'),
    dash.dependencies.Input('my-date-picker-range', 'start_date'), 
    dash.dependencies.Input('my-date-picker-range', 'end_date'),
    dash.dependencies.Input('staking-returns', 'value'),
    dash.dependencies.Input('staking-time-period-dropdown', 'value'),
    dash.dependencies.Input('dca-strategy-radio-items', 'value')
    ])

def update_line_graph(crypto, investment_period, investment, start_date, end_date, apr, rewards_freq, dca_strategy):
    #USD pairing as this has the most data
    FIAT = "USD"
    #Input the investment amount ($), investment period (Daily, Weekly, Monthly)
    prices = fd.get_crypto_price(crypto, FIAT, start_date, end_date)
    df, increment = dw.purchased_crypto(prices, apr, rewards_freq, investment, investment_period, dca_strategy)
    fv, final_date, min_pl, min_date, max_pl, max_date, min_pl_abs, max_pl_abs, total_invested = dw.final_stats(df)
    return generate_line_graph(df), fv, min_pl, min_date, max_pl, max_date, investment_period, increment, min_pl_abs, max_pl_abs, total_invested


if __name__ == '__main__':
    app.run_server(debug=True)
