from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


from app import app
from app import server

from apps import app1, app2

navbar = dbc.Navbar(
    dbc.Container(
        [
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.CardImg(src="assets/images/increase.png", style = {"height" : "30 px","width":"50px"})),
                    dbc.Col(dbc.NavbarBrand("Crypto Dollar Cost Average Calculator", className="ms-2")),
                ],
                align="center",
                className="g-0",
            ),
            dbc.Row([
                dbc.Col(),
                dbc.Col(
                    dbc.NavItem(
                        dbc.NavLink(
                            dcc.Link('DCA Calculator', href='/', style={"color":"black", "text-decoration": "none"})
                            )
                        )
                    ),
                dbc.Col(dbc.NavItem(
                    dbc.NavLink(
                        dcc.Link('Why DCA?', href='/contact', style={"color":"black", "text-decoration": "none"})
                        )
                    )
                ),
            ], className="w-50"
            )
        
        ]
    ),
    color="light",
    dark=False,
)
# navbar = dbc.Navbar(
#     children=[
#         dbc.CardImg(src="assets/images/bill.png", style = {"height" : "30 px","width":"50px"}),
#         dbc.NavItem(dbc.NavLink(dcc.Link('DCA Calculator', href='/', style={"color":"black", "text-decoration": "none"}))),
#         dbc.NavItem(dbc.NavLink(dcc.Link('Why DCA?', href='/contact', style={"color":"black", "text-decoration": "none"}))),
#     ],
#     brand="Crypto Dollar Cost Average Calculator",
#     brand_href="#",
#     color="light",
#     dark=False,
# )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
    navbar,
    ]),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return app1.layout
    elif pathname == '/contact':
        return app2.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)