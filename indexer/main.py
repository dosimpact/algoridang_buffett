import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import numpy as np
import json
import redis
import pandas as pd
import datetime
from io import BytesIO
import time

# .env
env = dict({
    "report_dir":"/content/drive/MyDrive/_ColabNotebooks/projects/forward-report/",
    "report_name":"2-forward-testing-v2-TC1", # not use
    "benchmark":"KQ11", # fdr : KS11 , yfinance : ^KS11 ,   # 코스피 KS11, 코스닥 KQ11
    "redis_host":"dosimpact-2.iptime.org",
    "redis_port":"8000",
    "redis_password":"Redosimpact",
    "redis_OHLCV_TTL":"432000" # 5days
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
  dt = datetime.datetime.now(datetime.timezone.utc) # UTC 현재 시간
  now = dt.now() + datetime.timedelta(hours=hours) # UTC -> UTC+9

  TODAY_DATE = now.strftime('%Y-%m-%d')
  TODAY_TIME = now.strftime('%H-%M-%S')

  return TODAY_DATE, TODAY_TIME


def getOHLCV(code, start, end=None):
  finalEndDate = end if end else getDateTimeStr()[0]
  cacheKey = f"ticker_{code}_{start}_{finalEndDate}"

  if(isCacheConnected):
      cached = cache.get(cacheKey)
      if(cached):
        return pd.read_json(BytesIO(cached))

      else:
        df = fdr.DataReader(code, start, finalEndDate)
        cache.setex(cacheKey,env['redis_OHLCV_TTL'],df.to_json())
        return df
  else:
    return fdr.DataReader(code, start, finalEndDate)


time_s = time.time()

# if __name__ == "__main__":
df_krx = fdr.StockListing('KRX')
codeList = list(df_krx['Code'])
successCount = 0

print(f"[start] ticker price batch job - {len(codeList)}")
for code in codeList[:100]:
    try:
        getOHLCV(code,'1900')
        successCount+=1
        time_i = time.time()
        print(f"[success] ticker price batch job - {code}"+f" [{time_i - time_s:.5f} sec]")

    except Exception as err:
        print("getOHLCV Exception")
        print(err)  


time_e = time.time()
print(f"[end] ticker price batch job - {successCount} / {len(codeList)}")
print(f"complated : {time_e - time_s:.5f} sec")
