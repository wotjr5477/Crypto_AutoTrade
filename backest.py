import pyupbit
import numpy as np

## 변동성 돌파 전략

# OHLCV = Open, High, Low, Close, Volume >> 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-BTC", count = 7)
print(df)

# 변동폭 * k값 계산, (고가-저가) * k값 / k = 0.5
df['range'] = (df['high'] - df['low']) * 0.5

# 매수가(target), range 칼럼을 한칸씩 밑으로 내림
df['target'] = df['open'] + df['range'].shift(1)
#print(df)

# fee = 0.0032

# df['ror'] = np.where(df['high'] > df['target'],
#                      df['close'] / df['target'] - fee,
#                      1)

# 수익율(ror), np.where(조건문, 참일 때 값, 거짓일 때 값)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

# 누적 곱 계산(cumprod) >> 누적 수익률(hpr)
df['hpr'] = df['ror'].cumprod()

# Draw Down(DD, 낙폭) 계산(누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# Max DD 계산
print("MDD(%): ", df['dd'].max())

# 엑셀로 출력
df.to_excel("dd.xlsx")