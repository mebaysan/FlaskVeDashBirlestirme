import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from flaskapp.dashboard.apps.covid19.app import init_callbacks as covid19_callbacks
from flaskapp.dashboard.layout import html_layout
from flaskapp.dashboard.urls import get_app_names, get_paths,get_layout


def init_dashboard(server): # Dash uygulaması oluşturmak için bir fonksiyon yazıyoruz, parametre olarak üzerinde çalışacağı server'i alacak (Flask'ı yollayacağız)
    app = dash.Dash(server=server, # __init__.py içerisinde bu fonksiyonu çağırırken orada oluşturduğumuz Flask uygulamasını parametre olarak yollayacağız
                    routes_pathname_prefix='/dashboards/',  # Dash uygulamamızın kök url'i
                    external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.index_string = html_layout
    covid19_callbacks(app) # covid19 dashboard'ında kullanılan callback'leri bu Dash app'i ile bind ediyoruz
    app.layout = html.Div([
        init_navbar(),
        dcc.Location(id='url',
                     refresh=False,

                     ),
        html.Div(id='page-content')
    ])

    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        return get_layout(pathname)

    return app.server


def init_navbar():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Anasayfa", href="/", external_link=True)),
            dbc.DropdownMenu(
                children=init_navbar_items(),
                nav=True,
                in_navbar=True,
                label="Dashboard'lar",
            ),
        ],
        brand="Açık Kaynak Veri Portalı",
        brand_href="/",
        brand_external_link=True,
        color="rgb(111, 66, 193)",
        dark=True,
    )


def init_navbar_items():
    items = [dbc.DropdownMenuItem("Dashboard'lar", header=True)]
    for (name, path) in zip(get_app_names(), get_paths()):
        items.append(dbc.DropdownMenuItem(name, href=f"{path}"))
    return items
