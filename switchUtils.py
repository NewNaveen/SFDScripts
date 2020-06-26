import paramiko
import time
import logging



class SwitchBasicFunctions:

    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s')
    logging.getLogger("paramiko").setLevel(logging.INFO)

    def sshToSwitches(self, ipaddress, username, password, port=22):
        """
        This function tries to ssh into the switches. Instead of writing SSH in all the functions we
        can use this function to SSH and do the configuration and get the output from the devices.

        :param ipaddress:
        :param username:
        :param password:
        :return:
        """

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.logger.info(f"***** connecting to switch = {ipaddress} *****")
            ssh.connect(ipaddress, port, username, password)
            return ssh
        except paramiko.ssh_exception.AuthenticationException as err:
            self.logger.info(f'Authentication is unsuccessful for switch = {ipaddress} with error = {err}')

        except paramiko.ssh_exception.NoValidConnectionsError as err:
            self.logger.info(f'No valid connection for switch = {ipaddress} with error = {err}')

        except TimeoutError as err:
            self.logger.info(f"switch {ipaddress} is unreachable {err}")

        except Exception as err:
            self.logger.info(f"Following error occurred on switch {ipaddress}: {err}")



"""
If we want to get only the output and don't want unnecessary information use the below paramiko commands

    def runSingleCmd(self):
        self.ipaddress = "10.174.18.16"
        self.username = "admin"
        self.password = "admin"

        connection = TestBGPCount().sshToSwitches(self.ipaddress, self.username, self.password)
        ssh_stdin, ssh_stdout, ssh_stderr = connection.exec_command("show version\n")
        self.logger.info("running show version command")
        output = ssh_stdout.read().decode("utf-8")
        self.logger.info(output)
"""