#!/usr/bin/python3
# -*- coding: utf-8 -*-

#=========================================================================
#	myUtils.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		Provides some custom helpful functions that can be used in various
#       other scripts.
#=========================================================================

import subprocess
import time

def runSys(inputCommand: str):
    out = subprocess.Popen(inputCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = out.communicate()
    if(stderr):
        errorMsg = f'An error occured when running system command: "{inputCommand}"\n' + stderr
        raise SystemError(errorMsg)
    return stdout.decode('utf-8').strip()

def getIPs():
    out = runSys('ifconfig | grep -E "BROADCAST|netmask"')
    outLines = out.splitlines()
    ips = {}
    for i, line in enumerate(outLines):
        if('BROADCAST' in line): # This line contains the logical name for NIC
            nicName = line.strip().split(':')[0]
            if('broadcast' in outLines[i+1]):
                address = outLines[i+1].strip().split(' ')[1]
            else:
                address = 'No Connection'
            ips[nicName] = address
    return ips

def checkConnections(iPs: dict):
    for nic in iPs.keys():
        if ('No Connection' in iPs[nic]):
            continue
        else:
            localIP = iPs[nic].split('.')[:-1]
            localIP.append('1')
            localIP = '.'.join(localIP)
            print(localIP)
            # pingResult = runSys(f'ping -c 1 -W 2 {localIP}')
            pingResult = runSys(f'ping -c 1 -W 2 -I {nic} {localIP}')
            if('0 received, 100% packet loss' in pingResult):
                iPs[nic] = 'No Connection'
            else:
                continue

#------------------------------------------------------------
#	getTime()
#		Description: Returns a tuple (size of 2) representing the current
#           time. First element in tuple is the time, second element 
#           is "am" or "pm"
#------------------------------------------------------------
def getTime(militaryTime=False):
    t = time.localtime(time.time())
    ampm = 'pm' if t.tm_hour >= 12 else 'am'
    hour = t.tm_hour - 12 if t.tm_hour > 12 and not(militaryTime) else t.tm_hour
    hour = 12 if hour == 0 and not(militaryTime) else hour
    return (f'{hour}:{t.tm_min}', ampm)


if __name__ == "__main__":
    pass