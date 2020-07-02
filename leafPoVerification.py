
import re
import logging
from SFDScripts.switchDetails import GetSwitchDetails
from SFDScripts.switchUtils import SwitchBasicFunctions


class LeafPoVerification:

    logger = logging.getLogger("naveen")
    logging.basicConfig(level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s')

    def configuredSpinePortChannels(self, output):
        """
        By using regular expression we are going to count the number of port-channels on each switch and returning
        the output
        :param output:
        :return:
        """

        regex = re.compile(r'port-channel[1-10]')
        """
        The Above regex matches the string starts with port-channel and any number between 1 & 60 and stores the output 
        in a list.
        """
        result = regex.findall(output, re.MULTILINE)
        count = len(result)
        return count

    def spineUpPortChannels(self, output):
        """
        By using regular expression we are going to count the number of UP port-channels on each switch and returning
        the output
        :param output:
        :return:
        """

        pc = ['port-channel1', 'port-channel2', 'port-channel3', 'port-channel4']
        # Matching the port-channels with the strings in the list. It is matching port-channel1000 also.
        result = [x for x in output.splitlines() for y in pc if y in x]
        # Getting only UP port-channels from result
        regex = re.compile(r'\(U\)')
        up_port_channels = [z for z in result if re.findall(regex, z)]
        # Subtracting 1 from the result, to eliminate po1000 from the count
        return len(up_port_channels) - 1



    def verifyLeafPortChannels(self):
        """
        In this class we are going to verify the number of port-channels on Spine-Switches and the status of the
        port-channel.
        :return:
        """

        cmd = "show port-channel summary"
        for ipaddress in GetSwitchDetails().get_leaf_switch_ip():
            for value in GetSwitchDetails().get_leaf_credentials():
                if value == ipaddress:
                    hostname = GetSwitchDetails().get_leaf_swithnames()[ipaddress]
                    username = GetSwitchDetails().get_leaf_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_leaf_credentials()[ipaddress]['password']
                    connection = SwitchBasicFunctions().sshToSwitches(ipaddress, username, password)
                    self.logger.info(f'Executing command = {cmd} on switch = {hostname} with ipaddress = {ipaddress}')
                    ssh_stdin, ssh_stdout, ssh_stderr = connection.exec_command(cmd)
                    output = ssh_stdout.read().decode('utf-8')
                    connection.close()

                    Spine_portchannels = LeafPoVerification().configuredSpinePortChannels(output)
                    self.logger.info(f'Configured Interlink port-channels on leaf = {hostname} are '
                                     f'count = {Spine_portchannels}')

                    if Spine_portchannels == GetSwitchDetails().spine_switch_count():
                        self.logger.info(f'Configured Interlink port-channels on leaf = {hostname} are equal '
                                         f'to total no.of leaf switches {GetSwitchDetails().spine_switch_count()}')
                    else:
                        self.logger.info(f'Configured Interlink port-channels on leaf = {hostname} are not equal '
                                         f'to total no.of spine switches {GetSwitchDetails().spine_switch_count()} ')

                    spine_up_portchannels = LeafPoVerification().spineUpPortChannels(output)
                    self.logger.info(f'number of UP Interlink port-channels on switch = {hostname} is {spine_up_portchannels}')

                    if spine_up_portchannels == GetSwitchDetails().spine_switch_count():
                        self.logger.info(f'UP Interlink port-channels on switch = {hostname} '
                                         f'are equal to total no.of Spines {GetSwitchDetails().spine_switch_count()}')
                    else:
                        self.logger.info(f'number of UP Interlink  port-channels on switch = {hostname} '
                                         f'are not equal to total no.of Spines {GetSwitchDetails().spine_switch_count()}')
                    self.logger.info(f'closing connection to switch = {hostname}')


x = LeafPoVerification()
x.verifyLeafPortChannels()
