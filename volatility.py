from pyupbit import Upbit
import pyupbit

def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def buy_crypto_currency(Upbit, ticker):
    krw = Upbit.get_balance(ticker)[2]
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw/float(sell_price) * 0.7
    return Upbit.buy_market_order(ticker, unit)

def sell_crypto_currency(Upbit, ticker):
    unit = Upbit.get_balance(ticker)[0]
    return Upbit.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]