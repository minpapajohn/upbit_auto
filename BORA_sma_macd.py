import time
import pyupbit
import datetime
import numpy as np

access = "lW3D2klxyDt5pWx2RpZU3zU926bSDwUb1YoxzWPl"
secret = "6xntC6KBqHhEj5sUie7dskl2q0JRuaxhXtrAJqds"

def get_SMA_MACD(ticker) :
    df = pyupbit.get_ohlcv(ticker, interval='minutes10', count=116)
    SMA01 = df['close'].rolling(window=3).mean() 
    SMA02 = df['close'].rolling(window=10).mean()
    SMA03 = df['close'].rolling(window=50).mean()
    
    ShortEMA = df.close.ewm(span=12, adjust=False).mean()
    LongEMA = df.close.ewm(span=26, adjust=False).mean()
    MACD = ShortEMA-LongEMA 
    Signal = MACD.ewm(span=9, adjust=False).mean()
    
    return (SMA01, SMA02, SMA03, MACD, Signal)

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0
    
def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

upbit = pyupbit.Upbit(access, secret) 
print("SMA_MACD Autotrade Start")

coin = input("KRW-BORA") 
coin_ = input("BORA")

while True: 
    try:
        now = datetime.datetime.now() 
        start_time = now - datetime.timedelta(hours=1) 
        end_time = now + datetime.timedelta(hours=10) 
            
        if start_time < now < end_time: 
                current_price = get_current_price(coin) 
        SMA01 = get_SMA_MACD(coin)[0] 
        SMA02 = get_SMA_MACD(coin)[1] 
        SMA03 = get_SMA_MACD(coin)[2] 
        MACD = get_SMA_MACD(coin)[3] 
        Signal = get_SMA_MACD(coin)[4] 
        print(SMA01[-1]) 
        print(SMA02[-1]) 
        print(SMA03[-1]) 
        print(MACD[-1]) 
            
        if (SMA03[-1] < SMA02[-1]) and (SMA03[-1] < SMA01[-1]) and ((SMA01[-2] < SMA02[-2]) and (SMA01[-1] > SMA02[-1])) and (MACD[-1] > Signal[-1]) :
                krw = upbit.get_balance("KRW") 
                upbit.buy_market_order(coin, krw*0.9995/2)
                buy_price = current_price 
                print(buy_price) 
            
        if SMA01[-1] < SMA02[-1] : 
                bal = upbit.get_balance(coin) 
                upbit.sell_market_order(coin, bal) 
                sell_price = current_price 
                print(sell_price) 
            
        earned_price = upbit.get_balance("KRW") 
        if earned_price >= (start_price*0.2)+start_price:     
            break 
            
            time.sleep(200) 
    except Exception as e:
            print(e) 
            time.sleep(1)
