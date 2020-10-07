import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from flaskapp.dashboard.apps.covid19 import mydata


DF = mydata.get_data()

layout = html.Div(children=[
    dbc.Row(children=[
        dbc.Col(
            children=[html.H1("Sağlık Bakanlığı'na ait Covid19 API", style={'color': '#17a2b8', 'marginTop': '35px'})],
            xs=12, sm=12, md=8, xl=8, lg=8),
        dbc.Col(children=[
            html.Label('Tarih Aralığı Seçin', style={'fontSize': '20px', 'color': '#17a2b8'}),
            html.Br(),
            dcc.DatePickerRange(
                id='covid19-my-date-picker',
                min_date_allowed=datetime(DF['tarih'].min().year, DF['tarih'].min().month,
                                          DF['tarih'].min().day),
                max_date_allowed=datetime(DF['tarih'].max().year, DF['tarih'].max().month,
                                          DF['tarih'].max().day + 1),
                start_date=datetime(DF['tarih'].min().year, DF['tarih'].min().month,
                                    DF['tarih'].min().day),
                end_date=datetime(DF['tarih'].max().year, DF['tarih'].max().month,
                                  DF['tarih'].max().day),
                display_format='D/M/YYYY',
            ),
            html.Br(),
            dbc.Button(
                id='covid19-submit-button',
                n_clicks=0,
                children='Filtrele',
                style={'marginTop': '5px', 'backgroundColor': '#17a2b8', 'borderColor': '#FFFFFF'}
            )], xs=12, sm=12, md=4, xl=4, lg=4),

    ], style={'marginLeft': '5px'}),
    dbc.Row(children=[
        dbc.Col(children=[
            dbc.Row(children=[dbc.Col(children=[dcc.Graph(id='covid19-gunluk-chart')])]),
            dbc.Row(children=[
                dbc.Col(children=[dcc.Markdown(id='covid19-gunluk-ozet')], style={'textAlign': 'center'})]),
        ], lg=6, xl=6, md=12, sm=12, xs=12),
        dbc.Col(children=[
            dbc.Row(children=[dbc.Col(children=[dcc.Graph(id='covid19-toplam-chart')])]),
            dbc.Row(children=[
                dbc.Col(children=[dcc.Markdown(id='covid19-toplam-ozet')], style={'textAlign': 'center'})]),
        ], lg=6, xl=6, md=12, sm=12, xs=12),
    ], no_gutters=True, id='covid19-my-charts-row'),
    dbc.Row(children=[
        dbc.Col(children=[dbc.Button(
            id='covid19-open-toast',
            n_clicks=0,
            children='Dashboard Hakkında Bilgi Al',
            color='info',
        ), dbc.Toast(
            [html.P("Filtreleme sayesinde istediğiniz zaman aralığını seçebilirsiniz.",
                    className="mb-0"),
             html.P("Line'ların üzerine tıklayarak o güne ait özet bilgiye erişebilirsiniz.",
                    className="mb-0")],
            id="covid19-simple-toast",
            header="Dashboard Kullanım Bilgisi",
            icon="info",
            dismissable=True,
            is_open=False,
            style={"position": "fixed", "top": 0, "right": 0, "width": 350, 'zIndex': 1},
        )], style={'textAlign': 'right', 'marginRight': '10px'}),
    ], id='covid19-info-toast-row', no_gutters=True)
])


def gunluk_chart(start, end):
    filtered_df = DF.query(f'tarih >= "{start}"').query(f'tarih <= "{end}"')
    gunluk_column_names = ['gunluk_vaka', 'gunluk_vefat', 'gunluk_iyilesen']
    gunluk_traces = []
    for col_name in gunluk_column_names:
        gunluk_traces.append(
            go.Scatter(x=filtered_df['tarih'], y=filtered_df[col_name], mode='lines', name=col_name))
    layout = go.Layout(title='2 Tarih Arasında Türkiye Günlük Corona Verileri', yaxis={'title': 'Günlük Veriler'},
                       xaxis={'title': 'Tarih'}, hovermode='x unified')
    gunluk_chart = go.Figure(layout=layout, data=gunluk_traces)
    return gunluk_chart


def toplam_chart(start, end):
    filtered_df = DF.query(f'tarih >= "{start}"').query(f'tarih <= "{end}"')
    toplam_column_names = ['toplam_vaka', 'toplam_vefat', 'toplam_iyilesen']
    toplam_traces = []
    for col_name in toplam_column_names:
        toplam_traces.append(go.Scatter(x=filtered_df['tarih'], y=filtered_df[col_name], mode='lines', name=col_name))
    layout = go.Layout(title='2 Tarih Arasında Türkiye Toplam Corona Verileri', yaxis={'title': 'Toplam Veriler'},
                       xaxis={'title': 'Tarih'}, hovermode='x unified')
    toplam_chart = go.Figure(layout=layout, data=toplam_traces)
    return toplam_chart

def init_callbacks(app): # bütün callback'lerimizi bir fonksiyon altında topluyoruz, bu sayede parametre olarak gelen Dash uygulaması ile callback'lerimizi bind edebileceğiz
    @app.callback([Output('covid19-gunluk-chart', 'figure'), Output('covid19-toplam-chart', 'figure')],
                  Input('covid19-submit-button', 'n_clicks'),
                  [State('covid19-my-date-picker', 'start_date'), State('covid19-my-date-picker', 'end_date')])
    def callback(n_clicks, start_date, end_date):
        start = pd.to_datetime(datetime.strptime(start_date[:10], '%Y-%m-%d'))
        end = pd.to_datetime(datetime.strptime(end_date[:10], '%Y-%m-%d'))
        return gunluk_chart(start, end), toplam_chart(start, end)

    @app.callback(
        Output('covid19-gunluk-ozet', 'children'),
        Input('covid19-gunluk-chart', 'clickData')
    )
    def gunluk_hover(clickData):
        if not clickData == None:
            tarih = clickData['points'][0]['x']
            tarih = pd.to_datetime(tarih)
            filtered_df = DF.query(f'tarih == "{tarih}"')
            return f"""
    ### Tarih: {tarih.day}/{tarih.month}/{tarih.year}
    | Günlük Vaka   |      Günlük İyileşen      |  Günlük Vefat |
    |:----------:|:-------------:|:------:|
    | {filtered_df['gunluk_vaka'].sum()} |  {filtered_df['gunluk_iyilesen'].sum()} | {filtered_df['gunluk_vefat'].sum()} |
                    """

    @app.callback(
        Output('covid19-toplam-ozet', 'children'),
        Input('covid19-toplam-chart', 'clickData')
    )
    def toplam_hover(clickData):
        if not clickData == None:
            tarih = clickData['points'][0]['x']
            tarih = pd.to_datetime(tarih)
            filtered_df = DF.query(f'tarih == "{tarih}"')
            return f"""
        ### Tarih: {tarih.day}/{tarih.month}/{tarih.year}
        | Toplam Vaka   |      Toplam İyileşen      |  Toplam Vefat |
        |:----------:|:-------------:|:------:|:-------:|
        | {filtered_df['toplam_vaka'].sum()} |  {filtered_df['toplam_iyilesen'].sum()} | {filtered_df['toplam_vefat'].sum()} |
                        """

    @app.callback(
        Output("covid19-simple-toast", "is_open"),
        [Input("covid19-open-toast", "n_clicks")],
    )
    def open_toast(n):
        if n:
            return True
        return False
