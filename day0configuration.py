"""
This code will do the day0 configuration on the SFD topology that is being imported.

As of now we have to manually copy/put the JSON file into the code folder so that the
Script will get the switch details and the input from the JSON instead of supplying them manually.

Author: Naveen Raju
"""

import paramiko
import time
import logging


from SFDScripts.switchDetails import GetSwitchDetails
from SFDScripts.switchUtils import SwitchBasicFunctions

class SwitchConfiguration:

    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("paramiko").setLevel(logging.INFO)


    commands = ['configure terminal\n', 'logging server 10.173.225.211 severity log-debug\n', 'logging enable\n',
                'ntp server 10.172.40.1\n', 'ntp server 10.172.40.2\n', 'clock timezone standard-timezone GMT0\n']
    """
    def test(self):
        for cmd in self.commands:
            print(cmd)
    """

    def day0_spine_configuration(self):
        for ipaddress in GetSwitchDetails().get_spine_switch_ip():
            for value in GetSwitchDetails().get_spine_credentials():
                if value == ipaddress:
                    username = GetSwitchDetails().get_spine_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_spine_credentials()[ipaddress]['password']
                    self.logger.info(f"Running commands on the switch = {ipaddress} ")
                    connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)
                    connection.invoke_shell()
                    for command in self.commands:
                        connection.send(command)
                        time.sleep(2)

                    connection.send('exit\n')
                    time.sleep(2)

                    connection.send('write memory\n')
                    time.sleep(2)

                    connection.close()
                    self.logger.info(f"***** configuration completed for switch {ipaddress} *****")

    def day0_leaf_configuration(self):
        for ipaddress in GetSwitchDetails().get_leaf_switch_ip():
            for value in GetSwitchDetails().get_leaf_credentials():
                if value == ipaddress:
                    username = GetSwitchDetails().get_leaf_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_leaf_credentials()[ipaddress]['password']
                    self.logger.info(f"Running commands on the switch = {ipaddress} ")
                    connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)
                    connection.invoke_shell()
                    for command in self.commands:
                        connection.send(command)
                        time.sleep(2)

                    connection.send('exit\n')
                    time.sleep(2)

                    connection.send('write memory\n')
                    time.sleep(2)

                    connection.close()
                    self.logger.info(f"***** configuration completed for switch {ipaddress} *****")

if __name__ == '__main__':
    x = SwitchConfiguration()
    x.day0_spine_configuration()
    x.day0_leaf_configuration()

