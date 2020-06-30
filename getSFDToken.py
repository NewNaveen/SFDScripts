import requests
import datetime
import logging
import json

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s - %(levelname)s - %(message)s')

SFD_url = "https://10.173.225.212/api/"

body = {"username": "admin@sfd.local",
        "password": "VMware1!"}

x = requests.post(url=f'{SFD_url}auth/token', data=None, json=body, verify=False)
response = x.json()
token = response["token"]
logging.info(token)
print(f'NFC {token}')

api_url = '{0}topology?edge-cloud=true'.format(SFD_url)
headers = {
        'Authorization': 'NFC {}'.format(token),
        'Content-type': 'application/json',
        'Accept': '*/*'}

wiring = requests.get(api_url, headers=headers, verify=False)
y = wiring.json()
print(y)
