# CLOVA OCR API 사용

import json
import base64
import requests

with open("testImage8.png", "rb") as f:
    img = base64.b64encode(f.read())

 # 본인의 APIGW Invoke URL로 치환
URL = ""
    
 # 본인의 Secret Key로 치환
KEY = ""
    
headers = {
    "Content-Type": "application/json",
    "X-OCR-SECRET": KEY
}
    
data = {
    "version": "V1",
    "requestId": "sample_id", # 요청을 구분하기 위한 ID, 사용자가 정의
    "timestamp": 0, # 현재 시간값
    "lang": "ko",
    "resultType": "string",
    "images": [
        {
            "name": "sample_image",
            "format": "jpg",
            "data": img.decode('utf-8')
        }
    ]
}
data = json.dumps(data)
response = requests.post(URL, data=data, headers=headers)
res = json.loads(response.text)

ocr_text = []

for i in range(len(res['images'][0]['fields'])):
    plz = res['images'][0]['fields'][i]['inferText']
    ocr_text.append(plz)

result = ' '.join(s for s in ocr_text)
print(result)