import requests
import json
import uuid
from requests.auth import HTTPBasicAuth

# API URL
url = "https://uat-sandbox-3ds-api.qi.iq/api/v1/payment"

# Basic Auth values
username = "mwtest"  
password = "WHaNFE5C3qlChqNbAzH4"
# use the credentials provided in the Payment Gateway API docs.
# الرؤوس
headers = {
    "Content-Type": "application/json",
    "X-Terminal-Id": "111111"  # استبدل YOUR_TERMINAL_ID بالمعرّف الخاص بك
}

# unique RequestId 
request_id = str(uuid.uuid4())

# request body
data = {
    "requestId": request_id,
    "amount": 256.89,
    "currency": "IQD",
    "locale": "en_US",
    "finishPaymentUrl": "https://merchant.net/finish",
    "notificationUrl": "https://merchant.net/notification",
}

# Send HTTP request with Basic Auth 
response = requests.post(url, headers=headers, data=json.dumps(data), auth=HTTPBasicAuth(username, password))

# print response
print(response.json())

