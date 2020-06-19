import paramiko
import logging
import time
import re

from SFDScripts.switchUtils import SwitchBasicFunctions
from SFDScripts.switchDetails import GetSwitchDetails


class VerifyDeployedConfig:
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("paramiko").setLevel(logging.INFO)

    def spineBgpConfig(self):
        """
        This one try to get the number of bgp neighbors on Spine switches
        :return:
        """
        cmd = "show ip bgp summary"
        for ipaddress in GetSwitchDetails().get_spine_switch_ip():
            for value in GetSwitchDetails().get_spine_credentials():
                if value == ipaddress:
                    username = GetSwitchDetails().get_spine_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_spine_credentials()[ipaddress]['password']
                    connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)
                    ssh_stdin, ssh_stdout, ssh_stderr = connection.exec_command(cmd)
                    self.logger.info(f'Executing command = {cmd} on switch = {ipaddress}')
                    output = ssh_stdout.read().decode('utf-8')
                    connection.close()
                    regex = re.findall(r'\d*\.\d*\.\d*\.\d*', output)
                    del regex[0]
                    count = len(regex)
                    if count == VerifyDeployedConfig().countLeafBgpneighbors():
                        self.logger.info(f'Configured BGP Neighbors on Switch {ipaddress} matches Leaf switch count')
                    else:
                        self.logger.info(f'Configured BGP Neighbors on Switch {ipaddress} Does not matches Leaf '
                                         f'switch count')
                    self.logger.info(count)

    def countLeafBgpneighbors(self):

        count = GetSwitchDetails().leaf_switch_count() + GetSwitchDetails().edgeleaf_switch_count()
        return count



if __name__ == '__main__':
    x = VerifyDeployedConfig()
    x.spineBgpConfig()
