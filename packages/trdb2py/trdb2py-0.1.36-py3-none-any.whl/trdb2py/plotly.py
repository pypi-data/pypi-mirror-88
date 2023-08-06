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


def showPNL(pnl: dict, isPerValue: bool = True, dtFormat: str = '%Y-%m-%d', toImg: bool = False):
    fv0 = {'date': [], 'value': []}
    for v in pnl['pnl'].values:
        fv0['date'].append(datetime.fromtimestamp(
            v.ts).strftime(dtFormat))

        if isPerValue:
            fv0['value'].append(v.perValue)
        else:
            fv0['value'].append(v.value - v.cost)

    fig = px.line(pd.DataFrame(fv0), x='date', y='value', title=pnl['title'])

    if toImg:
        fig.show(renderer="png")
    else:
        fig.show()


def showPNLs(lstpnl: list, isPerValue: bool = True, dtFormat: str = '%Y-%m-%d', toImg: bool = False):
    fig = go.Figure()

    for pnl in lstpnl:
        fv0 = {'date': [], 'value': []}
        for v in pnl['pnl'].values:
            fv0['date'].append(datetime.fromtimestamp(
                v.ts).strftime(dtFormat))

            if isPerValue:
                fv0['value'].append(v.perValue)
            else:
                fv0['value'].append(v.value - v.cost)

        df = pd.DataFrame(fv0)

        fig.add_trace(go.Scatter(x=df['date'], y=df['value'],
                                 mode='lines',
                                 name=pnl['title']))

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

    if valtype == 'abs':
        for v in arr:

            vals = []
            for wrv in v['df']['winrate']:
                vals.append(abs(wrv + valoff))

            fig.add_trace(go.Scatter(x=v['df']['date'], y=vals,
                                     mode='lines',
                                     name=v['title']))
    else:
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
