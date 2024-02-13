import dash
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

style = {
    "background": "white",
    "padding": "20px",
    "width": "300px",
    "border": "solid 0.5px #e0e0e0",
    "border-radius": "5px",
    "box-shadow": "0 6px 20px 0 rgba(0, 0, 0, 0.19)",
}
dash.register_page(__name__)

layout = (
    dmc.Container(
        dmc.Center(
            dmc.Stack(
                children=[
                    dmc.TextInput(
                        label="Your Server:",
                        style={"width": 200},
                        icon=DashIconify(icon="ic:round-computer"),
                    ),
                    dmc.TextInput(
                        label="Your Email:",
                        style={"width": 200},
                        icon=DashIconify(icon="ic:email"),
                    ),
                    dmc.TextInput(
                        label="Your Password:",
                        style={"width": 200},
                        icon=DashIconify(icon="ic:round-lock"),
                        type="password",
                    ),
                    dmc.Button(
                        "Submit",
                        color="blue",
                        style={"width": 200},
                    ),
                ],
                style=style,
                align="center",
                spacing="xl",
            )
        )
    ),
)
