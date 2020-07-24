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

def get_SFD_Token():
    x = requests.post(url=f'{SFD_url}auth/token', data=None, json=body, verify=False)
    response = x.json()
    token = response["token"]
    logging.info(token)
    # print(f'NFC {token}')
    return token


def get_Active_fabric_intent():
    token = get_SFD_Token()

    api_url = f'{SFD_url}fabric-intents'
    headers = {
            'Authorization': 'NFC {}'.format(token),
            'Content-type': 'application/json',
            'Accept': '*/*'}

    fabric_intent = requests.get(api_url, headers=headers, verify=False)
    y = fabric_intent.json()
    active_intent = [key["id"] for key in y["data"] if key["state"]["current_state"] == "ACTIVE"]
    return active_intent

def get_switch_info():
    token = get_SFD_Token()

    api_url = f'{SFD_url}switches/summary'
    headers = {
            'Authorization': 'NFC {}'.format(token),
            'Content-type': 'application/json',
            'Accept': '*/*'}

    switch_details= {}
    switch_summary = requests.get(api_url, headers=headers, verify=False)
    y = switch_summary.json()
    for i in y:
        for j in y[i]:
            switch_details.update({j["name"]: j["id"]})
    return switch_details


if __name__ == '__main__':
    print(get_switch_info())
    print(get_Active_fabric_intent())
