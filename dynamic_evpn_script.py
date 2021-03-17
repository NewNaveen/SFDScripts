import requests
import json

body = {
    "username": "admin@sfd.local",
    "password": "Admin!23"
}

url = input("enter sfd ip   : ")
wiring_id = input("enter wiring id   : ")
fabric_num = input("enter fabric intent id , take details from inspect    : ")
enter_tenant_id = input("enter tenant id , take details from inspect    : ")


def get_token():
    x = requests.post("https://{}/api/auth/token".format(url), data=None, json=body, verify=False)
    token = (json.loads(x.content.decode('utf-8'))['token'])
    return token


def get_topology(wiring_id):
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'NFC {}'.format(get_token())
    }
    x = requests.get("https://{}/api/wiring-diagrams/{}/topology".format(url, wiring_id), headers=header,
                     data=None, json=None, verify=False)
    topology = json.loads(x.content.decode('utf-8'))
    return topology


def get_leaf_pair_position():
    topology = get_topology(wiring_id)
    switch_id_name = {}
    for i in range(201, 261):
        for position in topology['switches']:
            if position['position'] == i:
                switch_id_name.update({position['id']: position['name']})
    for i in range(501, 503):
        for position in topology['switches']:
            if position['position'] == i:
                switch_id_name.update({position['id']: position['name']})
    return switch_id_name


switch_name_list = get_leaf_pair_position()
switch_id_list = list(switch_name_list.keys())


def create_host_network():
    vxlan_input = []
    for vxlan in range(10000, 16000, 500):
        data = []
        vlan = int(vxlan / 500)
        for switch in range(8, 15, 2):
            switch1 = switch_id_list[switch]
            switch2 = switch_id_list[switch + 1]
            switch1_name = switch_name_list[switch1]
            switch2_name = switch_name_list[switch2]
            data.append({
                "switch_id_1": switch1,
                "switch_1_name": switch1_name,
                "switch_id_2": switch2,
                "switch_2_name": switch2_name,
                "svi_ip_1": '173.1.{}.{}/24'.format(vlan, (switch + 1)),
                "svi_ip_2": '173.1.{}.{}/24'.format(vlan, (switch + 2)),
                "vtep_ip": None,
                "vlan_id": vlan

            })

        vxlan_input.append({
            "vni": vxlan,
            "static_anycast_gateway_ip_address": '173.1.{}.254/24'.format(vlan),
            "vlan_type": "WORKLOAD_VLAN",
            "switch_pairs": data,
            "description": 'vxlan_{}'.format(vxlan)
        })

    for vxlan in range(21000, 26000, 500):
        data = []
        vlan = int(vxlan / 500)
        for switch in range(20, 39, 2):
            switch1 = switch_id_list[switch]
            switch2 = switch_id_list[switch + 1]
            switch1_name = switch_name_list[switch1]
            switch2_name = switch_name_list[switch2]
            data.append({
                "switch_id_1": switch1,
                "switch_1_name": switch1_name,
                "switch_id_2": switch2,
                "switch_2_name": switch2_name,
                "svi_ip_1": '173.1.{}.{}/24'.format(vlan, (switch + 1)),
                "svi_ip_2": '173.1.{}.{}/24'.format(vlan, (switch + 2)),
                "vtep_ip": None,
                "vlan_id": vlan

            })

        vxlan_input.append({
            "vni": vxlan,
            "static_anycast_gateway_ip_address": '173.1.{}.254/24'.format(vlan),
            "vlan_type": "WORKLOAD_VLAN",
            "switch_pairs": data,
            "description": 'vxlan_{}'.format(vxlan)
        })

    for vxlan in range(41000, 46000, 500):
        data = []
        vlan = int(vxlan / 500)
        for switch in range(40, 59, 2):
            switch1 = switch_id_list[switch]
            switch2 = switch_id_list[switch + 1]
            switch1_name = switch_name_list[switch1]
            switch2_name = switch_name_list[switch2]
            data.append({
                "switch_id_1": switch1,
                "switch_1_name": switch1_name,
                "switch_id_2": switch2,
                "switch_2_name": switch2_name,
                "svi_ip_1": '173.1.{}.{}/24'.format(vlan, (switch + 1)),
                "svi_ip_2": '173.1.{}.{}/24'.format(vlan, (switch + 2)),
                "vtep_ip": None,
                "vlan_id": vlan

            })

        vxlan_input.append({
            "vni": vxlan,
            "static_anycast_gateway_ip_address": '173.1.{}.254/24'.format(vlan),
            "vlan_type": "WORKLOAD_VLAN",
            "switch_pairs": data,
            "description": 'vxlan_{}'.format(vxlan)
        })
    for vxlan in range(51000, 53000, 500):
        data = []
        vlan = int(vxlan / 500)
        for switch in range(0, 59, 2):
            switch1 = switch_id_list[switch]
            switch2 = switch_id_list[switch + 1]
            switch1_name = switch_name_list[switch1]
            switch2_name = switch_name_list[switch2]
            data.append({
                "switch_id_1": switch1,
                "switch_1_name": switch1_name,
                "switch_id_2": switch2,
                "switch_2_name": switch2_name,
                "svi_ip_1": '173.1.{}.{}/24'.format(vlan, (switch + 1)),
                "svi_ip_2": '173.1.{}.{}/24'.format(vlan, (switch + 2)),
                "vtep_ip": None,
                "vlan_id": vlan

            })

        vxlan_input.append({
            "vni": vxlan,
            "static_anycast_gateway_ip_address": '173.1.{}.254/24'.format(vlan),
            "vlan_type": "WORKLOAD_VLAN",
            "switch_pairs": data,
            "description": 'vxlan_{}'.format(vxlan)
        })
    return vxlan_input


# print(json.dumps(create_host_network(),indent=1))

def hostnetwork(fabric_id, tenant_id):
    host_network = create_host_network()
    for data in host_network:
        body = data
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'NFC {}'.format(get_token())
        }
        x = requests.post(
            "https://{}/api/fabric-intents/{}/tenants/{}/vxlan-segments".format(url, fabric_id, tenant_id),
            headers=header,
            data=None, json=body, verify=False)
        print(x)


hostnetwork(fabric_num, enter_tenant_id)
