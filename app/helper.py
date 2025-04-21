import requests

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
    SERVICE_ACCOUNT_FILE = 'crush-o-meter-457507-7be00c722fed.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    credentials.refresh(Request())
    return credentials.token

def validate_with_apple(receipt_data):
    # SHARED_SECRET = 'b79f0586e69e46a087ebe7864ea04972'
    SHARED_SECRET = 'c5d1d4e9958d485bbda9ff4bd5a7095f'
    PRODUCTION_URL = 'https://buy.itunes.apple.com/verifyReceipt'
    SANDBOX_URL = 'https://sandbox.itunes.apple.com/verifyReceipt'

    payload = {
        'receipt-data': receipt_data,
        'password': SHARED_SECRET
    }

    # print(payload)

    # Try production first
    response = requests.post(PRODUCTION_URL, json=payload)
    result = response.json()



    # Fall back to sandbox if needed
    if result.get('status') == 21007 or result.get('status') == 21003:
        response = requests.post(SANDBOX_URL, json=payload)
        result = response.json()

    if result.get('status') != 0:
        return None

    latest = result['latest_receipt_info'][-1]

    return {
        'original_transaction_id': latest['original_transaction_id'],
        'product_id': latest['product_id'],
        'expires_date': latest['expires_date'],
        'auto_renew_status': bool(int(latest.get('is_in_billing_retry_period', '0')))
    }


def validate_with_google(package_name, subscription_id, token):
    access_token = get_google_access_token()  # You need to implement this
    url = f"https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{package_name}/purchases/subscriptions/{subscription_id}/tokens/{token}"

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        'purchaseToken': token,
        'expiryTime': data['expiryTimeMillis'],
        'autoRenewing': data.get('autoRenewing', False)
    }
