import pandas as pd
from datetime import datetime
import time
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from trdb2py.statistics import buildPNLWinRateInYears, buildPNLListWinRateInYears2, buildPNLWinRateInMonths, buildPNLListWinRateInMonths2


def showAssetCandles(title: str, dfCandles: pd.DataFrame, columm: str = 'close', toImg: bool = False):
    fig = px.line(dfCandles, x='date', y=columm, title=title)

    if toImg:
        fig.show(renderer="png")
    else:
        fig.show()


def showHeatmap(df: pd.DataFrame, columns: list, valtype: str = '', valoff: float = 0.0, toImg: bool = False):
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

    if toImg:
        fig.show(renderer="png")
    else:
        fig.show()


def showHeatmapWinRateInYears(lstpnl: list, sortby: str = '', valtype: str = '', valoff: float = 0.0, toImg: bool = False):
    ret = buildPNLWinRateInYears(lstpnl)
    columns = []

    df = ret[0]

    if sortby != '':
        df = ret[0].sort_values(by=sortby).reset_index(drop=True)

    for y in range(ret[1], ret[2] + 1):
        columns.append('y{}'.format(y))

    columns.append('total')

    # print(columns)

    showHeatmap(df, columns, valtype, valoff, toImg)


def showWinRateInYears(lstpnl: list, valtype: str = '', valoff: float = 0.0, toImg: bool = False):
    arr = buildPNLListWinRateInYears2(lstpnl)

    fig = go.Figure()

    for v in arr:
        fig.add_trace(go.Scatter(x=v['df']['date'], y=v['df']['winrate'],
                                 mode='lines',
                                 name=v['title']))

    if toImg:
        fig.show(renderer="png")
    else:
        fig.show()


def showHeatmapWinRateInMonths(lstpnl: list, sortby: str = '', valtype: str = '', valoff: float = 0.0, toImg: bool = False):
    ret = buildPNLWinRateInMonths(lstpnl)
    columns = []

    df = ret[0]

    if sortby != '':
        df = ret[0].sort_values(by=sortby).reset_index(drop=True)

    for y in range(ret[1], ret[3] + 1):
        if y == ret[1]:
            for m in range(ret[2], 12 + 1):
                columns.append('m{}{}'.format(y, m))
        elif y == ret[3]:
            for m in range(1, ret[4] + 1):
                columns.append('m{}{}'.format(y, m))
        else:
            for m in range(1, 12 + 1):
                columns.append('m{}{}'.format(y, m))

    columns.append('total')

    # print(columns)

    showHeatmap(df, columns, valtype, valoff, toImg)


def showWinRateInMonths(lstpnl: list, valtype: str = '', valoff: float = 0.0, toImg: bool = False):
    arr = buildPNLListWinRateInMonths2(lstpnl)

    fig = go.Figure()

    for v in arr:
        fig.add_trace(go.Scatter(x=v['df']['date'], y=v['df']['winrate'],
                                 mode='lines',
                                 name=v['title']))

    if toImg:
        fig.show(renderer="png")
    else:
        fig.show()
