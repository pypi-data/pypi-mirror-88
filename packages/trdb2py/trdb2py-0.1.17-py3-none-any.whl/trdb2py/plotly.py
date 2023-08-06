import pandas as pd
from datetime import datetime
import time
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from trdb2py.statistics import buildPNLWinRateInYears


def showAssetCandles(title: str, dfCandles: pd.DataFrame, columm: str = 'close', toImg: bool = False):
    fig = px.line(dfCandles, x='date', y=columm, title=title)

    if toImg:
        fig.show(renderer="png")
    else:
        fig.show()


def showHeatmap(df: pd.DataFrame, columns: list, valtype: str = '', valoff: float = 0.0):
    data = []

    for index, row in df.iterrows():
        data.append([])

        for col in columns:
            if valtype == 'abs':
                data[index].append(abs(row[col] + valoff))
            else:
                data[index].append(row[col])
    # print(data)

    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=columns,
        y=df['title']))

    fig.show()


def showHeatmapWinRateInYears(lstpnl: list, sortby: str = '', valtype: str = '', valoff: float = 0.0):
    ret = buildPNLWinRateInYears(lstpnl)
    columns = []

    df = ret[0]

    if sortby != '':
        df = ret[0].sort_values(by=sortby).reset_index(drop=True)

    for y in range(ret[1], ret[2] + 1):
        columns.append('y{}'.format(y))

    columns.append('total')

    # print(columns)

    showHeatmap(df, columns, valtype, valoff)
