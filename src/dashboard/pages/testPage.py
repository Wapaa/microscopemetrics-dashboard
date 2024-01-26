import dash
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dash_table, dcc, html
from dash_iconify import DashIconify
from linkml_runtime.loaders import yaml_loader
from microscopemetrics_schema.datamodel.microscopemetrics_schema import (
    FieldIlluminationDataset,
)
from PIL import Image

obj = yaml_loader.load(
    "/home/wapaa/projects/microscopemetrics-dashboard/src/data/examples/FieldIlluminationDataset-001.yaml",
    target_class=FieldIlluminationDataset,
)


def get_intensity_profiles(var: FieldIlluminationDataset.output) -> pd.DataFrame:
    data_dict = var.intensity_profiles.columns
    dfs = [pd.DataFrame({key: value.values}) for key, value in data_dict.items()]
    df = pd.concat(dfs, axis=1)
    return df


def get_intensity_map_data(var: FieldIlluminationDataset.output) -> Image:
    list_ima = var.intensity_map.data
    x = var.intensity_map.shape_x
    y = var.intensity_map.shape_y
    ima = np.array(list_ima)
    pil_ima = Image.fromarray(ima.reshape([x, y]))
    return pil_ima


def get_key_values(var: FieldIlluminationDataset.output) -> pd.DataFrame:
    data_dict = var.key_values.__dict__
    data_dict = {
        key: value[0] if isinstance(value, list) and value else value
        for key, value in data_dict.items()
    }
    data_list = list(data_dict.items())
    df = pd.DataFrame(data_list, columns=["Key", "Value"])
    df.Key = df.Key.str.replace("_", " ").str.title()
    return df


data = get_key_values(obj.output)
data_IP = get_intensity_profiles(obj.output)
ima = get_intensity_map_data(obj.output)

dash.register_page(__name__)

layout = dmc.Container(
    [
        dmc.Center(
            dmc.Text(
                "Field Of Illumination Analysis",
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
                        dcc.Graph(
                            figure=px.imshow(ima, zmin=0.0, zmax=1.0, color_continuous_scale="hot")
                        ),
                    ],
                    span=6,
                ),
                dmc.Col(
                    [
                        dmc.Title("Key Values", color="#189A35", size="h3", mb=10),
                        dash_table.DataTable(data.to_dict("records"), page_size=10),
                    ],
                    span=6,
                ),
            ]
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Title("Intensity Profiles", color="#189A35", size="h3", mb=10),
                        dash_table.DataTable(
                            data_IP.to_dict("records"),
                            page_size=10,
                            style_table={"overflowX": "auto"},
                        ),
                    ],
                    span=6,
                ),
                dmc.Col([dcc.Graph(figure=px.line(data_IP))], span=6),
            ]
        ),
    ],
    fluid=True,
)
