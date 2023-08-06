# -*- coding:utf-8 -*-
import grpc
import trdb2py.trading2_pb2
import trdb2py.tradingdb2_pb2
import trdb2py.tradingdb2_pb2_grpc
from trdb2py.utils import str2Asset
from datetime import datetime
import time
import pandas as pd


def getAssetCandles(cfg: dict, asset: str, tsStart: int, tsEnd: int) -> pd.DataFrame:
    channel = grpc.insecure_channel(cfg['servaddr'])
    stub = trdb2py.tradingdb2_pb2_grpc.TradingDB2Stub(channel)

    curasset = str2Asset(asset)

    response = stub.getCandles(trdb2py.tradingdb2_pb2.RequestGetCandles(
        market=curasset.market,
        symbol=curasset.code,
        tsStart=tsStart,
        tsEnd=tsEnd,
        basicRequest=trdb2py.trading2_pb2.BasicRequestData(
            token=cfg['token'],
        ),
    ))

    fv = {'date': [], 'close': []}
    for curres in response:
        for candle in curres.candles.candles:
            fv['date'].append(datetime.fromtimestamp(
                candle.ts).strftime('%Y-%m-%d'))
            fv['close'].append(candle.close / 10000.0)

    return pd.DataFrame(fv)


def genSimTradingParams(cfg, lstParams: list, ignoreCache: bool = False):
    for i in range(len(lstParams)):
        yield trdb2py.tradingdb2_pb2.RequestSimTrading(
            basicRequest=trdb2py.trading2_pb2.BasicRequestData(
                token=cfg['token'],
            ),
            params=lstParams[i],
            ignoreCache=ignoreCache,
            index=i,
        )


def simTradings(cfg, lstParams: list, ignoreCache: bool = False) -> list:
    channel = grpc.insecure_channel(cfg['servaddr'])
    stub = trdb2py.tradingdb2_pb2_grpc.TradingDB2Stub(channel)

    lstRes = []
    responses = stub.simTrading2(
        genSimTradingParams(cfg, lstParams, ignoreCache))
    for response in responses:
        if len(response.pnl) > 0:
            pnl = response.pnl[0]
            lstRes.append({'title': pnl.title, 'pnl': pnl.total})

    return lstRes


def simTrading(cfg, params: trdb2py.trading2_pb2.SimTradingParams, ignoreCache: bool = False) -> dict:
    channel = grpc.insecure_channel(cfg['servaddr'])
    stub = trdb2py.tradingdb2_pb2_grpc.TradingDB2Stub(channel)

    response = stub.simTrading(trdb2py.tradingdb2_pb2.RequestSimTrading(
        basicRequest=trdb2py.trading2_pb2.BasicRequestData(
            token=cfg['token'],
        ),
        params=params,
    ))

    if len(response.pnl) > 0:
        pnl = response.pnl[0]
        return {'title': pnl.title, 'pnl': pnl.total}

    return None
