from datetime import datetime, timedelta
from random import randrange

import numpy as np
import omero
import pandas as pd
import plotly.graph_objs as go
from microscopemetrics_schema.datamodel.microscopemetrics_schema import (
    FieldIlluminationDataset,
)
from omero.gateway import BlitzGateway
from PIL import Image


def get_key_values_st(list_data):
    data = []
    d1 = datetime.strptime("1/1/2000 1:30 PM", "%m/%d/%Y %I:%M %p")
    d2 = datetime.strptime("1/1/2024 4:50 AM", "%m/%d/%Y %I:%M %p")
    cols = ["ID", "Object", "Channels", "Date Processed"]
    cols.extend(list(list_data[0]["unprocessed_analysis"].output.key_values.__dict__.keys()))
    for j, i in enumerate(list_data):
        var = i["unprocessed_analysis"].output
        values = list(var.key_values.__dict__.values())
        stff = "Object " + str(j)
        n = len(var.key_values.channel)
        row = [j, stff, n, random_date(d1, d2)]
        row.extend(values)
        data.append(row)
    df = pd.DataFrame(data, columns=cols)
    return df


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def info_row(obj):
    row = [obj.getId(), obj.OMERO_CLASS, obj.getName(), obj.getOwnerOmeName()]
    return row


def get_info_dash(conn):
    my_exp_id = conn.getUser().getId()
    default_group_id = conn.getEventContext().groupId
    list_PROJECTS = []
    list_DATASETS = []
    list_IMAGE = []
    for project in conn.getObjects("Project"):
        list_PROJECTS.append(info_row(project))
        for dataset in project.listChildren():
            list_DATASETS.append(info_row(dataset))
            for image in dataset.listChildren():
                list_IMAGE.append(info_row(image))
    df_project = pd.DataFrame(list_PROJECTS, columns=["ID", "OMERO_CLASS", "Name", "Owner"])
    df_dataset = pd.DataFrame(list_DATASETS, columns=["ID", "OMERO_CLASS", "Name", "Owner"])
    df_image = pd.DataFrame(list_IMAGE, columns=["ID", "OMERO_CLASS", "Name", "Owner"])

    return df_project, df_dataset, df_image


# ________________________________Connection_____________________


def get_connection(
    HOST="omero.mri.cnrs.fr",
    PORT=4064,
    USERNAME="odhmine",
    PASSWORD="Wa!na!pa@1",
    GROUP="microscope-metrics",
):
    conn = BlitzGateway(USERNAME, PASSWORD, group=GROUP, port=PORT, host=HOST)
    conn.connect()
    return conn


# ________________________________Functions_______________________


def get_profile_rois(var: FieldIlluminationDataset.output) -> pd.DataFrame:
    data_dict = var.roi_profiles.shapes
    data = [[key, value.x1, value.y1, value.x2, value.y2] for key, value in data_dict.items()]
    df = pd.DataFrame(data, columns=["ROI", "X1", "Y1", "X2", "Y2"])
    df.ROI = df.ROI.str.replace("_", " ", regex=True)
    df.ROI = df.ROI.str.title()
    return df


def get_microscope_list(conn):
    data = []
    for g in conn.getGroupsMemberOf():
        data.append([g.getName(), g.getId()])
    df = pd.DataFrame(data, columns=["Name", "Id"])
    return df


def get_projects_list(conn, group_id):
    data = []
    for project in conn.getObjects("Project", opts={"group": group_id}):
        data.append([project.getName(), project.getId()])
    df = pd.DataFrame(data, columns=["Name", "Id"])
    return df


def get_center_of_illumination(var: FieldIlluminationDataset.output) -> pd.DataFrame:
    data_dict = var.center_of_illumination["Centers of illumination"].shapes
    data = [[key, value.x, value.y] for key, value in data_dict.items()]
    df = pd.DataFrame(data, columns=["Point", "X", "Y"])
    return df


def get_corner_rois(var: FieldIlluminationDataset.output) -> pd.DataFrame:
    data_dict = var.roi_corners.shapes
    data = [[key, value.x, value.y, value.w, value.h] for key, value in data_dict.items()]
    df = pd.DataFrame(data, columns=["ROI", "X", "Y", "W", "H"])
    df.ROI = df.ROI.str.replace("_", " ", regex=True)
    df.ROI = df.ROI.str.title()
    return df


def get_intensity_profiles(var: FieldIlluminationDataset.output) -> pd.DataFrame:
    data_dict = var.intensity_profiles.columns
    dfs = [pd.DataFrame({key: value.values}) for key, value in data_dict.items()]
    df = pd.concat(dfs, axis=1)
    return df


def get_intensity_map_data(var: FieldIlluminationDataset.output) -> Image:
    # TZYXC
    list_ima = var.intensity_map.data
    x = var.intensity_map.shape_x
    y = var.intensity_map.shape_y
    z = var.intensity_map.shape_z
    t = var.intensity_map.shape_t
    c = var.intensity_map.shape_c
    ima = np.array(list_ima).reshape([t, z, y, x, c])
    # pil_ima = Image.fromarray(ima1)
    return ima


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


def add_rois(fig: go.Figure, df: pd.DataFrame) -> go.Figure:
    for i, row in df.iterrows():
        fig.add_shape(
            go.layout.Shape(
                type="rect",
                x0=row.X,
                y0=row.Y,
                x1=row.X + row.W,
                y1=row.Y + row.H,
                xref="x",
                yref="y",
                line=dict(
                    color="RoyalBlue",
                    width=3,
                ),
            )
        )
    return fig


def add_profile_rois(fig: go.Figure, df: pd.DataFrame) -> go.Figure:
    for i, row in df.iterrows():
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=row.X1,
                y0=row.Y1,
                x1=row.X2,
                y1=row.Y2,
                xref="x",
                yref="y",
                line=dict(
                    color="Green",
                    width=1,
                    dash="dot",
                ),
            )
        )
    return fig


# _____________________________________________________________________
def get_rois_omero(result):
    shapes_line = {}
    shapes_rectangle = {}
    for roi in result.rois:
        for s in roi.copyShapes():
            shape = {}
            shape["id"] = s.getId().getValue()
            shape["theT"] = s.getTheT().getValue()
            shape["theZ"] = s.getTheZ().getValue()
            if s.getTextValue():
                shape["textValue"] = s.getTextValue().getValue()
            if s.__class__.__name__ == "RectangleI":
                shape["type"] = "Rectangle"
                shape["x"] = s.getX().getValue()
                shape["y"] = s.getY().getValue()
                shape["w"] = s.getWidth().getValue()
                shape["h"] = s.getHeight().getValue()
                shapes_rectangle[s.getId().getValue()] = shape
            elif s.__class__.__name__ == "EllipseI":
                shape["type"] = "Ellipse"
                shape["cx"] = s.getCx().getValue()
                shape["cy"] = s.getCy().getValue()
                shape["rx"] = s.getRx().getValue()
                shape["ry"] = s.getRy().getValue()
            elif s.__class__.__name__ == "PointI":
                shape["type"] = "Point"
                shape["cx"] = s.getCx().getValue()
                shape["cy"] = s.getCy().getValue()
            elif s.__class__.__name__ == "LineI":
                shape["type"] = "Line"
                shape["x1"] = s.getX1().getValue()
                shape["x2"] = s.getX2().getValue()
                shape["y1"] = s.getY1().getValue()
                shape["y2"] = s.getY2().getValue()
                shapes_line[s.getId().getValue()] = shape
            elif s.__class__.__name__ == "MaskI":
                shape["type"] = "Mask"
                shape["x"] = s.getX().getValue()
                shape["y"] = s.getY().getValue()
                shape["w"] = s.getWidth().getValue()
                shape["h"] = s.getHeight().getValue()
            elif s.__class__.__name__ == "PolygonI":
                continue
    return shapes_rectangle, shapes_line


def get_info_roi_lines(shape_dict):
    data = [
        [key, value["x1"], value["y1"], value["x2"], value["y2"]]
        for key, value in shape_dict.items()
    ]
    df = pd.DataFrame(data, columns=["ROI", "X1", "Y1", "X2", "Y2"])
    return df


def get_info_roi_rectangles(shape_dict):
    data = [
        [key, value["x"], value["y"], value["w"], value["h"]] for key, value in shape_dict.items()
    ]
    df = pd.DataFrame(data, columns=["ROI", "X", "Y", "W", "H"])
    return df


def get_map_annotation(image_wrapper, conn):
    df = None
    for i in image_wrapper.listAnnotations():
        if i.__class__.__name__ == "MapAnnotationWrapper":
            keyPairs = conn.getObject("MapAnnotation", i.getId())
            table = dict(keyPairs.getValue())
            df = pd.DataFrame(table.items(), columns=["Key", "Value"])
    return df


"""    df.columns = df.columns.str.replace("ch\d{2}_", "", regex=True)
    df.columns = df.columns.str.replace("_", " ", regex=True)
    df.columns = df.columns.str.title()"""
