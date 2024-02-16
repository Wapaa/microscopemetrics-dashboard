import json

import dash
import dash_ag_grid as dag
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Input, Output, callback, dash_table, dcc, html
from dash_iconify import DashIconify

# from microscopemetrics_schema import strategies as st_sch
from hypothesis import HealthCheck, given, settings
from microscopemetrics.strategies import strategies as st_mm
from microscopemetrics_omero.load import load_image

from data_sources.tools import *

dash.register_page(__name__, path="/key")
c1 = "#d8f3dc"
c2 = "#eceff1"
c3 = "#189A35"


@given(dataset=st_mm.st_field_illumination_dataset())
@settings(max_examples=2, suppress_health_check=[HealthCheck.too_slow], deadline=10000)
def getDataset(dataset, list_data):
    list_data.append(dataset)


list_data = []
getDataset(list_data)


[_["unprocessed_analysis"].run() for _ in list_data]
data = get_key_values_st(list_data, "channel")

valueWAs = list(list_data[0]["unprocessed_analysis"].output.key_values.__dict__.keys())


layout = dmc.Container(
    [
        dmc.Center(
            dmc.Text(
                "Field Of Illumination Dashboard",
                color="#189A35",
                mb=30,
                style={"margin-top": "20px", "fontSize": 40},
            )
        ),
        dmc.Grid(
            [
                dmc.Col(
                    dmc.Stack(
                        [
                            dmc.Text("Microscope", size="sm", weight=700),
                            dcc.Dropdown(["Microscope L", "Microscope B", "Microscope G"]),
                            dmc.Text("Type of Analysis", size="sm", weight=700),
                            dcc.Dropdown(["Field Of Illumination"]),
                            dmc.Text("Analysis", size="sm", weight=700),
                            dcc.Dropdown(["L", "B", "G"]),
                        ]
                    ),
                    span=2,
                    style={
                        "background-color": c2,
                        "margin-right": "10px",
                        "border-radius": "0.5rem",
                    },
                ),
                dmc.Col(
                    [
                        dmc.Stack(
                            [
                                dmc.Grid(
                                    [
                                        dmc.Col(
                                            [
                                                html.H3("Select Category"),
                                                dcc.Dropdown(valueWAs, id="key_dpd"),
                                            ],
                                            span="auto",
                                            style={"background-color": c2, "margin-right": "10px"},
                                        ),
                                        dmc.Col(
                                            [
                                                html.H3("Select Date"),
                                                dcc.DatePickerRange(
                                                    id="date_filter",
                                                    start_date_placeholder_text="Start Period",
                                                    end_date_placeholder_text="End Period",
                                                    start_date=data["Date Processed"].min(),
                                                    end_date=data["Date Processed"].max(),
                                                    min_date_allowed=data["Date Processed"].min(),
                                                    max_date_allowed=data["Date Processed"].max(),
                                                ),
                                            ],
                                            span="auto",
                                        ),
                                    ],
                                ),
                                dmc.Title(
                                    "Key Measurments for FOI", color="#189A35", size="h3", mb=10
                                ),
                                dash_table.DataTable(
                                    id="table",
                                    columns=[{"name": i, "id": i} for i in sorted(data.columns)],
                                    data=data.to_dict("records"),
                                    page_size=10,
                                    sort_action="native",
                                    sort_mode="multi",
                                    sort_as_null=["", "No"],
                                    sort_by=[{"column_id": "pop", "direction": "asc"}],
                                    editable=False,
                                    style_cell={
                                        "textAlign": "left",
                                        "fontSize": 10,
                                        "font-family": "sans-serif",
                                    },
                                    style_header={
                                        "backgroundColor": "#189A35",
                                        "fontWeight": "bold",
                                        "fontSize": 15,
                                    },
                                ),
                            ]
                        )
                    ],
                    span="auto",
                    style={
                        "background-color": c2,
                        "margin-right": "10px",
                        "border-radius": "0.5rem",
                    },
                ),
                dmc.Col(
                    [
                        dmc.Title("Decile 0 Plot through Time", color="#189A35", size="h3", mb=10),
                        dcc.Graph(
                            id="graph_line",
                            figure=px.line(
                                data,
                                x="Date Processed",
                                y="channel",
                                title="Decile 0 by Date Processed",
                                markers=True,
                            ).update_layout(clickmode="event+select"),
                        ),
                    ],
                    span="auto",
                    style={"background-color": "#eceff1", "border-radius": "5px"},
                ),
            ],
            justify="space-between",
            align="stretch",
            gutter="xl",
            style={
                "margin-top": "20px",
            },
        ),
        dmc.Grid(
            id="grido",
            justify="space-between",
            align="stretch",
            gutter="xl",
            style={
                "margin-top": "20px",
            },
        ),
        dmc.Grid(
            id="grido1",
            justify="space-between",
            align="stretch",
            gutter="xl",
            style={
                "margin-top": "20px",
                "margin-bottom": "10px",
            },
        ),
    ],
    fluid=True,
)


@callback(
    Output("grido", "children"),
    Output("grido1", "children"),
    # Input("cell-selection-double-click-callback", "selectedRows"),
    Input("graph_line", "clickData"),
    prevent_initial_call=True,
)
def display_cell_double_clicked_on(point):
    # print(type(c[0]['pointIndex']))
    ID = point["points"][0]["pointIndex"]
    style = {"background-color": c2, "border-radius": "0.5rem"}
    var = list_data[ID]["unprocessed_analysis"].output
    image = get_intensity_map_data(var)
    data = get_key_values(var)
    data_IP = get_intensity_profiles(var)
    fig = px.imshow(image, zmin=0, zmax=1, color_continuous_scale="gray")
    t = []
    t.append(dmc.Title("Intensity Map", color="#189A35", size="h3"))
    t.append(
        dmc.Grid(
            [
                dmc.Col([dcc.Dropdown(["Channel 1"])], span="auto"),
                dmc.Col([dcc.Dropdown(["Channel 1"])], span="auto"),
            ]
        )
    )
    t.append(dcc.Graph(figure=fig, id="rois-graph"))

    t1 = []
    t1.append(dmc.Title("Key Values", color="#189A35", size="h3"))
    t1.append(
        dash_table.DataTable(
            id="table-multicol-sorting",
            columns=[{"name": i, "id": i} for i in sorted(data.columns)],
            data=data.to_dict("records"),
            page_size=10,
            sort_action="native",
            sort_mode="multi",
            sort_as_null=["", "No"],
            sort_by=[{"column_id": "pop", "direction": "asc"}],
            editable=False,
            style_cell={
                "textAlign": "left",
                "fontSize": 10,
                "font-family": "sans-serif",
            },
            style_header={
                "backgroundColor": "#189A35",
                "fontWeight": "bold",
                "fontSize": 15,
            },
        ),
    )
    children1 = [
        dmc.Col(
            id="object_info",
            children=[dmc.Stack(id="map_image", children=t)],
            span=4,
            style={"background-color": c2, "border-radius": "0.5rem", "margin-right": "10px"},
        ),
        dmc.Col(
            id="object_info",
            children=[dmc.Stack(id="map_image", children=t1)],
            span="auto",
            style=style,
        ),
    ]
    children2 = [
        dmc.Col(
            [
                dmc.Title("Intensity Profiles", color="#189A35", size="h3"),
                dcc.Graph(figure=px.line(data_IP)),
            ],
            span=6,
            style={"background-color": c2, "border-radius": "0.5rem", "margin-right": "10px"},
        )
    ]
    return children1, children2


@callback(
    Output("graph_line", "figure"),
    Output("table", "data"),
    Input("date_filter", "start_date"),
    Input("date_filter", "end_date"),
    Input("key_dpd", "value"),
)
def update_line(start_date, end_date, key_dpd="channel"):
    data_new = get_key_values_st(list_data, key_dpd)
    data_fd = data_new[
        (data_new["Date Processed"] >= start_date) & (data_new["Date Processed"] <= end_date)
    ]
    line_graph = px.line(
        data_new, x="Date Processed", y=key_dpd, title=f"{key_dpd} by Date Processed", markers=True
    )
    print(key_dpd)
    return line_graph, data_new.to_dict("records")
