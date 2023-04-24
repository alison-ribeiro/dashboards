import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime

import requests
import json

# import from folders/theme changer

from dash_bootstrap_templates import ThemeSwitchAIO

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]

app = dash.Dash(__name__, external_stylesheets=[FONT_AWESOME, dbc.themes.BOOTSTRAP])

app.scripts.config.serve_locally = True
server = app.server


# ========== Styles ============ #


main_config = {
    "hovermode": "x unified",
    "legend": {
        "yanchor": "top",
        "y": 0.9,
        "xanchor": "right",
        "x": 0.2,
        "title": {"text": None},
        "font": {"color": "white"},
        "bgcolor": "rgba(0,0,0,0.5)",
    },
    "margin": {"l": 10, "r": 10, "t": 0, "b": 10},
}

config_graph = {"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY


orders = []
page = 1
while True:
    url = f"https://bling.com.br/Api/v2/pedidos/page={page}/json/"
    params = {
        "apikey": "9e4f7df3bcb41a13ed8746d50556e66cf16af5fe3a48e62f4704e7d86230acd724814239"
    }
    response = requests.get(url, params=params)
    json_data = json.loads(response.text)
    if (
        "retorno" in json_data
        and "pedidos" in json_data["retorno"]
        and json_data["retorno"]["pedidos"]
    ):
        for order in json_data["retorno"]["pedidos"]:
            order_data = {
                "numero": order["pedido"]["numero"],
                "data": order["pedido"]["data"],
                "cliente": order["pedido"]["cliente"]["nome"],
                "valor": order["pedido"]["totalvenda"],
                "situacao": order["pedido"]["situacao"],
            }
            if "tipoIntegracao" in order["pedido"]:
                order_data["tipoIntegracao"] = order["pedido"]["tipoIntegracao"]
            else:
                order_data["tipoIntegracao"] = None
            orders.append(order_data)
        page += 1
    else:
        break

df = pd.DataFrame(orders)

df["valor"] = df["valor"].astype(float)

df = df.loc[df["situacao"] == "Atendido"]


df = df.copy()

soma_total = df.groupby("cliente")["valor"].sum()
df_cru = df.copy()
df_cru.loc[df_cru["cliente"] == "Consumidor Final", "cliente"] = "Lojinha"
df_cru.loc[df_cru["tipoIntegracao"] == "WooCommerceWH", "cliente"] = "Site"
df_cru.loc[df_cru["cliente"] == "Venda Externa", "cliente"] = "Venda Mauricio"
df_cru.loc[df_cru["situacao"] != "Cancelado", "situacao"] = 1

df_cru["data"] = pd.to_datetime(df_cru["data"])
df_cru["dia"] = df_cru["data"].dt.day
df_cru["mes"] = df_cru["data"].dt.month
df_cru["ano"] = df_cru["data"].dt.year

data_atual = datetime.date.today()

mes_atual = data_atual.month
dia_atual = data_atual.day

df_graph3 = df_cru.copy()
df_graph2 = df_cru.copy()
data_atual = datetime.date.today()

# filtrar a tabela pelo mês e dia atual
pedidos_hoje = df_cru.query("mes == @data_atual.month and dia == @data_atual.day")

# verificar se há informações para evitar erros
if len(pedidos_hoje) == 0:
    valor_total = 0
else:
    valor_total = pedidos_hoje["valor"].sum()


df_graph1 = df_cru.groupby(["cliente", "dia", "mes"])["valor"].sum().reset_index()


options_month = [{"label": "Ano todo", "value": 0}]

for element in df_cru["mes"]:
    options_month.append({"label": element, "value": element})


options_month = list(set([tuple(d.items()) for d in options_month]))
options_month = [dict(d) for d in options_month]
options_month = sorted(options_month, key=lambda x: x["value"])


fig6 = go.Figure()
fig6.add_trace(
    go.Indicator(
        mode="number+delta",
        title={"text": "Valor de venda por dia"},
        value=valor_total,
        number={"prefix": "R$", "font": {"size": 48}},
        delta={
            "relative": True,
            "valueformat": ".1%",
            "reference": df_cru["valor"].mean(),
        },
    )
)

fig6.update_layout(
    height=200,  # Definir a altura total do gráfico
)


def convert_to_text(month):
    lista1 = [
        "Ano Todo",
        "Janeiro",
        "Fevereiro",
        "Março",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    return lista1[month]


# =========  Layout  =========== #
app.layout = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.Legend(
                                                                    "Análise  de Vendas"
                                                                )
                                                            ],
                                                            width=12,
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        html.Button("Atualizar Página"),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dcc.Graph(
                                                                    figure=fig6,
                                                                    className="dbc",
                                                                    config=config_graph,
                                                                )
                                                            ],
                                                            style={"heigth": "100%"},
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    width=2,
                    style={"heigth": "100%"},
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dcc.Graph(
                                                            id="graph1",
                                                            className="dbc",
                                                            config=config_graph,
                                                        )
                                                    ]
                                                ),
                                            ],
                                            style={"heigth": "100%"},
                                        ),
                                    ],
                                    style={"heigth": "100%"},
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dcc.Graph(
                                                            id="graph2",
                                                            className="dbc",
                                                            config=config_graph,
                                                        )
                                                    ]
                                                ),
                                            ],
                                            style={"heigth": "100%"},
                                        ),
                                    ],
                                    style={"heigth": "100%"},
                                ),
                            ]
                        ),
                    ],
                    width=8,
                    style={
                        "padding-left": "3px",
                        "padding-right": "3px",
                        "heigth": "100%",
                    },
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [html.Legend("Escolha um mês")],
                                                    width=12,
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.RadioItems(
                                                    id="radio-meses",
                                                    options=options_month,
                                                    value=mes_atual,
                                                    inline=True,
                                                    labelCheckedClassName="text-success",
                                                    inputCheckedClassName="border border-success bg-success",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    width=2,
                    style={
                        "padding-left": "0",
                        "padding-right": "2px",
                        "height": "100%",
                    },
                ),
            ]
        ),
    ],
    fluid=True,
    style={"height": "100vh"},
)


@app.callback(
    Output("graph1", "figure"),
    Input("radio-meses", "value"),
)
def garfico1(mes_selecionado):
    # Filtrar o DataFrame pelo mês selecionado

    df_filtrado = df_graph1[df_graph1["mes"] == mes_selecionado]

    # Criar uma nova figura do gráfico com os dados filtrados

    fig_filtrado = go.Figure()

    for cliente in df_filtrado["cliente"].unique():
        data = df_filtrado[df_filtrado["cliente"] == cliente]
        fig_filtrado.add_trace(
            go.Scatter(
                x=data["dia"],
                y=data["valor"],
                mode="lines+markers+text",  # Adicionar o modo de exibição de texto
                # Adicionar o valor como texto em cada ponto
                text=[f"R${round(valor, 2):.2f}" for valor in data["valor"]],
                textposition="top center",  # Definir a posição do texto
                name=cliente,
            )
        )

    # Atualizar o layout do gráfico com o mês selecionado
    fig_filtrado.update_layout(
        main_config,
        height=300,
    )

    return fig_filtrado


@app.callback(
    Output("graph2", "figure"),
    Input("radio-meses", "value"),
)
def garfico2(mes_selecionado):
    df_graph2["mes"] = pd.to_datetime(df_graph2["data"]).dt.month
    df_by_month_and_client = (
        df_graph2.groupby(["mes", "cliente"])["valor"].sum().reset_index()
    )
    garfico2 = go.Figure()
    for cliente in df_by_month_and_client["cliente"].unique():
        sub_df = df_by_month_and_client[df_by_month_and_client["cliente"] == cliente]
        garfico2.add_trace(
            go.Bar(
                x=sub_df["mes"],
                y=sub_df["valor"],
                name=cliente,
                text=["R$ " + str(round(x, 2)) for x in sub_df["valor"]],
                textposition="auto",
            )
        )
    garfico2.update_layout(
        title="Gastos Mensais dos Clientes",
        xaxis_tickformat="%m/%Y",
        yaxis_title="Valor Total",
        yaxis=dict(tickprefix="R$ "),
    )
    return garfico2


if __name__ == "__main__":
    app.run_server(debug=True, port=8054)
