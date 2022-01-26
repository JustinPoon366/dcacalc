from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


from app import app
from app import server

from apps import app1, app2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
    dcc.Link('Core App|', href='/apps/app1'),
    dcc.Link('Other Apps', href='/apps/app2'),
        ], className="row"),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)