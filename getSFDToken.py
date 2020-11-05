import requests
import datetime
import logging
import json

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s - %(levelname)s - %(message)s')

SFD_url = "https://10.173.225.215/api/"

body = {"username": "admin@sfd.local",
        "password": "Admin!23"}

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

def get_Draft_fabric_intent():

    token = get_SFD_Token()

    api_url = f'{SFD_url}fabric-intents'
    headers = {
        'Authorization': 'NFC {}'.format(token),
        'Content-type': 'application/json',
        'Accept': '*/*'}

    fabric_intent = requests.get(api_url, headers=headers, verify=False)
    y = fabric_intent.json()
    draft_intent = [key["id"] for key in y["data"] if key["state"]["current_state"] == "DRAFT"]
    if draft_intent:
        print(draft_intent[0])
    else:
        print("There is no Draft Intent on this SFD")
    return draft_intent[0]


def get_switch_info():
    token = get_SFD_Token()

    api_url = f'{SFD_url}switches/summary'
    headers = {
            'Authorization': 'NFC {}'.format(token),
            'Content-type': 'application/json',
            'Accept': '*/*'}

    switch_details = {}
    switch_summary = requests.get(api_url, headers=headers, verify=False)
    y = switch_summary.json()
    for i in y:
        for j in y[i]:
            switch_details.update({j["name"]: j["id"]})
    return switch_details

def l2_vlan_create():

    # fabric_intent_id = input("Enter fabric intent ID: ")
    vlans = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    for vlan in vlans:
        token = get_SFD_Token()

        api_url = f"{SFD_url}fabric-intents/41:52380505177063593/host-networks"
        headers = {
            'Authorization': 'NFC {}'.format(token),
            'Content-type': 'application/json',
            'Accept': '*/*'}

        switch_id_1 = "2:52376670150034965"
        switch_id_2 = "2:52376670154229528"
        svi_ip_1 = f"192.1.{vlan}.2/24"
        svi_ip_2 = f"192.1.{vlan}.3/24"
        vrrp_virtual_ip = f"192.1.{vlan}.1/24"
        name = f"{vlan}"
        description = f"vlan {vlan}"
        data = {
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
            "description": description
        }
        print(data)
        body = data
        #print(body)
        x = requests.post(api_url, headers=headers, data=None, json=body, verify=False)
        print(x.content)


def l3_vlan_create_physical_switches():

    # fabric_intent_id = input("Enter fabric intent ID: ")
    vlans = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    fabric_intent = get_Draft_fabric_intent()
    for vlan in vlans:

        token = get_SFD_Token()

        api_url = f'{SFD_url}fabric-intents/{fabric_intent}/host-networks'
        headers = {
            'Authorization': 'NFC {}'.format(token),
            'Content-type': 'application/json',
            'Accept': '*/*'}

        switch_id_1 = "2:52394049025901583"
        switch_id_2 = "2:52394049030653202"
        switch_id_3 = "2:52394049035306517"
        switch_id_4 = "2:52394049040418584"
        switch_id_5 = "2:52394049045792795"
        switch_id_6 = "2:52394049050052894"
        switch_id_7 = "2:52394049053690401"
        switch_id_8 = "2:52394049057950500"
        switch_id_9 = "2:52394049061325863"
        switch_id_10 = "2:52394049064766762"
        switch_id_11 = "2:52394049069321773"
        switch_id_12 = "2:52394049073221424"
        switch_id_13 = "2:52394049076269107"
        switch_id_14 = "2:52394049079972150"
        switch_id_15 = "2:52394049084068409"
        switch_id_16 = "2:52394049087116092"

        svi_ip_sw1 = f"192.1.{vlan}.2/24"
        svi_ip_sw2 = f"192.1.{vlan}.3/24"
        vrrp_virtual_ip1 = f"192.1.{vlan}.1/24"

        svi_ip_sw3 = f"192.2.{vlan}.2/24"
        svi_ip_sw4 = f"192.2.{vlan}.3/24"
        vrrp_virtual_ip2 = f"192.2.{vlan}.1/24"

        svi_ip_sw5 = f"192.3.{vlan}.2/24"
        svi_ip_sw6 = f"192.3.{vlan}.3/24"
        vrrp_virtual_ip3 = f"192.3.{vlan}.1/24"

        svi_ip_sw7 = f"192.4.{vlan}.2/24"
        svi_ip_sw8 = f"192.4.{vlan}.3/24"
        vrrp_virtual_ip4 = f"192.4.{vlan}.1/24"

        svi_ip_sw9 = f"192.5.{vlan}.2/24"
        svi_ip_sw10 = f"192.5.{vlan}.3/24"
        vrrp_virtual_ip5 = f"192.5.{vlan}.1/24"

        svi_ip_sw11 = f"192.6.{vlan}.2/24"
        svi_ip_sw12 = f"192.6.{vlan}.3/24"
        vrrp_virtual_ip6 = f"192.6.{vlan}.1/24"

        svi_ip_sw13 = f"192.7.{vlan}.2/24"
        svi_ip_sw14 = f"192.7.{vlan}.3/24"
        vrrp_virtual_ip7 = f"192.7.{vlan}.1/24"

        svi_ip_sw15 = f"192.8.{vlan}.2/24"
        svi_ip_sw16 = f"192.8.{vlan}.3/24"
        vrrp_virtual_ip8 = f"192.8.{vlan}.1/24"

        name = f"{vlan}"
        description = f"vlan {vlan}"

        data = {
            "vlan_id": vlan,
            "type": "WORKLOAD_VLAN",
            "data": [
                {
                    "switch_id_1": switch_id_1,
                    "switch_id_2": switch_id_2,
                    "svi_ip_1": svi_ip_sw1,
                    "svi_ip_2": svi_ip_sw2,
                    "vrrp_virtual_ip": vrrp_virtual_ip1
                },
                {
                    "switch_id_1": switch_id_3,
                    "switch_id_2": switch_id_4,
                    "svi_ip_1": svi_ip_sw3,
                    "svi_ip_2": svi_ip_sw4,
                    "vrrp_virtual_ip": vrrp_virtual_ip2
                },
                {
                    "switch_id_1": switch_id_5,
                    "switch_id_2": switch_id_6,
                    "svi_ip_1": svi_ip_sw5,
                    "svi_ip_2": svi_ip_sw6,
                    "vrrp_virtual_ip": vrrp_virtual_ip3
                },
                {
                    "switch_id_1": switch_id_7,
                    "switch_id_2": switch_id_8,
                    "svi_ip_1": svi_ip_sw7,
                    "svi_ip_2": svi_ip_sw8,
                    "vrrp_virtual_ip": vrrp_virtual_ip4
                },
                {
                    "switch_id_1": switch_id_9,
                    "switch_id_2": switch_id_10,
                    "svi_ip_1": svi_ip_sw9,
                    "svi_ip_2": svi_ip_sw10,
                    "vrrp_virtual_ip": vrrp_virtual_ip5
                },
                {
                    "switch_id_1": switch_id_11,
                    "switch_id_2": switch_id_12,
                    "svi_ip_1": svi_ip_sw11,
                    "svi_ip_2": svi_ip_sw12,
                    "vrrp_virtual_ip": vrrp_virtual_ip6
                },
                {
                    "switch_id_1": switch_id_13,
                    "switch_id_2": switch_id_14,
                    "svi_ip_1": svi_ip_sw13,
                    "svi_ip_2": svi_ip_sw14,
                    "vrrp_virtual_ip": vrrp_virtual_ip7
                },
                {
                    "switch_id_1": switch_id_15,
                    "switch_id_2": switch_id_16,
                    "svi_ip_1": svi_ip_sw15,
                    "svi_ip_2": svi_ip_sw16,
                    "vrrp_virtual_ip": vrrp_virtual_ip8
                }
            ],
            "name": name,
            "description": description
        }
        print(data)
        body = data
        #print(body)
        x = requests.post(api_url, headers=headers, data=None, json=body, verify=False)
        print(x.content)

def l3_vlan_create_virtual_switches():

    # fabric_intent_id = input("Enter fabric intent ID: ")
    #vlans = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    fabric_intent = get_Draft_fabric_intent()
    for vlan in range(101, 111):

        token = get_SFD_Token()

        api_url = f'{SFD_url}fabric-intents/{fabric_intent}/host-networks'
        headers = {
            'Authorization': 'NFC {}'.format(token),
            'Content-type': 'application/json',
            'Accept': '*/*'}

        switch_id_1 = "2:52394049091310655"
        switch_id_2 = "2:52394049092686980"
        switch_id_3 = "2:52394049093440713"
        switch_id_4 = "2:52394049094325518"
        switch_id_5 = "2:52394049095079251"
        switch_id_6 = "2:52394049095800216"
        switch_id_7 = "2:52394049096521181"
        switch_id_8 = "2:52394049097274914"
        switch_id_9 = "2:52394049098061415"
        switch_id_10 = "2:52394049098880684"
        switch_id_11 = "2:52394049099601649"
        switch_id_12 = "2:52394049100289846"
        switch_id_13 = "2:52394049101764475"
        switch_id_14 = "2:52394049102780352"
        switch_id_15 = "2:52394049103697925"
        switch_id_16 = "2:52394049104451658"

        svi_ip_sw1 = f"192.1.{vlan}.2/24"
        svi_ip_sw2 = f"192.1.{vlan}.3/24"
        vrrp_virtual_ip1 = f"192.1.{vlan}.1/24"

        svi_ip_sw3 = f"192.2.{vlan}.2/24"
        svi_ip_sw4 = f"192.2.{vlan}.3/24"
        vrrp_virtual_ip2 = f"192.2.{vlan}.1/24"

        svi_ip_sw5 = f"192.3.{vlan}.2/24"
        svi_ip_sw6 = f"192.3.{vlan}.3/24"
        vrrp_virtual_ip3 = f"192.3.{vlan}.1/24"

        svi_ip_sw7 = f"192.4.{vlan}.2/24"
        svi_ip_sw8 = f"192.4.{vlan}.3/24"
        vrrp_virtual_ip4 = f"192.4.{vlan}.1/24"

        svi_ip_sw9 = f"192.5.{vlan}.2/24"
        svi_ip_sw10 = f"192.5.{vlan}.3/24"
        vrrp_virtual_ip5 = f"192.5.{vlan}.1/24"

        svi_ip_sw11 = f"192.6.{vlan}.2/24"
        svi_ip_sw12 = f"192.6.{vlan}.3/24"
        vrrp_virtual_ip6 = f"192.6.{vlan}.1/24"

        svi_ip_sw13 = f"192.7.{vlan}.2/24"
        svi_ip_sw14 = f"192.7.{vlan}.3/24"
        vrrp_virtual_ip7 = f"192.7.{vlan}.1/24"

        svi_ip_sw15 = f"192.8.{vlan}.2/24"
        svi_ip_sw16 = f"192.8.{vlan}.3/24"
        vrrp_virtual_ip8 = f"192.8.{vlan}.1/24"

        name = f"{vlan}"
        description = f"vlan {vlan}"

        data = {
            "vlan_id": vlan,
            "type": "WORKLOAD_VLAN",
            "data": [
                {
                    "switch_id_1": switch_id_1,
                    "switch_id_2": switch_id_2,
                    "svi_ip_1": svi_ip_sw1,
                    "svi_ip_2": svi_ip_sw2,
                    "vrrp_virtual_ip": vrrp_virtual_ip1
                },
                {
                    "switch_id_1": switch_id_3,
                    "switch_id_2": switch_id_4,
                    "svi_ip_1": svi_ip_sw3,
                    "svi_ip_2": svi_ip_sw4,
                    "vrrp_virtual_ip": vrrp_virtual_ip2
                },
                {
                    "switch_id_1": switch_id_5,
                    "switch_id_2": switch_id_6,
                    "svi_ip_1": svi_ip_sw5,
                    "svi_ip_2": svi_ip_sw6,
                    "vrrp_virtual_ip": vrrp_virtual_ip3
                },
                {
                    "switch_id_1": switch_id_7,
                    "switch_id_2": switch_id_8,
                    "svi_ip_1": svi_ip_sw7,
                    "svi_ip_2": svi_ip_sw8,
                    "vrrp_virtual_ip": vrrp_virtual_ip4
                },
                {
                    "switch_id_1": switch_id_9,
                    "switch_id_2": switch_id_10,
                    "svi_ip_1": svi_ip_sw9,
                    "svi_ip_2": svi_ip_sw10,
                    "vrrp_virtual_ip": vrrp_virtual_ip5
                },
                {
                    "switch_id_1": switch_id_11,
                    "switch_id_2": switch_id_12,
                    "svi_ip_1": svi_ip_sw11,
                    "svi_ip_2": svi_ip_sw12,
                    "vrrp_virtual_ip": vrrp_virtual_ip6
                },
                {
                    "switch_id_1": switch_id_13,
                    "switch_id_2": switch_id_14,
                    "svi_ip_1": svi_ip_sw13,
                    "svi_ip_2": svi_ip_sw14,
                    "vrrp_virtual_ip": vrrp_virtual_ip7
                },
                {
                    "switch_id_1": switch_id_15,
                    "switch_id_2": switch_id_16,
                    "svi_ip_1": svi_ip_sw15,
                    "svi_ip_2": svi_ip_sw16,
                    "vrrp_virtual_ip": vrrp_virtual_ip8
                }
            ],
            "name": name,
            "description": description
        }
        print(data)
        body = data
        #print(body)
        x = requests.post(api_url, headers=headers, data=None, json=body, verify=False)
        print(x.content)


def l3_vlan_create_2switches():

    # fabric_intent_id = input("Enter fabric intent ID: ")
    # vlans = [210, 220, 230, 240, 250, 260, 270, 280, 290]

    for vlan in range(21, 31):

        token = get_SFD_Token()

        api_url = f"{SFD_url}fabric-intents/41:52383150157562067/host-networks"
        headers = {
            'Authorization': 'NFC {}'.format(token),
            'Content-type': 'application/json',
            'Accept': '*/*'}

        switch_id_1 = "2:52383099665449111"
        switch_id_2 = "2:52383099666497726"

        svi_ip_sw1 = f"192.168.{vlan}.2/24"
        svi_ip_sw2 = f"192.168.{vlan}.3/24"
        vrrp_virtual_ip1 = f"192.168.{vlan}.1/24"

        name = f"{vlan}"
        description = f"vlan {vlan}"

        data = {
            "vlan_id": vlan,
            "type": "WORKLOAD_VLAN",
            "data": [
                {
                    "switch_id_1": switch_id_1,
                    "switch_id_2": switch_id_2,
                    "svi_ip_1": svi_ip_sw1,
                    "svi_ip_2": svi_ip_sw2,
                    "vrrp_virtual_ip": vrrp_virtual_ip1
                }
            ],
            "name": name,
            "description": description
        }
        print(data)
        body = data
        #print(body)
        x = requests.post(api_url, headers=headers, data=None, json=body, verify=False)
        print(x.content)


if __name__ == '__main__':
    #l3_vlan_create_2switches()
    #l3_vlan_create_physical_switches()
    l3_vlan_create_virtual_switches()
    #get_Draft_fabric_intent()

"""
        svi_ip_sw1 = f"192.1.{vlan}.2/24"
        svi_ip_sw2 = f"192.1.{vlan}.3/24"
        vrrp_virtual_ip1 = f"192.1.{vlan}.1/24"


        svi_ip_sw3 = f"192.2.{vlan}.2/24"
        svi_ip_sw4 = f"192.2.{vlan}.3/24"
        vrrp_virtual_ip2 = f"192.2.{vlan}.1/24"

        svi_ip_sw5 = f"192.3.{vlan}.2/24"
        svi_ip_sw6 = f"192.3.{vlan}.3/24"
        vrrp_virtual_ip3 = f"192.3.{vlan}.1/24"

        svi_ip_sw7 = f"192.4.{vlan}.2/24"
        svi_ip_sw8 = f"192.4.{vlan}.3/24"
        vrrp_virtual_ip4 = f"192.4.{vlan}.1/24"

        svi_ip_sw9 = f"192.5.{vlan}.2/24"
        svi_ip_sw10 = f"192.5.{vlan}.3/24"
        vrrp_virtual_ip5 = f"192.5.{vlan}.1/24"
        """