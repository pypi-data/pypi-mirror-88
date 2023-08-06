import pandas as pd
from datetime import datetime
import time
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def showAssetCandles(title: str, dfCandles: pd.DataFrame, columm: str = 'close', toImg: bool = False):
    fig = px.line(dfCandles, x='date', y=columm, title=title)

    if toImg:
        fig.show(renderer="png")
    else:
        fig.show()
