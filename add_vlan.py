#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 16:29:33 2020

@author: hsheng

get fabric-intent is very important for "next step" action, as our API format required fabric-intents/{id}
"""

import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_url_base = 'https://10.173.225.211/api/'


# get token to authorize
def get_token(username, password):
    body = {
        "username": username,
        "password": password,
        "authDomain": "LOCAL_AUTH"
    }

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Accept': '*/*'
    }

    api_url = '{0}auth/token'.format(api_url_base)
    response = requests.post(api_url, headers=headers, data=None, json=body, verify=False)

    j = json.loads(response.text)

    if response.status_code == 200:
        return j['token']

    else:
        return "Getting token failed", response.text


token = get_token("admin@sfd.local", "Admin!23")


##func to get fabric intents
def get_fabric_intents():
    api_url = '{0}fabric-intents/'.format(api_url_base)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }
    response = requests.get(api_url, headers=headers, verify=False)
    j = json.loads(response.text)

    if response.status_code == 200 or response.status_code == 202:
        return j['data']
    else:
        return response.status_code, "failed to get fabric-intents"


# only get the last one since we are not going to use all the fabric_intent_id
list = get_fabric_intents()
for dict in list:
    if dict['state']['current_state'] == 'DRAFT':
        fabric_intent_id = dict['id']


# func to get interlinks info
def get_switch_id():
    api_url = '{0}fabric-intents/{1}/configuration'.format(api_url_base, fabric_intent_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }
    response = requests.get(api_url, headers=headers, verify=False)
    j = json.loads(response.text)

    if response.status_code == 200 or response.status_code == 202:
        return j['switches']
    else:
        return response.status_code, "failed to get fabric config"


config_list = get_switch_id()
for sw_dict in config_list:
    if sw_dict['name'] == 'sc2-t6-S5232F-L1':
        switch_id_1 = sw_dict['id']
    if sw_dict['name'] == 'sc2-t6-S5232F-L2':
        switch_id_2 = sw_dict['id']


# func to add vlan
def add_vlan():
    api_url = '{0}fabric-intents/{1}/host-networks'.format(api_url_base, fabric_intent_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }

    vlans = [10, 11, 12, 13, 14, 15, 16]
    for vlan in vlans:
        svi_ip_1 = "172.16.{}.1/24".format(vlan)
        svi_ip_2 = "172.16.{}.2/24".format(vlan)
        vrrp_virtual_ip = "172.16.{}.253/24".format(vlan)
        name = "{}".format(vlan)
        body = {
            "vlan_id": vlan,
            "type": "WORKLOAD_VLAN",
            "data": [
                {
                    "switch_id_1": switch_id_1,
                    "switch_id_2": switch_id_2,
                    "svi_ip_1": svi_ip_1,
                    "svi_ip_2": svi_ip_2,
                    "vrrp_virtual_ip": vrrp_virtual_ip
                }
            ],
            "name": name,
            "description": " "
        }
        response = requests.post(api_url, headers=headers, data=None, json=body, verify=False)

        if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
            print("vlan {} have been added".format(vlan))
        else:
            return response.status_code, response.text, "failed to add vlan"

add_vlan()

