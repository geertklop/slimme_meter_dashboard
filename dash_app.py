import pandas as pd
import datetime
import sqlite3
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                external_stylesheets=external_stylesheets)



app.layout = html.Div(
    html.Div([
        html.H2('Energieverbuik per 5 minuten', style={'text-align':'center'}),
        dcc.Graph(id='live-update-daily-total'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval = 300000,
            n_intervals = 0
        )
    ])
)


@app.callback(Output('live-update-daily-total', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_daily_total(n):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    first_of_month = datetime.datetime(current_year,
                                       current_month,
                                       1
                                       )
    # fetch data from database
    db = sqlite3.connect('/home/gklop/slimme_meter_project/data/meterdata.db')
    df = pd.read_sql_query("select * from meterstanden where currentdate >= '{}';".format(first_of_month), db)

    #grab minimum values of day
    verbruik_dag = df.groupby(df['currentdate'].dt.date())['verbruik_delta'].sum().reset_index()
    terug_dag = df.groupby(df['currentdate'].dt.date())['terug_delta'].sum().reset_index()

    data = verbruik_dag.merge(terug_dag, how='left', on='currentdate')

    traces = []
    for i in ['verbruik_dag', 'terug_dag']:
        traces.append(go.Bar(
            x=data['currentdate'],
            y=df[i],
            text=df[i],
            name=i
        ))

    return {'data': traces,
            'layout': go.Layout(
                barmode='group',
                xaxis=dict(title=''),
                yaxis=dict(title='verbruik in kWh')
            )
            }


@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    first_of_month = datetime.datetime(current_year,
                                       current_month,
                                       1
                                       )
    # fetch data from database
    db = sqlite3.connect('/home/gklop/slimme_meter_project/data/meterdata.db')
    df = pd.read_sql_query("select * from meterstanden where currentdate >= '{}';".format(first_of_month), db)

    traces = []
    for i in ['verbruik_delta', 'terug_delta']:
        traces.append(go.Scatter(
            x=df['currentdate'],
            y=df[i],
            text=df[i],
            mode='lines',
            name=i
        ))

    return {'data': traces,
            'layout': go.Layout(
                xaxis=dict(title=''),
                yaxis=dict(title='verbruik in kWh'),
                hovermode='closest'
            )
            }


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8050)










