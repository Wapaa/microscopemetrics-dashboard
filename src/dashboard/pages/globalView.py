import dash
import dash_mantine_components as dmc
import plotly.express as px
from dash import Input, Output, callback, dash_table, dcc, html
from dash_iconify import DashIconify
from microscopemetrics_omero.load import load_image

from data_sources.tools import *

conn = get_connection()
df_project, df_dataset, df_image = get_info_dash(conn)
test_text = (
    conn.getUser().getFullName()
    + " has acces to "
    + str(len(df_project))
    + " project(s), "
    + str(len(df_dataset))
    + " dataset(s) and "
    + str(len(df_image))
    + " image(s)"
)


dash.register_page(__name__, path="/globalView")

style = {
    "background": "white",
    "padding": "20px",
    "width": "300px",
    "border": "solid 0.5px #e0e0e0",
    "border-radius": "5px",
    "box-shadow": "0 6px 20px 0 rgba(0, 0, 0, 0.19)",
}

layout = (
    dmc.Container(
        [
            dmc.Grid(
                children=[
                    dmc.Col(
                        dmc.Card(
                            children=[
                                dmc.CardSection(dmc.Image(src="/assets/images/photo.jpeg")),
                                dmc.Group(
                                    [
                                        dmc.Text("Experimenter Info Card", weight=500),
                                        dmc.Badge(
                                            conn.getUser().getFullName(),
                                            color="red",
                                            variant="light",
                                        ),
                                    ],
                                    position="apart",
                                    mt="md",
                                    mb="xs",
                                ),
                                dmc.Text(
                                    test_text,
                                    size="sm",
                                    color="dimmed",
                                ),
                                dmc.Button(
                                    "More Info",
                                    variant="light",
                                    color="blue",
                                    fullWidth=True,
                                    mt="md",
                                    radius="md",
                                ),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 350},
                        ),
                        span=4,
                    ),
                    dmc.Col(
                        [
                            dmc.Stack(
                                children=[
                                    dmc.Title("Available Projects", color="#189A35", size="h3"),
                                    dash_table.DataTable(
                                        df_project.to_dict("records"),
                                        page_size=10,
                                        style_table={"overflowX": "auto", "magin-top": "20px"},
                                    ),
                                    dmc.Title("Available Datasets:", color="#189A35", size="h3"),
                                    dash_table.DataTable(
                                        df_dataset.to_dict("records"),
                                        page_size=10,
                                        style_table={"overflowX": "auto", "magin-top": "20px"},
                                    ),
                                    dmc.Title("Available Images:", color="#189A35", size="h3"),
                                    dash_table.DataTable(
                                        df_image.to_dict("records"),
                                        page_size=10,
                                        style_table={"overflowX": "auto", "magin-top": "20px"},
                                    ),
                                ]
                            ),
                        ],
                        span=8,
                    ),
                ]
            ),
            dmc.Stack(
                [
                    html.P("Search Image by ID"),
                    dcc.Input(
                        id="imageid",
                        type="number",
                        value=27627,
                        debounce=True,
                        min=0,
                        max=100000,
                        step=1,
                        style={"width": 200},
                    ),
                    dmc.Title("Visualise Image", color="#189A35", size="h3", mb=10),
                    dcc.Dropdown(
                        id="channelId", options={}, value="Channel 0", style={"width": 200}
                    ),
                    dcc.Graph(figure={}, id="image_graph"),
                ]
            ),
        ],
        fluid=True,
    ),
)


@callback(
    Output(component_id="image_graph", component_property="figure"),
    Output(component_id="channelId", component_property="options"),
    Input(component_id="imageid", component_property="value"),
    Input(component_id="channelId", component_property="value"),
)
def update_graph_id(value=27627, channel="channel 0"):
    conn = get_connection()
    image_wrapper = conn.getObject("Image", value)
    image_omero = load_image(image_wrapper)
    print(channel)
    channel_list = [f"channel {i}" for i in range(0, image_omero.shape[4])]
    print(image_omero.shape)
    imaaa = image_omero[0, 0, :, :, int(channel[-1])] / 255
    fig = px.imshow(imaaa, zmin=0, zmax=1, color_continuous_scale="gray")
    return fig, channel_list


conn.close()
