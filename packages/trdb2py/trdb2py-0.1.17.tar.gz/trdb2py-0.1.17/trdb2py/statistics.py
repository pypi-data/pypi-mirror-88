# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2
from trdb2py.utils import str2Asset
from datetime import datetime
import time
import pandas as pd


def calcPNLWinRateInYear(pnl: trdb2py.trading2_pb2.PNLAssetData, year: int) -> dict:
    sellnums = 0
    winnums = 0
    buynums = 0

    if year == -1:
        for v in pnl.lstCtrl:
            if v.type == trdb2py.trading2_pb2.CtrlType.CTRL_SELL:
                sellnums = sellnums + 1
                if v.sellPrice > v.averageHoldingPrice:
                    winnums = winnums + 1
            if v.type == trdb2py.trading2_pb2.CtrlType.CTRL_BUY:
                buynums = buynums + 1

        ret = {'sellnums': sellnums, 'winnums': winnums,
               'winrate': 0, 'buynums': buynums}
        if sellnums > 0:
            ret['winrate'] = winnums * 1.0 / sellnums

        return ret

    for v in pnl.lstCtrl:
        dt = datetime.fromtimestamp(v.ts)
        if dt.year == year:
            if v.type == trdb2py.trading2_pb2.CtrlType.CTRL_SELL:
                sellnums = sellnums + 1
                if v.sellPrice > v.averageHoldingPrice:
                    winnums = winnums + 1
            if v.type == trdb2py.trading2_pb2.CtrlType.CTRL_BUY:
                buynums = buynums + 1

    ret = {'sellnums': sellnums, 'winnums': winnums,
           'winrate': 0, 'buynums': buynums}
    if sellnums > 0:
        ret['winrate'] = winnums * 1.0 / sellnums

    return ret


def buildPNLWinRateInYears(lstpnl: list) -> tuple:
    minyear = 0
    maxyear = 0

    for v in lstpnl:
        sdt = datetime.fromtimestamp(v['pnl'].values[0].ts)
        edt = datetime.fromtimestamp(
            v['pnl'].values[len(v['pnl'].values) - 1].ts)

        if minyear == 0 or sdt.year < minyear:
            minyear = sdt.year

        if maxyear == 0 or edt.year > maxyear:
            maxyear = edt.year

    fv0 = {
        'title': [],
    }

    for y in range(minyear, maxyear + 1):
        fv0['y{}'.format(y)] = []

        for v in lstpnl:
            if y == minyear:
                fv0['title'].append(v['title'])

            ret = calcPNLWinRateInYear(v['pnl'], y)
            fv0['y{}'.format(y)].append(ret['winrate'])

    fv0['total'] = []
    for v in lstpnl:
        ret = calcPNLWinRateInYear(v['pnl'], -1)
        fv0['total'].append(ret['winrate'])

    # print(fv0)

    return (pd.DataFrame(fv0), minyear, maxyear)
