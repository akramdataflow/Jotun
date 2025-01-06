import requests
import json
import uuid

# URL الخاص بـ API
url = "https://uat-sandbox-3ds-api.qi.iq/api/v1/payment"

# الرؤوس
headers = {
    "Content-Type": "application/json",
    "X-Terminal-Id": "111111"  # استبدل YOUR_TERMINAL_ID بالمعرّف الخاص بك
}

# توليد RequestId جديد
request_id = str(uuid.uuid4())

# بيانات الطلب
data = {
    "requestId": request_id,
    "amount": 256.89,
    "currency": "IQD",
    "locale": "en_US",
    "finishPaymentUrl": "https://merchant.net/finish",
    "notificationUrl": "https://merchant.net/notification",
    "customerInfo": {
        "firstName": "John",
        "middleName": "Mark",
        "lastName": "Doe",
        "phone": "009647xxxxxxxxx",
        "email": "j.doe@gmail.com",
        "accountId": "j.doe",
        "accountNumber": "40817123456787852369",
        "address": "57th street 26",
        "city": "Baghdad",
        "provinceCode": "BGD",
        "countryCode": "IQ",
        "postalCode": "10069",
        "birthDate": "07201985",
        "identificationType": "00",
        "identificationNumber": "4605 555555",
        "identificationCountryCode": "IQ",
        "identificationExpirationDate": "03122024",
        "nationality": "IQ",
        "countryOfBirth": "IQ",
        "fundSource": "01",
        "participantId": "someParticipantId",
        "additionalMessage": "Transfer of funds, excluding VAT",
        "transactionReason": "00",
        "claimCode": "123456789"
    },
    "browserInfo": {
        "browserAcceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "browserIp": "140.82.118.3",
        "browserJavaEnabled": False,
        "browserLanguage": "en-US",
        "browserColorDepth": "24",
        "browserScreenWidth": "1024",
        "browserScreenHeight": "768",
        "browserTZ": "-180",
        "browserUserAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"
    },
    "additionalInfo": {
        "key": "value"
    }
}

# إرسال الطلب
response = requests.post(url, headers=headers, data=json.dumps(data))

# عرض النتيجة
print(response.json())
