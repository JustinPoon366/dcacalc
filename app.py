import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
app.title = 'Crypto Dollar Cost Calculator'
server = app.server
app.config.suppress_callback_exceptions = True