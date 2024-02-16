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
list_GROUP = get_microscope_list(conn)
l = list_GROUP.Id.to_list()

layout = dmc.Container(
    [
        dmc.Grid(
            children=[
                dmc.Col(
                    [
                        dcc.Dropdown(l, value=l[0], id="group_id", style={"width": "75%"}),
                        dcc.Dropdown(id="project_id", style={"width": "75%"}),
                    ],
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                        "margin-bottom": "20px",
                    },
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


@callback(Output("project_id", "options"), Input("group_id", "value"))
def update_project_id(group_id):
    conn = get_connection()
    list_PROJECT = get_projects_list(conn, group_id)
    l = list_PROJECT.Id.to_list()
    conn.close()
    return [{"label": i, "value": i} for i in l]
