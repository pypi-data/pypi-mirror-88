# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2
from trdb2py.utils import str2Asset
from datetime import datetime
import time
import pandas as pd


def isWinAtTimeIntervals(pnl: trdb2py.trading2_pb2.PNLAssetData, tsStart: int = -1, tsEnd: int = -1) -> bool:
    """
    isWinAtTimeIntervals - 判断这个时间区间内，是否赢（不亏损），时间区间是[tsStart, tsEnd)
    """

    hasStart = False
    pvStart = 0
    pvEnd = 0

    if tsStart <= 0:
        tsStart = pnl.values[0].ts

    if tsEnd <= 0:
        tsEnd = pnl.values[len(pnl.values) - 1].ts + 1

    for v in pnl.values:
        if v.ts >= tsStart and v.ts < tsEnd:
            if not hasStart:
                hasStart = True
                pvStart = v.perValue

            pvEnd = v.perValue

    return pvEnd >= pvStart


def calcPNLWinRateInYear(pnl: trdb2py.trading2_pb2.PNLAssetData, year: int = -1) -> dict:
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
        else:
            iswin = isWinAtTimeIntervals(pnl)

            if iswin:
                ret['winrate'] = 1.0
            else:
                ret['winrate'] = 0.0

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
    else:
        dtStart = datetime.strptime('{}-01-01'.format(year), '%Y-%m-%d')
        dtEnd = datetime.strptime('{}-01-01'.format(year + 1), '%Y-%m-%d')
        iswin = isWinAtTimeIntervals(
            pnl, dtStart.timestamp(), dtEnd.timestamp())

        if iswin:
            ret['winrate'] = 1.0
        else:
            ret['winrate'] = 0.0

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
        ret = calcPNLWinRateInYear(v['pnl'])
        fv0['total'].append(ret['winrate'])

    # print(fv0)

    return (pd.DataFrame(fv0), minyear, maxyear)


def buildPNLWinRateInYears2(pnl: trdb2py.trading2_pb2.PNLAssetData) -> pd.DataFrame:
    fv0 = {
        'date': [],
        'winrate': [],
    }

    sdt = datetime.fromtimestamp(pnl.values[0].ts)
    edt = datetime.fromtimestamp(pnl.values[len(pnl.values) - 1].ts)

    minyear = sdt.year
    maxyear = edt.year

    for y in range(minyear, maxyear + 1):
        fv0['date'].append(y)

        ret = calcPNLWinRateInYear(pnl, y)
        fv0['winrate'].append(ret['winrate'])

    return pd.DataFrame(fv0)


def buildPNLListWinRateInYears2(lstpnl: list) -> list:
    arr = []

    for v in lstpnl:
        df = buildPNLWinRateInYears2(v['pnl'])
        arr.append({'title': v['title'], 'df': df})

    return arr


def calcPNLWinRateInYearMonth(pnl: trdb2py.trading2_pb2.PNLAssetData, year: int = -1, month: int = -1) -> dict:
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
        else:
            iswin = isWinAtTimeIntervals(pnl)

            if iswin:
                ret['winrate'] = 1.0
            else:
                ret['winrate'] = 0.0

        return ret

    for v in pnl.lstCtrl:
        dt = datetime.fromtimestamp(v.ts)
        if dt.year == year and dt.month == month:
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
    else:
        dtStart = datetime.strptime('{}-{}-01'.format(year, month), '%Y-%m-%d')
        dtEnd = None

        if month == 12:
            dtEnd = datetime.strptime(
                '{}-01-01'.format(year + 1), '%Y-%m-%d')
        else:
            dtEnd = datetime.strptime(
                '{}-{}-01'.format(year, month + 1), '%Y-%m-%d')

        iswin = isWinAtTimeIntervals(
            pnl, dtStart.timestamp(), dtEnd.timestamp())

        if iswin:
            ret['winrate'] = 1.0
        else:
            ret['winrate'] = 0.0

    return ret


def buildPNLWinRateInMonths(lstpnl: list) -> tuple:
    minyear = 0
    maxyear = 0
    minmonth = 0
    maxmonth = 0

    for v in lstpnl:
        sdt = datetime.fromtimestamp(v['pnl'].values[0].ts)
        edt = datetime.fromtimestamp(
            v['pnl'].values[len(v['pnl'].values) - 1].ts)

        if minyear == 0 or sdt.year < minyear:
            minyear = sdt.year
            minmonth = sdt.month

        if maxyear == 0 or edt.year > maxyear:
            maxyear = edt.year
            maxmonth = edt.month

    fv0 = {
        'title': [],
    }

    for y in range(minyear, maxyear + 1):
        if y == minyear:
            for m in range(minmonth, 12 + 1):
                fv0['m{}{}'.format(y, m)] = []
        elif y == maxyear:
            for m in range(1, maxmonth + 1):
                fv0['m{}{}'.format(y, m)] = []
        else:
            for m in range(1, 12 + 1):
                fv0['m{}{}'.format(y, m)] = []

    for y in range(minyear, maxyear + 1):
        for v in lstpnl:
            if y == minyear:
                fv0['title'].append(v['title'])

                for m in range(minmonth, 12 + 1):
                    ret = calcPNLWinRateInYearMonth(v['pnl'], y, m)
                    fv0['m{}{}'.format(y, m)].append(ret['winrate'])
            elif y == maxyear:
                for m in range(1, maxmonth + 1):
                    ret = calcPNLWinRateInYearMonth(v['pnl'], y, m)
                    fv0['m{}{}'.format(y, m)].append(ret['winrate'])
            else:
                for m in range(1, 12 + 1):
                    ret = calcPNLWinRateInYearMonth(v['pnl'], y, m)
                    fv0['m{}{}'.format(y, m)].append(ret['winrate'])

    fv0['total'] = []
    for v in lstpnl:
        ret = calcPNLWinRateInYearMonth(v['pnl'])
        fv0['total'].append(ret['winrate'])

    # print(fv0)

    return (pd.DataFrame(fv0), minyear, minmonth, maxyear, maxmonth)


def buildPNLWinRateInMonths2(pnl: trdb2py.trading2_pb2.PNLAssetData) -> pd.DataFrame:
    fv0 = {
        'date': [],
        'winrate': [],
    }

    sdt = datetime.fromtimestamp(pnl.values[0].ts)
    edt = datetime.fromtimestamp(pnl.values[len(pnl.values) - 1].ts)

    minyear = sdt.year
    maxyear = edt.year
    minmonth = sdt.month
    maxmonth = edt.month

    for y in range(minyear, maxyear + 1):
        if y == minyear:
            for m in range(minmonth, 12 + 1):
                fv0['date'].append(y * 100 + m)
                ret = calcPNLWinRateInYearMonth(pnl, y, m)
                fv0['winrate'].append(ret['winrate'])
        elif y == maxyear:
            for m in range(1, maxmonth + 1):
                fv0['date'].append(y * 100 + m)
                ret = calcPNLWinRateInYearMonth(pnl, y, m)
                fv0['winrate'].append(ret['winrate'])
        else:
            for m in range(1, 12 + 1):
                fv0['date'].append(y * 100 + m)
                ret = calcPNLWinRateInYearMonth(pnl, y, m)
                fv0['winrate'].append(ret['winrate'])

    return pd.DataFrame(fv0)


def buildPNLListWinRateInMonths2(lstpnl: list) -> list:
    arr = []

    for v in lstpnl:
        df = buildPNLWinRateInMonths2(v['pnl'])
        arr.append({'title': v['title'], 'df': df})

    return arr
