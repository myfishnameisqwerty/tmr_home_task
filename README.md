run `docker-compose build`

run `docker-compose up`

You are good to go. Navigate to http://127.0.0.1:8000/docs and try the post method

You can see in the logs the proccess.
 ```INFO:root:Producer started
web-1               | INFO:root:Producer sent event='{"request_id":"1qaz1qa","event_id":"1qaz1qa","role_id":"string","event_type":"string","event_timestamp":"2024-07-18T23:45:51.475000Z","affected_assets":["string"]}'
web-1               | INFO:root:Producer stopped
anomaly_detector-1  | INFO:root:Consumer event='{"request_id":"1qaz1qa","event_id":"1qaz1qa","role_id":"string","event_type":"string","event_timestamp":"2024-07-18T23:45:51.475000Z","affected_assets":["string"]}'
web-1               | INFO:     172.18.0.1:44826 - "POST / HTTP/1.1" 200 OK
localstack-1        | 2024-07-19T00:04:11.872  INFO --- [et.reactor-0] localstack.request.aws     : AWS dynamodb.GetItem => 200
anomaly_detector-1  | INFO:root:response={'ResponseMetadata': {'RequestId': 'c349b2c7-afbc-464b-a2a8-7db4228eeee9', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'TwistedWeb/24.3.0', 'date': 'Fri, 19 Jul 2024 00:04:11 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'x-amzn-requestid': 'c349b2c7-afbc-464b-a2a8-7db4228eeee9', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}
localstack-1        | 2024-07-19T00:04:12.618  INFO --- [et.reactor-1] localstack.request.aws     : AWS dynamodb.PutItem => 200
anomaly_detector-1  | INFO:root:Anomaly detected for event 1qaz1qa with score 7.
web-1               | INFO:root:Producer started
web-1               | INFO:root:Producer sent event='{"request_id":"qwe","event_id":"1qaz1qa","role_id":"string","event_type":"string","event_timestamp":"2024-07-18T23:45:51.475000Z","affected_assets":["string"]}'
anomaly_detector-1  | INFO:root:Consumer event='{"request_id":"qwe","event_id":"1qaz1qa","role_id":"string","event_type":"string","event_timestamp":"2024-07-18T23:45:51.475000Z","affected_assets":["string"]}'
web-1               | INFO:root:Producer stopped
localstack-1        | 2024-07-19T00:04:21.566  INFO --- [et.reactor-1] localstack.request.aws     : AWS dynamodb.GetItem => 200
anomaly_detector-1  | INFO:root:response={'Item': {'anomaly_score': Decimal('7'), 'event_id': '1qaz1qa', 'event_type': 'string', 'affected_assets': ['string'], 'role_id': 'string', 'event_timestamp': '2024-07-18T23:45:51.475000Z', 'request_id': '1qaz1qa'}, 'ResponseMetadata': {'RequestId': 'e886f8b1-cd07-4724-9d99-d693d4e68c5d', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'TwistedWeb/24.3.0', 'date': 'Fri, 19 Jul 2024 00:04:21 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '262', 'x-amzn-requestid': 'e886f8b1-cd07-4724-9d99-d693d4e68c5d', 'x-amz-crc32': '3086977737'}, 'RetryAttempts': 0}}
web-1               | INFO:     172.18.0.1:58272 - "POST / HTTP/1.1" 200 OK
anomaly_detector-1  | INFO:root:Event 1qaz1qa already processed.
web-1               | INFO:root:Producer started
web-1               | INFO:root:Producer sent event='{"request_id":"qwe","event_id":"ereew","role_id":"string","event_type":"string","event_timestamp":"2024-07-18T23:45:51.475000Z","affected_assets":["string"]}'
anomaly_detector-1  | INFO:root:Consumer event='{"request_id":"qwe","event_id":"ereew","role_id":"string","event_type":"string","event_timestamp":"2024-07-18T23:45:51.475000Z","affected_assets":["string"]}'
localstack-1        | 2024-07-19T00:04:32.113  INFO --- [et.reactor-1] localstack.request.aws     : AWS dynamodb.GetItem => 200
web-1               | INFO:root:Producer stopped
anomaly_detector-1  | INFO:root:response={'ResponseMetadata': {'RequestId': '10ee1fcb-fe86-47d2-bccb-f40349192373', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'TwistedWeb/24.3.0', 'date': 'Fri, 19 Jul 2024 00:04:32 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'x-amzn-requestid': '10ee1fcb-fe86-47d2-bccb-f40349192373', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}
web-1               | INFO:     172.18.0.1:39394 - "POST / HTTP/1.1" 200 OK
anomaly_detector-1  | INFO:root:No anomaly detected for event ereew.
web-1               | INFO:root:Producer started
web-1               | INFO:root:Producer sent event='{"request_id":"qwe","event_id":"ereew","role_id":"string","event_type":"string","event_timestamp":"2024-07-18T23:45:51.475000Z","affected_assets":["string"]}'
anomaly_detector-1  | INFO:root:Consumer event='{"request_id":"qwe","event_id":"ereew","role_id":"string","event_type":"string","event_timestamp":"2024-07-18T23:45:51.475000Z","affected_assets":["string"]}'
localstack-1        | 2024-07-19T00:04:37.706  INFO --- [et.reactor-0] localstack.request.aws     : AWS dynamodb.GetItem => 200
web-1               | INFO:root:Producer stopped```
