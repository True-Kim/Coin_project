
import pyupbit
import numpy as np


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv('KRW-BTC')
    #df = df['2021']
    df['range'] = (df['high'] - df['low']) * k
    #df['range_shift1'] = df['range'].shift(1)
    df['target'] = df['open'] + df['range'].shift(1)  #목표가 칼럼 추가

    fee = 0.05

    df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target']-fee, 1)  #고가와 목표가를 비교 #조건, 조건이 참 일 때의 값, 조건이 거짓일 때의 값


    df['hpr'] = df['ror'].cumprod()
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    ror = df['ror'].cumprod()[-2]
    return ror

for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror))  #k값이 얼마일 때 가장 높은 수익률ror
#df.to_excel("btc.xlsx")

#MDD계산하기
#MDD(Maximum Draw Down)은 투자 기간 중에 포트폴리오의 전 고점에서 저점까지의 최대 누적 손실을 의미
#낙폭 중 가장 큰 값이 바로 MDD

