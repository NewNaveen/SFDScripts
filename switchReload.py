
import paramiko
import logging
import time

from SFDScripts.switchDetails import GetSwitchDetails
from SFDScripts.switchUtils import SwitchBasicFunctions

class SwitchReload:

    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("paramiko").setLevel(logging.INFO)

    def spineSwitchReload(self):
        """
        This will help is reloading the spine switches. It will get switch details from the Json file
        in another function.
        :return:
        """
        for ipaddress in GetSwitchDetails().get_spine_switch_ip():
            for value in GetSwitchDetails().get_spine_credentials():
                if value == ipaddress:
                    username = GetSwitchDetails().get_spine_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_spine_credentials()[ipaddress]['password']
                    self.logger.info(f'****** Reloading switch = {ipaddress} ******')
                    connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)

                    connection = connection.invoke_shell()

                    connection.send("reload\n")
                    time.sleep(2)

                    connection.send("yes\n")
                    time.sleep(2)

                    output = connection.recv(65535).decode('utf-8')
                    self.logger.info(output)
                    self.logger.info(f'******* Reloading of switch = {ipaddress} is completed ******')
                    connection.close()


    def leafSwitchReload(self):
        """
        This will help is reloading the spine switches. It will get switch details from the Json file
        in another function.
        :return:
        """
        for ipaddress in GetSwitchDetails().get_leaf_switch_ip():
            for value in GetSwitchDetails().get_leaf_credentials():
                if value == ipaddress:
                    username = GetSwitchDetails().get_leaf_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_leaf_credentials()[ipaddress]['password']
                    self.logger.info(f'****** Reloading switch = {ipaddress} ******')
                    connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)

                    connection = connection.invoke_shell()

                    connection.send("reload\n")
                    time.sleep(2)

                    connection.send("yes\n")
                    time.sleep(2)

                    output = connection.recv(65535).decode('utf-8')
                    self.logger.info(output)
                    self.logger.info(f'******* Reloading of switch = {ipaddress} is completed ******')
                    connection.close()



if __name__ == '__main__':
    x = SwitchReload()
    #x.spineSwitchReload()
    x.leafSwitchReload()
