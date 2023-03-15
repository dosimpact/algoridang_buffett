- [schema comment](#schema-comment)
  - [operation-schema.json](#operation-schemajson)
- [change log](#change-log)


# schema comment 

## operation-schema.json

+ iterations
+ tickers

```json
{
  "id": 1,  // pk
  "userId": 1, // onwer
  "reportName": "report_name", // saved file name
  "iterations": [ // port iterations
    {
      "id":1,
      "startDate": "2022-9-12", // start 
      "endDate": "2022-10-13",  // end (null ,종료일 없음) 
      "tickers": [  // univ
        {
          "key":"017250",
          "name":"인터엠",
        },
        {
          "key":"070300",
          "name":"엑스큐어",
        },
        {
          "key":"070590",
          "name":"한솔인티큐브",
        },
        {
          "key":"134060",
          "name":"이퓨쳐",
        },
        {
          "key":"001770",
          "name":"SHD",
        },
      ]
    }
  ],
  "opsTradingFee": 0, // 매매수수료
  "opsSlippage":0, // 슬리피지
  "opsIterationsIdx": 0, // 현재 운용중인 이터레이션 ( 보통 iteration 배열 )
  "opsLastUpdateAt": "", // 마지막 리포트 생성일 
  "opsVersion": "", // 리포트 생성 버전
  "rebalancing":"QUATER", // QUATER(default), MONTH, QUATER, YEAR,
  "tickerProviderStrategy":"",
  "buyStrategy":null,// default(null, 포트 시작날짜 전량 종가 매수)
  "sellStrategy":null, // default(null,포트 종료날짜 전량 종가 매도 )
  "reportBenchmarkTicker": "KQ11" // 코스피 KS11, 코스닥 KQ11
}

```

# change log

