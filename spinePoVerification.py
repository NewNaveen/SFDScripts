
import re
import logging
from SFDScripts.switchDetails import GetSwitchDetails
from SFDScripts.switchUtils import SwitchBasicFunctions


class SpinePoVerification:

    logger = logging.getLogger("naveen")
    logging.basicConfig(level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s')

    def configuredPortChannels(self, output):
        """
        By using regular expression we are going to count the number of port-channels on each switch and returning
        the output
        :param output:
        :return:
        """

        regex = re.compile(r'port-channel[1-60]')
        """
        The Above regex matches the string starts with port-channel and any number between 1 & 60 and stores the output 
        in a list.
        """
        result = regex.findall(output, re.MULTILINE)
        count = len(result)
        return count

    def upPortChannels(self, output):
        """
        By using regular expression we are going to count the number of UP port-channels on each switch and returning
        the output
        :param output:
        :return:
        """

        regex = re.compile(r'\(U\)')
        """
        The Above regex matches the string starts with port-channel and any number between 1 & 60 and stores the output 
        in a list.
        """
        result = regex.findall(output, re.MULTILINE)
        count = len(result)
        return count

    def verifySpinePortChannels(self):
        """
        In this class we are going to verify the number of port-channels on Spine-Switches and the status of the
        port-channel.
        :return:
        """

        cmd = "show port-channel summary"
        for ipaddress in GetSwitchDetails().get_spine_switch_ip():
            for value in GetSwitchDetails().get_spine_credentials():
                if value == ipaddress:
                    hostname = GetSwitchDetails().get_spine_swithnames()[ipaddress]
                    username = GetSwitchDetails().get_spine_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_spine_credentials()[ipaddress]['password']
                    connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)
                    self.logger.info(f'Executing command = {cmd} on switch = {hostname} with ipaddress = {ipaddress}')
                    ssh_stdin, ssh_stdout, ssh_stderr = connection.exec_command(cmd)
                    output = ssh_stdout.read().decode('utf-8')
                    connection.close()

                    configuredportchannels = SpinePoVerification().configuredPortChannels(output)
                    self.logger.info(f'Configured port-channels on spine = {hostname} are '
                                     f'count = {configuredportchannels}')

                    if configuredportchannels == GetSwitchDetails().total_leaf_switches():
                        self.logger.info(f'Configured port-channels on spine = {hostname} are equal '
                                         f'to total no.of leaf switches {GetSwitchDetails().total_leaf_switches()}')
                    else:
                        self.logger.info(f'Configured port-channels on spine = {hostname} are not equal '
                                         f'to total no.of leaf switches {GetSwitchDetails().total_leaf_switches()} ')

                    up_portchannels = SpinePoVerification().upPortChannels(output)
                    self.logger.info(f'number of UP port-channels on switch = {hostname} is {up_portchannels}')

                    if up_portchannels == GetSwitchDetails().total_leaf_switches():
                        self.logger.info(f'number of UP port-channels on switch = {hostname} are equal to total no.of '
                                         f'Leafs {GetSwitchDetails().total_leaf_switches()}')
                    else:
                        self.logger.info(f'number of UP port-channels on switch = {hostname} are not equal to total '
                                         f'no.of Leafs {GetSwitchDetails().total_leaf_switches()}')
                    self.logger.info(f'closing connection to switch = {hostname}')



x = SpinePoVerification()
x.verifySpinePortChannels()