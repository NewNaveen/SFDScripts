"""
This script tries to import the required details from JSON file.
It will get you the Spine and leaf switch ip addresses and it's credentials.

"""

import json


class GetSwitchDetails:

    def get_spine_switch_ip(self):
        """
        This function gets the spine switch ip address details from the Json file and store them in a list.
        :return:
        """
        with open('setup1.json', 'r') as f:
            json_text = f.read()
            setup = json.loads(json_text)
            spine_ip = [value['mgmt_ip_address'] for value in setup['topology']['nodes']
                        if value['role'] == 'SPINE']
            return spine_ip

    def spine_switch_count(self):
        """
        This function helps to find the number of spine switches in uploaded topology.
        :return:
        """
        spines = GetSwitchDetails().get_spine_switch_ip()
        totalSpines = len(spines)
        return totalSpines

    def get_spine_credentials(self):
        """
        This function fetches the spine switch credentials from the Input JSON file.
        :return:
        """
        credentials = {}
        with open('setup1.json', 'r') as f:
            json_text = f.read()
            setup = json.loads(json_text)
            for value in setup['topology']['nodes']:
                if value['role'] == 'SPINE':
                    credentials.update({value['mgmt_ip_address'] : value['credential']})
            return credentials

    def get_spine_swithnames(self):
        """
        This function gives the Spine switch names from the input JSON file
        :return:
        """
        switchnames = {}
        with open('setup1.json', 'r') as f:
            json_text = f.read()
            setup = json.loads(json_text)
            for value in setup['topology']['nodes']:
                if value['role'] == "SPINE":
                    switchnames.update({value['mgmt_ip_address'] : value['name']})
            return switchnames


    def get_leaf_switch_ip(self):
        """
        This function gets the Leaf switch ip address details from the Json file and store them in a list.
        :return:
        """
        with open('setup1.json', 'r') as f:
            json_text = f.read()
            setup = json.loads(json_text)
            leaf_ip = [value['mgmt_ip_address'] for value in setup['topology']['nodes'] if value['role'] == 'LEAF']
            return leaf_ip

    def leaf_switch_count(self):
        """
        This function helps to find the number of Leaf switches in uploaded topology.
        :return:
        """
        leafs = GetSwitchDetails().get_leaf_switch_ip()
        totalLeafs = len(leafs)
        return totalLeafs

    def get_leaf_credentials(self):
        """
        This function fetches the Leaf switch credentials from the Input JSON file.
        :return:
        """
        credentials = {}
        with open('setup1.json', 'r') as f:
            json_text = f.read()
            setup = json.loads(json_text)
            for value in setup['topology']['nodes']:
                if value['role'] == 'LEAF':
                    credentials.update({value['mgmt_ip_address'] : value['credential']})
            return credentials

    def get_leaf_swithnames(self):
        """
        This function gives the Leaf switch names from the input JSON file
        :return:
        """
        switchnames = {}
        with open('setup1.json', 'r') as f:
            json_text = f.read()
            setup = json.loads(json_text)
            for value in setup['topology']['nodes']:
                if value['role'] == "LEAF":
                    switchnames.update({value['mgmt_ip_address'] : value['name']})
            return switchnames

    def get_edgeleaf_switch_ip(self):
        """
        This function gets the Edge Leaf switch ip address details from the Json file and store them in a list.
        :return:
        """
        with open('setup1.json', 'r') as f:
            json_text = f.read()
            setup = json.loads(json_text)
            edgeleaf_ip = [value['mgmt_ip_address'] for value in setup['topology']['nodes']
                           if value['role'] == 'EDGE_LEAF']
            return edgeleaf_ip

    def edgeleaf_switch_count(self):
        """
        This function helps to find the number of Edge Leaf switches in uploaded topology.
        :return:
        """
        edgeleafs = GetSwitchDetails().get_edgeleaf_switch_ip()
        totalEdgeLeafs = len(edgeleafs)
        return totalEdgeLeafs

    def get_edgeleaf_credentials(self):
        """
        This function fetches the Leaf switch credentials from the Input JSON file.
        :return:
        """
        credentials = {}
        with open('setup1.json', 'r') as f:
            json_text = f.read()
            setup = json.loads(json_text)
            for value in setup['topology']['nodes']:
                if value['role'] == 'EDGE_LEAF':
                    credentials.update({value['mgmt_ip_address'] : value['credential']})
            return credentials

    def get_edgeleaf_swithnames(self):
        """
        This function gives the Edge Leaf switch names from the input JSON file
        :return:
        """
        switchnames = {}
        with open('setup1.json', 'r') as f:
            json_text = f.read()
            setup = json.loads(json_text)
            for value in setup['topology']['nodes']:
                if value['role'] == "EDGE_LEAF":
                    switchnames.update({value['mgmt_ip_address'] : value['name']})
            return switchnames

    def total_leaf_switches(self):
        """
        This function calculates the total number of leaf switches in the topology including Edge leaf switches.
        :return:
        """
        total = GetSwitchDetails().leaf_switch_count() + GetSwitchDetails().edgeleaf_switch_count()
        return total
"""
if __name__ == '__main__':
    x = GetSwitchDetails()
    print(x.get_spine_switch_ip())
    print(x.get_leaf_switch_ip())
    print(x.get_edgeleaf_switch_ip())
"""