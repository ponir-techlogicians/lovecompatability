import requests
import base64
from google.oauth2 import service_account
from google.auth.transport.requests import Request

from datetime import datetime
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime

def parse_apple_datetime(date_str):
    # Convert from Apple-style to ISO 8601
    try:
        dt = datetime.strptime(date_str.replace(' Etc/GMT', ''), "%Y-%m-%d %H:%M:%S")
        return make_aware(dt)
    except Exception as e:
        print("Failed to parse date:", date_str, e)
        return None

def get_google_access_token():
    SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
    # SERVICE_ACCOUNT_FILE = 'crush-o-meter-457507-7be00c722fed.json'
    SERVICE_ACCOUNT_FILE = 'crush-o-meter-457507-f3ae8ffb4892.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    credentials.refresh(Request())
    return credentials.token

def validate_with_apple(receipt_data):
    # SHARED_SECRET = 'b79f0586e69e46a087ebe7864ea04972'
    # SHARED_SECRET = 'c5d1d4e9958d485bbda9ff4bd5a7095f'
    SHARED_SECRET = '04f5330c43ac4fb8b7bc11d2b353ce97'
    PRODUCTION_URL = 'https://buy.itunes.apple.com/verifyReceipt'
    SANDBOX_URL = 'https://sandbox.itunes.apple.com/verifyReceipt'

    payload = {
        'receipt-data': receipt_data['transactionReceipt'],
        'password': SHARED_SECRET
    }

    print(payload)

    # Try production first
    response = requests.post(PRODUCTION_URL, json=payload)
    result = response.json()

    print(result)


    # Fall back to sandbox if needed
    if result.get('status') == 21007 or result.get('status') == 21003:
        response = requests.post(SANDBOX_URL, json=payload)
        print(response.json())
        result = response.json()

    if result.get('status') != 0:
        return None

    latest = result['receipt']['in_app'][-1]

    return {
        'original_transaction_id': latest['original_transaction_id'],
        'product_id': latest['product_id'],
        # 'expires_date': latest['expires_date'],
        # 'auto_renew_status': bool(int(latest.get('is_in_billing_retry_period', '0')))
    }

# def validate_with_apple(receipt_data):
#     SHARED_SECRET = 'c5d1d4e9958d485bbda9ff4bd5a7095f'
#     PRODUCTION_URL = 'https://buy.itunes.apple.com/verifyReceipt'
#     SANDBOX_URL = 'https://sandbox.itunes.apple.com/verifyReceipt'
#
#     if not receipt_data:
#         print("❌ Empty receipt data!")
#         return None
#
#     # Ensure receipt is a base64-encoded string
#     if isinstance(receipt_data['transactionReceipt'], bytes):
#         receipt_data = base64.b64encode(receipt_data).decode('utf-8')
#     elif isinstance(receipt_data, dict):
#         print("❌ Error: receipt_data is a dict; expected string or bytes.")
#         return None
#     elif not isinstance(receipt_data, str):
#         print(f"❌ Error: Invalid receipt_data type: {type(receipt_data)}")
#         return None
#
#     # Log short portion of receipt data
#     print("✅ Sending to Apple production:", receipt_data[:50], "...")
#
#     payload = {
#         'receipt-data': receipt_data,
#         'password': SHARED_SECRET
#     }
#
#     headers = {'Content-Type': 'application/json'}
#
#     # First, try production
#     try:
#         response = requests.post(PRODUCTION_URL, json=payload, headers=headers)
#         result = response.json()
#     except Exception as e:
#         print("❌ Production request failed:", str(e))
#         return None
#
#     print("🔁 Apple production response:", result)
#
#     # Fall back to sandbox if needed
#     if result.get('status') == 21007:
#         print("⚠️ Receipt is from Sandbox. Retrying with sandbox URL...")
#         try:
#             response = requests.post(SANDBOX_URL, json=payload, headers=headers)
#             result = response.json()
#         except Exception as e:
#             print("❌ Sandbox request failed:", str(e))
#             return None
#         print("🧪 Apple sandbox response:", result)
#
#     # If still invalid
#     if result.get('status') != 0:
#         print("❌ Apple receipt validation failed. Status:", result.get('status'))
#         return None
#
#     # Extract latest receipt info
#     try:
#         latest = result['latest_receipt_info'][-1]
#         return {
#             'original_transaction_id': latest['original_transaction_id'],
#             'product_id': latest['product_id'],
#             'expires_date': latest['expires_date'],
#             'auto_renew_status': bool(int(latest.get('is_in_billing_retry_period', '0')))
#         }
#     except Exception as e:
#         print("❌ Error parsing receipt info:", str(e))
#         return None


def validate_with_google(package_name, subscription_id, token):
    access_token = get_google_access_token()  # You need to implement this
    url = f"https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{package_name}/purchases/subscriptions/{subscription_id}/tokens/{token}"
    print('url',url)
    print('access_token:', access_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    print(response.json())

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        'purchaseToken': token,
        'expiryTime': data['expiryTimeMillis'],
        'autoRenewing': data.get('autoRenewing', False)
    }

def get_app_info(response):
    package_name = 'com.crushometer.crushometerapp'
    product_id = 'com.crushometer.unlockcrush'
    purchase_token = response['purchaseToken']