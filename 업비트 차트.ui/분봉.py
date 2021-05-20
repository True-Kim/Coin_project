import pyupbit
import pandas as pd

tickers = pyupbit.get_tickers(fiat = 'BTC')
print(tickers)
print(len(tickers))

df = pyupbit.get_ohlcv('KRW-BTC', 'minute1') #1분봉 뒤에 숫자마다 3, 5로 바꾸면 됨
print(df)

#n분봉의 원리 = 1분봉을 조합

"""df['open'].resample('3T').frist()
df['high'].resample('3T').max()
df['low'].resample('3T').min()
df['close'].resample('3T').last()
df['volume'].resample('3T').sum()"""

#시세 캔들 조회(주봉)
df = pyupbit.get_ohlcv(ticker = 'KRW-BTC', interval='week')
print(df) 
#df.to_excel('week_btc.xlsx')

df = pyupbit.get_ohlcv(ticker = 'KRW-BTC', interval = 'day', count = 10) #count 값 설정 안하면 최대 200개 가져옴
print(df)

df = pyupbit.get_ohlcv(ticker = 'KRW-BTC', interval= 'month') #volume이 매우 크게 나옴
print(df)

pd.options.display.float_format = '{:.1f}'.format  #소숫점 1자리까지만 출력
df = pyupbit.get_ohlcv(ticker = 'KRW-BTC', interval='month')
print(df)


