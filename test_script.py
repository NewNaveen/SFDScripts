import paramiko
import logging
import time
import re

from SFDScripts.switchUtils import SwitchBasicFunctions
from SFDScripts.switchDetails import GetSwitchDetails


class Test:
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("paramiko").setLevel(logging.INFO)

    def SpineuPBgpNeighbors(self):
        """
        Writing this code to verify the UP BGP neighbors on the spine switch

        We can write the count logic by using the list comprehension also by using the below code

        result = [line for line in output.splitlines() if ("Idle" in line) or ("Connect" in line)]
        The output is stored in list and assigned to the result variable
        check the length of result and compare it with the count of Leaf switches.

        :return:
        """
        cmd = "show ip bgp summary"
        for ipaddress in GetSwitchDetails().get_spine_switch_ip():
            for value in GetSwitchDetails().get_spine_credentials():
                if value == ipaddress:
                    hostname = GetSwitchDetails().get_spine_swithnames()[ipaddress]
                    username = GetSwitchDetails().get_spine_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_spine_credentials()[ipaddress]['password']
                    print(hostname)


x = Test()
x.SpineuPBgpNeighbors()