#패키지 설치

import pyupbit
import pprint

f = open("upbit.txt")
lines = f.readlines()   # 모든 라인 읽어오기
access = lines[0].strip()  # 0번째 줄 가져오기 strip()메소드를 사용해 '\n'을 없애 줌.
secret = lines[1].strip()
f.close()

# print(access)
# print(secret)


upbit = pyupbit.Upbit(access, secret)


# ---- 잔고 조회
# 전체 잔고 조회
balances = upbit.get_balances() 
print(balances)  # 튜플로 출력됨, 첫번재는 자산 출력/ 두번째는 초당 호출횟수, 분당 호출횟수에 대한 정보 출력 
print(balances[0])  # 자산 출력
pprint.pprint(balances[0][0])  # 더 예쁘게 출력 


# 특정 코인 잔고 조회
balance = upbit.get_balance(ticker = "KRW")
print(balance)


# ---- 지정가 주문
# XRP 지정가 매수주문 buy_limit_order(티커, 주문가격, 주문량)
xrp_price = pyupbit.get_current_price("KRW-XRP")
print(xrp_price)

# 지정가 주문을 통해 매매 금액보다 낮게 주문 넣기 - 참고 : uuid는 고유 주문 아이디로 잘 기억해둬야 함. 체결 취소에 사용됨
resp = upbit.buy_limit_order("KRW-XRP", 200, 100)
pprint.pprint(resp)


# 지정가 매도
# sell_limit_order(티커, 주문가격, 주문량)
# 1) 잔고조회
xrp_balance = upbit.get_balance("KRW-XRP") 
# 2) 매도
resp = upbit.sell_limit_order("KRW-XRP", 265, xrp_balance)
print(resp)


# ---- 시장가 주문
# 시장가 매수
# buy_market_order(티커, 주문가격) -> 이때 주문가격은 원화기준
resp = upbit.buy_market_order("KRW-XRP", 10000)
pprint.pprint(resp)


# 시장가 매도
# sell_market_order(티커, 주문량)
# 1) 잔고조회
xrp_balance = upbit.get_balance("KRW-XRP")
# 2) 매도
resp = upbit.sell_market_order("KRW-XRP", xrp_balance)
pprint.pprint(resp)


