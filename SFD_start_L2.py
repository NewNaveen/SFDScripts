#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:48:51 2020

@author: hsheng

Set up a baseline to load a template/performance testing.
little change can help different testbed, switch name part needs manually change....
"""

import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# below are the data we pre-defined, only modify data at one file
username, password = 'admin@sfd.local', 'VMware1!'
url_base = 'https://10.173.225.212/api/'

# tb_06
json_file = 'TB06_32_S2_L28_Edge2_L2.json'
sw_name = ['sc2-t6-S5232F-L1', "sc2-t6-S5232F-L2", "sc2-t6-S5232F-L3", "sc2-t6-S5232F-L4", "sc2-t6-S5232F-L5",
           "sc2-t6-S5232F-L6", "sc2-t6-S5232F-L7", "sc2-t6-S5232F-L8", "sc2-t6-S5232F-L9", "sc2-t6-S5232F-L10",
           "sc2-t6-S5232F-L11", "sc2-t6-S5232F-L12", "sc2-t6-S5232F-L13", "sc2-t6-S5232F-L14", "sc2-t6-S5232F-L15",
           "sc2-t6-S5232F-L16", "V-Leaf-102", "V-Leaf-102", "V-Leaf-103", "V-Leaf-104", "V-Leaf-105", "V-Leaf-106",
           "V-Leaf-107", "V-Leaf-108", "V-Leaf-109", "V-Leaf-110", "V-Leaf-111", "V-Leaf-112"]


def welcome():
    print("SFD is starting loading stuff....\n")


def get_token(username, password, url_base):
    data = "{\n\
        \"username\":" + "\"" + username + "\"" + ",\n\
            \"password\":" "\"" + password + "\"" + ",\n\
                \"authDomain\": \"LOCAL_AUTH\"\n}"

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Accept': '*/*'
    }
    api_url = '{0}auth/token'.format(url_base)
    r = requests.post(url=api_url, data=data, headers=headers, verify=False)
    j = json.loads(r.text)

    if r.status_code == 200:
        return j['token']

    else:
        return "Getting token failed"


token = get_token(username, password, url_base)


def upload_json(token, url_base, json_file):
    api_url = '{0}wiring-diagrams'.format(url_base)
    headers = {
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }

    files = {'designFile': open(json_file, 'rb')}
    response = requests.post(api_url, headers=headers, files=files, verify=False)
    print(response.ok)
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
        return "wiring diagram has been uploaded\n"
    else:
        return response.status_code, response.json(), "failed to upload wiring diagram\n"


def get_wiring_diagram():
    api_url = '{}wiring-diagrams/summary'.format(url_base)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }
    response = requests.get(api_url, headers=headers, verify=False)
    j = json.loads(response.text)

    if response.status_code == 200 or response.status_code == 202:
        return j['data'][0]['id']
    else:
        return response.status_code, "failed to get fabric-intents\n"


def get_wiring_id():
    wiring_id = get_wiring_diagram()
    return wiring_id


def create_fabric_intent(wiring_id):
    api_url = '{0}fabric-intents'.format(url_base)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }

    body = {
        "name": "start_test1",
        "description": "start_test",
        "wiring_diagram_id": wiring_id
    }
    response = requests.post(api_url, headers=headers, data=None, json=body, verify=False)
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
        return "fabric-intent has been created\n"
    else:
        return response.status_code, "failed to create fabric-intents\n"


def get_fabric_id():
    api_url = '{0}fabric-intents/'.format(url_base)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }
    response = requests.get(api_url, headers=headers, verify=False)
    j = json.loads(response.text)
    print(j)

    if response.status_code == 200 or response.status_code == 202:
        output = j['data']
        for d in output:
            if d['state']['current_state'] == 'DRAFT':
                return d['id']
    else:
        return response.status_code, "failed to get fabric-id"


def create_interlink(fabric_id):
    api_url = '{0}fabric-intents/{1}/interlinks'.format(url_base, fabric_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }

    body = {
        "name": "string",
        "type": "L2_VLT",
        "L3_BGP": {
            "ufd": True,
            "rstp": True,
            "mtu": 1500,
            "interlink_subnet": {
                "address": "192.168.0.0",
                "prefix_len": 16
            },
            "loopback_seed_address": {
                "address": "50.0.0.0",
                "prefix_len": 32
            },
            "bgp": {
                "type": "eBGP",
                "as_leaf_range": [
                    {
                        "start": 64801,
                        "end": 64928
                    }
                ],
                "as_spine_range": [
                    {
                        "start": 64601,
                        "end": 64616
                    }
                ]
            }
        },
        "L2_VLT": {
            "ufd": True,
            "mtu": 1500,
            "edge_interlink_ebgp": {
                "interlink_subnet": {
                    "address": "192.168.0.0",
                    "prefix_len": 16
                },
                "loopback_seed_address": {
                    "address": "50.0.0.0",
                    "prefix_len": 32
                },
                "bgp": {
                    "type": "eBGP",
                    "as_leaf_range": [
                        {
                            "start": 64801,
                            "end": 64928
                        }
                    ],
                    "as_spine_range": [
                        {
                            "start": 64601,
                            "end": 64616
                        }
                    ]
                }
            }
        }
    }
    response = requests.post(api_url, headers=headers, data=None, json=body, verify=False)
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
        return "interlink has been created\n"
    else:
        return response.status_code, response.text, "failed to create interlink\n"


def get_switch_id(fabric_id, sw_1, sw_2):
    global switch_id_1, switch_id_2
    api_url = '{0}fabric-intents/{1}/configurations'.format(url_base, fabric_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }
    response = requests.get(api_url, headers=headers, verify=False)
    j = json.loads(response.text)
    for sw_dict in j['switches']:
        if sw_dict['name'] == sw_1:
            switch_id_1 = sw_dict['id']
        if sw_dict['name'] == sw_2:
            switch_id_2 = sw_dict['id']
    return switch_id_1, switch_id_2


def add_vlan(fabric_id, switch_id_1, switch_id_2, vlans):
    api_url = '{0}fabric-intents/{1}/host-networks'.format(url_base, fabric_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(token),
        'cache-control': "no-cache",
        'Accept': '*/*'
    }

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


# create a table to store switch_name matching vlans
def create_table():
    d = {}
    #    vlans= [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    vlans = [10, 11, 12, 13, 14]
    for i in range(0, len(sw_name) - 1, 2):
        d[sw_name[i], sw_name[i + 1]] = vlans
        vlans = list(map(lambda x: x + 10, vlans))
    return d


def SFD_start():
    welcome()
    print(upload_json(token, url_base, json_file))
    wiring_id = get_wiring_id()
    print(wiring_id)
    create_fabric_intent(wiring_id)
    fabric_id = get_fabric_id()
    print(fabric_id)
    x = create_interlink(fabric_id)
    print(x)

    table = create_table()
    for x, y in table.items():
        sw_1, sw_2 = x
        vlans = y
        switch_id_1, switch_id_2 = get_switch_id(fabric_id, sw_1, sw_2)
        add_vlan(fabric_id, switch_id_1, switch_id_2, vlans)


#    fi.approve_fabric_intent(fabric_id)
#    fi.deploy_fabric_intent(fabric_id)


if __name__ == '__main__':
    SFD_start()





