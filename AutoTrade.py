import time
import pyupbit
import datetime

access = "TbT5pDsRrLq9UvpnrTRIJskuI2xpljB76AbDOfyR"
secret = "lxNMvrWP71MXetix38H88DyjxRQ8X0OF10GXjsKp"

def get_target_price(ticker, k): # ticker(목표 코인), k값
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    # 목표가 = 종가(=다음날 시가) + 변동폭 * k
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True: # 한무 루프
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") # 9:00
        end_time = start_time + datetime.timedelta(days=1) # 9:00 +1일

        # 09:00:00 < 현재 < 08:59:50
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5) # 매수 목표가 생성
            current_price = get_current_price("KRW-BTC") 
            if target_price < current_price: # 현재가가 목표가보다 높으면
                krw = get_balance("KRW") # 원화 잔고 조회
                if krw > 5000: # 최소 거래가격보다 높으면
                    upbit.buy_market_order("KRW-BTC", krw*0.9995) # 수수료 고려(ex. BTC 수수료 0.05% 제외)
        else: # 08:59:00 ~ 09:00:00
            btc = get_balance("BTC") # BTC 잔고 조회
            if btc > 0.00008: #잔고가 5000원 이상이면? >> 근데 btc가 0.00008 이상?
                upbit.sell_market_order("KRW-BTC", btc*0.9995) # BTC 전량 매도
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)