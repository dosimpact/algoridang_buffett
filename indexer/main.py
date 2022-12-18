import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import numpy as np
import json
import redis
import pandas as pd
import datetime
import time
import os
from io import BytesIO
from dotenv import load_dotenv

load_dotenv(verbose=True)

# .env
env = dict({
    # fdr : KS11 , yfinance : ^KS11 ,   # 코스피 KS11, 코스닥 KQ11
    "benchmark": os.getenv('benchmark'),
    "redis_host": os.getenv('redis_host'),
    "redis_port": os.getenv('redis_port'),
    "redis_password": os.getenv('redis_password'),
    "redis_OHLCV_TTL": os.getenv('redis_OHLCV_TTL'),  # 5days
})

# constant
CONST = dict({
    "getOHLCV_lastUpdateAt": 'getOHLCV_lastUpdateAt',
    "getOHLCV_lastUpdateCount": 'getOHLCV_lastUpdateCount',
    "getOHLCV_isUpdating": 'getOHLCV_isUpdating',
})

# redis connection
cache = redis.Redis(
    host=env["redis_host"],
    port=env["redis_port"],
    password=env["redis_password"],
    db=0,
)
isCacheConnected = False

try:
    cache.get('hello')
    isCacheConnected = True
except Exception as err:
    print("REDIS Exception")
    print(err)
    exit(0)


# utils
def getDateTimeStr(hours=9):
    dt = datetime.datetime.now(datetime.timezone.utc)  # UTC 현재 시간
    now = dt + datetime.timedelta(hours=hours)  # UTC -> UTC+9

    TODAY_DATE = now.strftime('%Y-%m-%d')
    TODAY_TIME = now.strftime('%H-%M-%S')

    return TODAY_DATE, TODAY_TIME


def isBeforeOrSame(dateStr1, dateStr2):
    datetime1 = datetime.datetime.strptime(dateStr1, '%Y-%m-%d')
    datetime2 = datetime.datetime.strptime(dateStr2, '%Y-%m-%d')
    return datetime1 <= datetime2

# getOHLCV


def getOHLCV_cachingAllPeriod(code):
    cacheKey_allPeriod = f"ticker_{code}"

    if (isCacheConnected):
        cached = cache.get(cacheKey_allPeriod)
        lastUpdateAt = cache.get('getOHLCV_lastUpdateAt').decode('utf-8')
        todayDate = getDateTimeStr()[0]

        if (cached and lastUpdateAt and isBeforeOrSame(todayDate, lastUpdateAt)):
            df = pd.read_json(BytesIO(cached))
            return df
        else:
            df = fdr.DataReader(code, "1900", todayDate)
            cache.set(cacheKey_allPeriod, df.to_json())
            return df


# main.py
time_s = time.time()

df_krx = fdr.StockListing('KRX')
codeList = list(df_krx['Code'])
successCount = 0
finalEndDate = getDateTimeStr()[0]

print(f"[start] ticker price batch job - {len(codeList)}")
print(f"[info] finalEndDate {finalEndDate}")

cache.set(CONST["getOHLCV_lastUpdateAt"], finalEndDate)
cache.set(CONST["getOHLCV_isUpdating"], 1)

for code in codeList:
    try:
        getOHLCV_cachingAllPeriod(code)
        successCount += 1
        time_i = time.time()
        print(
            f"[success] ticker price batch job - {code}"+f" [{time_i - time_s:.5f} sec]")
        time.sleep(0.2)

    except Exception as err:
        print("getOHLCV Exception")
        print(err)

print(f"[end] ticker price batch job - {successCount} / {len(codeList)}")
cache.set(CONST["getOHLCV_lastUpdateCount"], successCount)
cache.set(CONST["getOHLCV_isUpdating"], 0)

time_e = time.time()
print(f"complated : {time_e - time_s:.5f} sec")
