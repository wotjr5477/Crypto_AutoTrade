import pyupbit

# Exchange API
## 로그인
access = "TbT5pDsRrLq9UvpnrTRIJskuI2xpljB76AbDOfyR"          # 본인 값으로 변경
secret = "lxNMvrWP71MXetix38H88DyjxRQ8X0OF10GXjsKp"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

## 잔고 조회
print(str(upbit.get_balance("KRW")) + " KRW")         # 보유 현금 조회
print(str(upbit.get_balance("KRW-BTC")) + " BTC")     # 비트코인 자산 조회
print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회(리플)