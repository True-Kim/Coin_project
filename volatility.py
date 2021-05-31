import time
import pyupbit

""" 목표가 계산 """
def get_target_price(ticker):
    # 업비트 거래소에서 지정된 ticker의 Open, High, Low, Close, Volume (시가, 고가, 저가, 종가, 거래량)을 df에 바인딩
    # 최근 200개 행의 DataFrame으로 반환
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    # 변동성 전략 : 목표가 = 전날 종가 + (전날 고가 - 전날 저가) * k     
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

""" 매수 함수"""
def buy_crypto_currency(upbit, ticker):
    # 원화 보유수량을 krw에 바인딩
    krw = upbit.get_balance("KRW")
    # ticker의 호가정보를 orderbook에 바인딩
    orderbook = pyupbit.get_orderbook(ticker)
    # orderbook의 0번째 호가정보를 가져와라
    sell_price = orderbook[0]['orderbook_units'][0]['ask_price']
    # 구매 단위
    unit = krw/float(sell_price) * 0.7
    # 시장가 매수
    return upbit.buy_market_order(ticker, unit)

""" 매도 함수 """
def sell_crypto_currency(upbit, ticker):
    # 해당 티커 보유수량을 unit에 바인딩 
    unit = upbit.get_balance(ticker)
    # 시장가 매도
    return upbit.sell_market_order(ticker, unit)

""" 전일 5일의 이동평균 계산 """
def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    # 5일간의 평균 계산
    ma = close.rolling(5).mean()
    return ma[-2]
