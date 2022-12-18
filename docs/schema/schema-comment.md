- [schema comment](#schema-comment)
  - [operation-schema.json](#operation-schemajson)


# schema comment 

## operation-schema.json

```json
{
  "id": 1,  // pk
  "userId": 1, // onwer
  "reportName": "report_name", // saved file name
  "iterations": [ // port iterations
    {
      "startDate": "2022-9-12", // start 
      "endDate": "2022-10-13",  // end (null ,종료일 없음) 
      "tickers": [  // univ
        {
          "017250": "인터엠",
          "070300": "엑스큐어",
          "070590": "한솔인티큐브",
          "134060": "이퓨쳐",
          "001770": "SHD"
        }
      ]
    }
  ],
  "opsTradingFee": 0, // 매매수수료
  "opsSlippage":0, // 슬리피지
  "opsIterationsIdx": 0, // 현재 운용중인 이터레이션 ( 보통 iteration 배열 )
  "opsLastUpdateAt": "", // 마지막 리포트 생성일 
  "opsVersion": "", // 리포트 생성 버전
  "rebalancing":"PORT_CHANGE", // PORT_CHANGE(default), MONTH, QUATER, YEAR,
  "buyStrategy":null,// default(null, 포트 시작날짜 전량 종가 매수)
  "sellStrategy":null, // default(null,포트 종료날짜 전량 종가 매도 )
  "reportBenchmarkTicker": "KQ11" // 코스피 KS11, 코스닥 KQ11
}

```