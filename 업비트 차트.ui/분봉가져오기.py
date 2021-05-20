import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1") #1분마다 가져오기
#count=5 개수 설정도 추가 가능
print(df)

orderbook = pyupbit.get_orderbook("KRW-BTC")
print(orderbook)

bids_asks = orderbook[0]['orderbook_units']

for bid_ask in bids_asks:
    print(bid_ask)