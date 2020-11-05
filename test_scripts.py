import paramiko
import datetime
import time
import concurrent.futures


ip_address = ["10.175.18.90", "10.175.18.92", "10.175.18.94",
              "10.175.18.96", "10.175.18.98", "10.175.18.100",
              "10.175.18.102", "10.175.18.104"]

def switch_reload(ipaddress):
    '''
    try to  find an exception which handles if we the switch is unresponsive. basically we are able to login to switch
    and not able to go to CLI mode.
    '''
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("***** connecting to {} switch ******".format(ipaddress))
        ssh.connect(ipaddress, username="admin", password="admin")
        ssh_stdin, ssh_stdout, ssh_stder = ssh.exec_command('show vlan')
        output = ssh_stdout.read().decode('utf-8')
        print(output)
        print("***** closing ssh connection to {} switch ******\n".format(ipaddress))
        ssh.close()

    except paramiko.ssh_exception.AuthenticationException as err:
        print(err)

    except TimeoutError as err:
        print("switch {0} unreachable {1}".format(ipaddress, err))

if __name__ == '__main__':
    # This concurrent features will do the functions of thread start, join and initiating threading process
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as e:
        e.map(switch_reload, ip_address)