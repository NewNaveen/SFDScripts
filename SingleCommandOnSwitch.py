import paramiko
import time
import concurrent.futures

from SFDScripts import switchDetails
from SFDScripts.switchDetails import GetSwitchDetails

spine_ip = GetSwitchDetails().get_spine_switch_ip()
leaf_ip = GetSwitchDetails().get_leaf_switch_ip()
required_ip = [leaf_ip[x] for x in range(8, 16)]


class RunSingleCommand:

    def run_commands(self):
        commands = ["show ip interface brief | except unassigned", "show ip bgp summary",
                    "show running-configuration bgp",
                    "show running-configuration vlt", "show vlt 127", "show port-channel summary", "show vlan",
                    "show vrrp brief", "show running-configuration uplink-state-group", "show spanning-tree active",
                    "show running-configuration | grep 1500"]

        for ipaddress in GetSwitchDetails().get_spine_switch_ip():
            for value in GetSwitchDetails().get_spine_credentials():
                if value == ipaddress:
                    try:
                        username = GetSwitchDetails().get_spine_credentials()[ipaddress]['username']
                        password = GetSwitchDetails().get_spine_credentials()[ipaddress]['password']
                        ssh = paramiko.SSHClient()
                        # ssh.load_host_keys()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        print("***** connecting to {} switch ******".format(ipaddress))
                        ssh.connect(ipaddress, 22, username, password)
                        for command in commands:
                            ssh_stdin, ssh_stdout, ssh_stder = ssh.exec_command(command)
                            output = ssh_stdout.read()
                            output = output.decode('utf8')
                            print(output)
                            print("***** closing ssh connection to {} switch ******\n".format(ipaddress))
                        ssh.close()

                    except paramiko.ssh_exception.AuthenticationException as err:
                        print(err)

                    except TimeoutError as err:
                        print("switch {0} unreachable {1}".format(ipaddress, err))

    def run_single_command_leafswitch(self, ipaddress):

        """
        try to  find an exception which handles if we the switch is unresponsive. basically we are able to login to switch
        and not able to go to CLI mode.
        """
        for value in GetSwitchDetails().get_leaf_credentials():
            if value == ipaddress:
                try:
                    username = GetSwitchDetails().get_leaf_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_leaf_credentials()[ipaddress]['password']
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    print("***** connecting to {} switch ******".format(ipaddress))
                    ssh.connect(ipaddress, 22, username, password)
                    ssh_stdin, ssh_stdout, ssh_stder = ssh.exec_command('show running-configuration telemetry')
                    output = ssh_stdout.read().decode('utf-8')
                    print(output)
                    print("***** closing ssh connection to {} switch ******\n".format(ipaddress))
                    ssh.close()

                except paramiko.ssh_exception.AuthenticationException as err:
                    print(err)

                except TimeoutError as err:
                    print("switch {0} unreachable {1}".format(ipaddress, err))

    def run_single_command_spineswitch(self, ipaddress):
        '''
        try to  find an exception which handles if we the switch is unresponsive. basically we are able to login to
        switch and not able to go to CLI mode.
        '''
        for value in GetSwitchDetails().get_spine_credentials():
            if value == ipaddress:
                try:
                    username = GetSwitchDetails().get_spine_credentials()[ipaddress]['username']
                    password = GetSwitchDetails().get_spine_credentials()[ipaddress]['password']
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    print("***** connecting to {} switch ******".format(ipaddress))
                    ssh.connect(ipaddress, 22, username, password)
                    ssh_stdin, ssh_stdout, ssh_stder = ssh.exec_command('show running-configuration telemetry')
                    output = ssh_stdout.read().decode('utf-8')
                    print(output)
                    print("***** closing ssh connection to {} switch ******\n".format(ipaddress))
                    ssh.close()

                except paramiko.ssh_exception.AuthenticationException as err:
                    print(err)

                except TimeoutError as err:
                    print("switch {0} unreachable {1}".format(ipaddress, err))


if __name__ == '__main__':
    x = RunSingleCommand()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as command:
        command.map(x.run_single_command_spineswitch, spine_ip)
        command.map(x.run_single_command_leafswitch, leaf_ip)
