import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

layout = html.Div(children=[
    dcc.Graph(id='example',
    figure=go.Figure(data=[go.Scatter(x=[1,2,3],y=[3,2,1],mode='lines')],layout=go.Layout(title='Example Chart')))
])
