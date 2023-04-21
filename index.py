import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc


from app import *

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Análise  de Vendas")
                        ]),
                        dbc.Col([
                            html.I(className='fa fa-chart-line',
                                   style={'font-size': '300%'})
                        ]),
                    ]),
                    dbc.Row([
                        html.Button('Atualizar Página', id='btn-refresh'),
                        dcc.Location(id='url', refresh=False)
                    ]),
                ]),
            ]),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Vendas por dia")
                        ]),
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc')
                        ]),
                    ]),
                ]),
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Análise  de Vendas")
                        ]),
                        dbc.Col([
                            html.I(className='fa fa-chart-line',
                                   style={'font-size': '300%'})
                        ]),
                    ]),
                    dbc.Row([
                        html.Button('Atualizar Página'),

                    ]),
                ]),
            ]),
        ], width=3),
    ])
], fluid=True, style={'height': '100vh'})


@app.callback(
    Output('url', 'pathname'),
    Input('btn-refresh', 'n_clicks'),
    State('url', 'pathname')
)
def refresh_page(n_clicks, pathname):
    if n_clicks is not None:
        return pathname + '?refresh=' + str(n_clicks)
    return pathname


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
