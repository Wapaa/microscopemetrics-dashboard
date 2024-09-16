import dash
import dash_mantine_components as dmc
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import Input, Output, callback, dash_table, dcc, html
from linkml_runtime.loaders import yaml_loader
from microscopemetrics_omero.load import load_image
from microscopemetrics_schema.datamodel.microscopemetrics_schema import (
    FieldIlluminationDataset,
)

from data_sources.tools import *

obj = yaml_loader.load(
    "/home/wapaa/projects/microscopemetrics-dashboard/src/data/examples/FieldIlluminationDataset-001 (3).yaml",
    target_class=FieldIlluminationDataset,
)

# ________________________________for test purposes_______________
url = "/home/wapaa/Downloads/chroma(1).npy"
np_im = np.load(url)
imaa = np_im[0, 0, :, :, 0] / 255


# _______________________________________________________________
imageId = 27627
conn = get_connection()
image_wrapper = conn.getObject("Image", imageId)
image_omero = load_image(image_wrapper)
imaaa = image_omero[0, 0, :, :, 0] / 255
roi_service = conn.getRoiService()
result = roi_service.findByImage(imageId, None)
date = image_wrapper.getDate()

# ______________________________________Data__________________________
# channel_list = [f"channel {i}" for i in range(0, image_omero.shape[4])]
channel_list = image_wrapper.getChannelLabels()
channel_list = ["( " + i + "nm )" + " Channel: " + str(j) for j, i in enumerate(channel_list)]

# roi_df = get_corner_rois(obj.output)
# rois = roi_df.ROI.to_list()
data = get_key_values(obj.output)
data_IP = get_intensity_profiles(obj.output)
ima = get_intensity_map_data(obj.output)
# points_df = get_center_of_illumination(obj.output)
# profile_rois_df = get_profile_rois(obj.output)
shapes_rectangle, shapes_line = get_rois_omero(result)
df_lines_omero = get_info_roi_lines(shapes_line)
df_rects_omero = get_info_roi_rectangles(shapes_rectangle)
map_ano = get_map_annotation(image_wrapper, conn)
# _____________________________________________________________________


dash.register_page(__name__)

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
                    [
                        dmc.Title("Intensity Map", color="#189A35", size="h3", mb=10),
                        dcc.Dropdown(channel_list, value=channel_list[0], id="channel-dropdown"),
                        dcc.RadioItems(
                            options=["Raw Image", "ROIS Image"],
                            value="Raw Image",
                            inline=True,
                            id="rois-radio",
                        ),
                        dcc.Graph(figure={}, id="rois-graph"),
                        dmc.Text(date, color="#189A35", size="lg", style={"margin-top": "20px"}),
                    ],
                    span=6,
                ),
                dmc.Col(
                    [
                        dmc.Title("Key Values", color="#189A35", size="h3", mb=10),
                        dash_table.DataTable(
                            id="table-multicol-sorting",
                            columns=[{"name": i, "id": i} for i in sorted(map_ano.columns)],
                            data=map_ano.to_dict("records"),
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
                    ],
                    span=6,
                ),
            ]
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Title("Intensity Profiles", color="#189A35", size="h3"),
                        dcc.Graph(figure=px.line(data_IP, markers=True)),
                    ],
                    span=6,
                ),
                dmc.Col(
                    [
                        dmc.Title("Intensity Profiles Table", color="#189A35", size="h3", mb=10),
                        dash_table.DataTable(
                            data_IP.to_dict("records"),
                            page_size=10,
                            style_table={"overflowX": "auto", "magin-top": "20px"},
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
                    ],
                    span=6,
                ),
            ]
        ),
    ],
    fluid=True,
)


@callback(
    Output(component_id="rois-graph", component_property="figure"),
    Input(component_id="channel-dropdown", component_property="value"),
    Input(component_id="rois-radio", component_property="value"),
)
def update_graph(
    channel,
    value,
):
    imaaa = image_omero[0, 0, :, :, int(channel[-1])]
    fig = px.imshow(imaaa, zmin=imaaa.min(), zmax=imaaa.max(), color_continuous_scale="gray")
    fig1 = px.imshow(imaaa, zmin=imaaa.min(), zmax=imaaa.max(), color_continuous_scale="hot")
    fig1 = add_rois(go.Figure(fig1), df_rects_omero)
    fig1 = add_profile_rois(go.Figure(fig1), df_lines_omero)
    if value == "Raw Image":
        return fig
    elif value == "ROIS Image":
        return fig1
    else:
        return fig


conn.close()
