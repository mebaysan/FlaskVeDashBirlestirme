from databaysansoft.dashboard.apps.covid19.app import layout as covid19_layout
from databaysansoft.dashboard.error_404 import layout as error_404
from databaysansoft.dashboard.apps.example.app import layout as example_layout
URL_PATHS = [
    {'path': '/dashboards/covid19', 'app_name': 'Covid19', 'layout': covid19_layout},
    {'path': '/dashboards/example', 'app_name': 'Example Güzel Oldu', 'layout': example_layout},
] # URL'leri burada set ediyoruz, otomatik olarak çekecek


def get_layout(pathname):
    for dct in URL_PATHS:
        if dct['path'] == pathname:
            return dct['layout']
    return error_404


def get_app_names():
    app_names = []
    for dct in URL_PATHS:
        app_names.append(dct['app_name'])
    return app_names


def get_paths():
    paths = []
    for dct in URL_PATHS:
        paths.append(dct['path'])
    return paths
