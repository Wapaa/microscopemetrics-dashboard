import dash
import dash_mantine_components as dmc
from dash import Dash, html
from dash_iconify import DashIconify

external_stylesheets = [dmc.theme.DEFAULT_COLORS]


def get_icon(icon):
    return DashIconify(icon=icon, height=24)


app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    use_pages=True,
    suppress_callback_exceptions=True,
)


app.layout = html.Div(
    [
        html.Div(
            [
                dmc.Center(dmc.Image(src="/assets/images/logo.png", alt="logo", width=200)),
                dmc.Center(
                    dmc.Text(
                        "Microscope Metrics Dashboard",
                        color="#189A35",
                        weight=700,
                        size="lg",
                        style={"margin-bottom": "20px"},
                    )
                ),
                dmc.NavLink(
                    label="Dashboard",
                    icon=get_icon(icon="material-symbols:dashboard-outline"),
                    href="/testpage",
                ),
                dmc.NavLink(
                    label="User View", icon=get_icon(icon="tabler:gauge"), href="/globalView"
                ),
                dmc.NavLink(
                    label="Unnamed",
                    icon=get_icon(icon="bi:house-door-fill"),
                    href="/underconstruction",
                ),
                dmc.NavLink(
                    label="Unnamed",
                    icon=get_icon(icon="tabler:gauge"),
                    href="/underconstruction",
                ),
            ],
            style={
                "width": "18%",
                "background": "white",
                "height": "100vh",
                "display": "inline-block",
                "border-right": "solid 1px #e0e0e0",
            },
        ),
        html.Div(
            [dash.page_container],
            style={
                "width": "80%",
                "height": "100vh",
                "margin-left": "2px",
                "display": "inline-block",
                "background": "white",
            },
        ),
    ],
    style={"display": "flex", "justify-content": "space-between", "margin-bottom": "20px"},
)

if __name__ == "__main__":
    app.run(debug=True, host="10.6.12.32")
