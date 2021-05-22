import time
import pyupbit

""" 목표가 계산 """
def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    # 목표가 = 전날 종가 + (전날 고가 - 전날 저가) * k
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

""" 매수 함수"""
def buy_crypto_currency(upbit, ticker):
    krw = upbit.get_balance("KRW")
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook[0]['orderbook_units'][0]['ask_price']
    unit = krw/float(sell_price) * 0.7
    return upbit.buy_market_order(ticker, unit)

""" 매도 함수 """
def sell_crypto_currency(upbit, ticker):
    unit = upbit.get_balance(ticker)
    return upbit.sell_market_order(ticker, unit)

""" 전일 5일의 이동평균 계산 """
def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]