import dash
from dash import html
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from microscopemetrics.strategies import strategies as st_mm

dash.register_page(__name__, path="/psf")


@given(dataset=st_mm.st_psf_beads_dataset())
@settings(max_examples=1, suppress_health_check=[HealthCheck.too_slow], deadline=10000)
def getPSF(dataset, list_data):
    list_data.append(dataset)


psf_data = []
getPSF(psf_data)
[_.run() for _ in psf_data]

layout = html.Div(
    [
        html.H1("This page is under construction"),
    ]
)
