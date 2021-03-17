
import logging
import time
import concurrent.futures

from SFDScripts.switchDetails import GetSwitchDetails
from SFDScripts.switchUtils import SwitchBasicFunctions

spine_ip = GetSwitchDetails().get_spine_switch_ip()
leaf_ip = GetSwitchDetails().get_leaf_switch_ip()


class SwitchReload:

    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("paramiko").setLevel(logging.INFO)

    def spineSwitchReload(self, ipaddress):
        """
        This will help is reloading the spine switches. It will get switch details from the Json file
        in another function.
        :return:
        """
        for value in GetSwitchDetails().get_spine_credentials():
            if value == ipaddress:
                username = GetSwitchDetails().get_spine_credentials()[ipaddress]['username']
                password = GetSwitchDetails().get_spine_credentials()[ipaddress]['password']
                self.logger.info(f'****** Reloading switch = {ipaddress} ******')
                connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)

                connection = connection.invoke_shell()

                connection.send("reload\n")
                time.sleep(2)

                connection.send("no\n")
                time.sleep(2)

                connection.send("yes\n")
                time.sleep(2)

                output = connection.recv(65535).decode('utf-8')
                self.logger.info(output)
                self.logger.info(f'******* Reloading of switch = {ipaddress} is completed ******')
                connection.close()


    def leafSwitchReload(self, ipaddress):
        """
        This will help is reloading the spine switches. It will get switch details from the Json file
        in another function.
        :return:
        """
        for value in GetSwitchDetails().get_leaf_credentials():
            if value == ipaddress:
                username = GetSwitchDetails().get_leaf_credentials()[ipaddress]['username']
                password = GetSwitchDetails().get_leaf_credentials()[ipaddress]['password']
                self.logger.info(f'****** Reloading switch = {ipaddress} ******')
                connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)

                connection = connection.invoke_shell()

                connection.send("reload\n")
                time.sleep(2)

                connection.send("no\n")
                time.sleep(2)

                connection.send("yes\n")
                time.sleep(2)

                output = connection.recv(65535).decode('utf-8')
                self.logger.info(output)
                self.logger.info(f'******* Reloading of switch = {ipaddress} is completed ******')
                connection.close()


if __name__ == '__main__':
    x = SwitchReload()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as reload:
        reload.map(x.leafSwitchReload, leaf_ip)
        reload.map(x.spineSwitchReload, spine_ip)
