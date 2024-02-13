import dash
import dash_mantine_components as dmc
import plotly.express as px
from dash import Input, Output, callback, dash_table, dcc, html
from dash_iconify import DashIconify
from microscopemetrics_omero.load import load_image

from data_sources.tools import *

dash.register_page(__name__, path="/layoutTemp/")

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv")

conn = get_connection()
list_GROUP = []

layout = dmc.Container(
    [
        dmc.Grid(
            children=[
                dmc.Col("test", span=4),
                dmc.Col(
                    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
                    span=4,
                ),
                dmc.Col(
                    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
                    span=4,
                ),
            ]
        ),
        dmc.Grid(
            children=[
                dmc.Col(
                    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
                    span=4,
                ),
                dmc.Col(
                    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
                    span=4,
                ),
                dmc.Col(
                    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
                    span=4,
                ),
            ]
        ),
        dmc.Grid(
            children=[
                dmc.Col(
                    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
                    span=4,
                ),
                dmc.Col(
                    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
                    span=4,
                ),
                dmc.Col(
                    dcc.Graph(figure=px.histogram(df, x="continent", y="lifeExp", histfunc="avg")),
                    span=4,
                ),
            ]
        ),
    ],
    fluid=True,
)
