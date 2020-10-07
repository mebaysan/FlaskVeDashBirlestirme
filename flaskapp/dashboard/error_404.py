import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

layout = dbc.Jumbotron(
    [
        html.H1("404!", className="display-3"),
        html.P(
            "Aradığınız Sayfa Bulunamadı! ",
            className="lead",
        ),
        html.Hr(className="my-2"),
        dcc.Link(dbc.Button("Anasayfa", style={'backgroundColor': '#6f42c1'}), className="lead",
                 href='/',refresh=True),
    ], style={'textAlign': 'center'}
)
