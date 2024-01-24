import dash
import dash_mantine_components as dmc
from dash import Dash, dcc, html

app = Dash(__name__, use_pages=True)

app.layout = html.Div(
    [
        dmc.Navbar(
            p="md",  # providing medium padding all side
            fixed=False,  # Setting fixed to false
            width={"base": 300},  # Initial size of navbar ie. 300px
            hidden=True,  # we want to hide for smaller screen
            hiddenBreakpoint="md",  # after past medium size navbar will be hidden.
            height="100vh",  # providing height of navbar
            id="sidebar",
            children=[
                dmc.Anchor("Link1", href="/"),
                dmc.Anchor("Link2", href="testpage"),
                dmc.Anchor("Link3", href="/"),
                dmc.Anchor("Link4", href="/"),
            ],
        ),
        dash.page_container,
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
