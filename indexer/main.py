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

print(os.getenv('benchmark'))

# .env
env = dict({
    # fdr : KS11 , yfinance : ^KS11 ,   # 코스피 KS11, 코스닥 KQ11
    "benchmark": os.getenv('benchmark'),
    "redis_host": os.getenv('redis_host'),
    "redis_port": os.getenv('redis_port'),
    "redis_password": os.getenv('redis_password'),
    "redis_OHLCV_TTL": os.getenv('redis_OHLCV_TTL'),  # 5days
})

CONST = dict({
    "getOHLCV_lastUpdateAt": 'getOHLCV_lastUpdateAt',
    "getOHLCV_lastUpdateCount": 'getOHLCV_lastUpdateCount'
})

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


# utils
def getDateTimeStr(hours=9):
    dt = datetime.datetime.now(datetime.timezone.utc)  # UTC 현재 시간
    now = dt.now() + datetime.timedelta(hours=hours)  # UTC -> UTC+9

    TODAY_DATE = now.strftime('%Y-%m-%d')
    TODAY_TIME = now.strftime('%H-%M-%S')

    return TODAY_DATE, TODAY_TIME


def getOHLCV(code, start, end=None):
    finalEndDate = end if end else getDateTimeStr()[0]
    cacheKey = f"ticker_{code}"

    if (isCacheConnected):
        cached = cache.get(cacheKey)
        if (cached):
            return pd.read_json(BytesIO(cached))

        else:
            df = fdr.DataReader(code, start, finalEndDate)
            cache.setex(cacheKey, env['redis_OHLCV_TTL'], df.to_json())
            return df
    else:
        return fdr.DataReader(code, start, finalEndDate)


time_s = time.time()

df_krx = fdr.StockListing('KRX')
codeList = list(df_krx['Code'])
successCount = 0
finalEndDate = getDateTimeStr()[0]

print(f"[start] ticker price batch job - {len(codeList)}")

print(f"[info] finalEndDate {finalEndDate}")
cache.set(CONST["getOHLCV_lastUpdateAt"], finalEndDate)

for code in codeList:
    try:
        getOHLCV(code, '1900', finalEndDate)
        successCount += 1
        time_i = time.time()
        print(
            f"[success] ticker price batch job - {code}"+f" [{time_i - time_s:.5f} sec]")
        time.sleep(0.2)

    except Exception as err:
        print("getOHLCV Exception")
        print(err)


time_e = time.time()
print(f"[end] ticker price batch job - {successCount} / {len(codeList)}")
cache.set(CONST["getOHLCV_lastUpdateCount"], successCount)

print(f"complated : {time_e - time_s:.5f} sec")
