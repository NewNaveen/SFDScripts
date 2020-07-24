
import logging
import time
import re

from SFDScripts.switchUtils import SwitchBasicFunctions
from SFDScripts.switchDetails import GetSwitchDetails


class VerifyBGPConfig:

    logger = logging.getLogger("naveen")
    logging.basicConfig(level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s')

    def countLeafBgpneighbors(self):

        count = GetSwitchDetails().leaf_switch_count() + GetSwitchDetails().edgeleaf_switch_count()
        return count

    def configuredBGPneighbors(self, output):

        """
        This function will count the number of configured BGP neighbors on the switches.
        :param output:
        :return:
        """
        # The below regex matches ip address x.x.x.x pattern and gives the output

        regex = re.findall(r'\d*\.\d*\.\d*\.\d*', output)

        if len(regex) > 0:
            del regex[0]
            count = len(regex)
        else:
            count = len(regex)
        return count

    def downbgpneighbors(self, output):

        """
        This function will verify how many up bgp neighbors are there are spine switches.
        :param output:
        :return:
        """

        result = [line for line in output.splitlines() if ("Idle" in line) or ("Connect" in line)]
        count = len(result)
        return count

    def spineBgpConfig(self):
        """
        This one try to get the number of bgp neighbors on Spine switches
        :return:
        """
        cmd = "show ip bgp summary"
        for ipaddress in GetSwitchDetails().get_spine_switch_ip():
            for value in GetSwitchDetails().get_spine_credentials():
                if value == ipaddress:
                    hostname = GetSwitchDetails().get_spine_swithnames()[ipaddress]
                    username = GetSwitchDetails().get_spine_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_spine_credentials()[ipaddress]['password']
                    connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)
                    ssh_stdin, ssh_stdout, ssh_stderr = connection.exec_command(cmd)
                    self.logger.info(f'Executing command = {cmd} on switch = {hostname} with ipaddress = {ipaddress}')
                    output = ssh_stdout.read().decode('utf-8')
                    connection.close()

                    # the below piece of code is to check configured BGP Neighbors
                    bgp_neighbors = VerifyBGPConfig().configuredBGPneighbors(output)
                    self.logger.info(f'There are {bgp_neighbors} BGP neighbors CONFIGURED on the Switch = {hostname}')
                    if bgp_neighbors == VerifyBGPConfig().countLeafBgpneighbors():
                        self.logger.info(f'Configured BGP Neighbors on Switch {hostname} ipaddress = {ipaddress} '
                                         f'matches Leaf switch count')
                    else:
                        self.logger.info(f'Configured BGP Neighbors on Switch {hostname} ipaddress = {ipaddress} '
                                         f'Does not matches Leaf switch count')

                    # Below piece of code is to verify up bgp neighbors
                    if int(bgp_neighbors) > 0:

                        down_bgp_neighbors = VerifyBGPConfig().downbgpneighbors(output)
                        self.logger.info(f'There are {down_bgp_neighbors} BGP Down neighbors on Spine {hostname} '
                                         f'ipaddress = {ipaddress}')

                        upneighbors = VerifyBGPConfig().countLeafBgpneighbors() - down_bgp_neighbors
                        self.logger.info(f'There are {upneighbors} BGP up Neighbors on switch {hostname} '
                                         f'ipaddress = {ipaddress}')
                        if upneighbors == VerifyBGPConfig().countLeafBgpneighbors():
                            self.logger.info(f'BGP Up neighbors on Spine = {hostname} ipaddress = {ipaddress} matches '
                                             f'Leaf switch count')
                        else:
                            self.logger.info(f'BGP Up neighbors on Spine = {hostname} ipaddress = {ipaddress} Does not '
                                             f'matches Leaf switch count')
                    else:
                        self.logger.info(f'There are no BGP neighbors configured on Spine = {hostname} '
                                         f'ipaddress = {ipaddress}')



if __name__ == '__main__':
    x = VerifyBGPConfig()
    x.spineBgpConfig()
