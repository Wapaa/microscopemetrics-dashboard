from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(children=[
    html.H1("Hello Dash"),
    html.Div("Dash: A web application framework for Python.")
])
if __name__ == '__main__':
    app.run_server(debug=True)