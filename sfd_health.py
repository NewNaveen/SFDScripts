#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 21:39:51 2020

@author: hsheng
"""

import time
import datetime
import paramiko

# below are the data we pre-defined, only modify data at one file

ipaddress = '10.173.225.212'
username = 'admin@sfd.local'
password = 'Admin!23'


def get_health(ipaddress):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipaddress, username=username, password=password)
    connection = ssh.invoke_shell()

    for i in range(100):
        connection.send('system health --full\n')
        time.sleep(5)

        output = connection.recv(65535).decode("utf-8")
        banner = datetime.datetime.now()
        fo = open("vlan_creation.txt", "a")
        fo.write("\n@@@@@@@@ Executing command for {} time". format(i))
        fo.write("\n###############The current time is %s\n\n\n" % str(banner))
        fo.write(output)
        fo.close()
    ssh.close()

def main_SFD_start():
    get_health(ipaddress)

if __name__ == '__main__':
    main_SFD_start()

