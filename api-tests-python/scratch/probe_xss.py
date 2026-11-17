import sys, os
sys.path.insert(0, os.path.abspath("."))
import urllib3
urllib3.disable_warnings()
from config import Config
from client.api_client import BayMaxApiClient

client = BayMaxApiClient(Config.BASE_URL)
client.login(Config.USERNAME, Config.PASSWORD)
payload = "<script>alert('VULNERABLE')</script>"
resp = client.get('/api/clinic/visits', params={'date': payload})
print('Status:', resp.status_code)
print('Headers Content-Type:', resp.headers.get('Content-Type'))
print('Body:', resp.text)
