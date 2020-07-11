#!/usr/bin/python3
# -*- coding: utf-8 -*-

#=========================================================================
#	WebScraping.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		This module provides multiple functions that scrape the web from 
#       various sources for information based on the user of this application. 
#=========================================================================

import requests
from bs4 import BeautifulSoup
import SysUtils
currentIpData = None

#------------------------------------------------------------
#	class IpData()
#		Description: Object that contains relavent ip information.
#------------------------------------------------------------
class IpData():
    def __init__(self, ip=None, city=None, region=None, country=None, countryCode=None, isp=None, latitude=None, longitude=None):
        self.ip = ip
        self.city = city
        self.region = region
        self.country = country
        self.countryCode = countryCode
        self.isp = isp
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return str(self.__dict__)

#------------------------------------------------------------
#	getPublicIP()
#		Description: requests from "WhatIsMyIP.org" for public 
#       IP Address
#------------------------------------------------------------
def getPublicIP():
    global currentIpData
    if(currentIpData is None):
        currentIpData = getPublicIpData()
    return currentIpData.ip

#------------------------------------------------------------
#	getPublicIpData()
#		Description: Creates and returns an object containg ip data.
#           Will return none if object cannot be created 
#           because of missing or unexpected data.
#------------------------------------------------------------
def getPublicIpData():
    page = requests.get('https://www.whatismyip.org/my-ip-address')
    soup = BeautifulSoup(page.content, 'html.parser')
    tableData = [d.text for d in soup.find_all('td')]
    dataDict = {    # setup a dictionary with default values in keys
        'ip': None,
        'city': None,
        'region': None,
        'country': None,
        'countryCode': None,
        'isp': None,
        'latitude': None,
        'longitude': None
    }
    if(len(tableData) % 2 == 0):
        values = [d for i, d in enumerate(tableData) if i % 2 != 0 ] # Onlly filter out the values for the table set.
        if(len(values) == len(dataDict.keys())): # ensure the number of values match the numebr of keys as they will be mapped 1 to 1
            keys = list(dataDict.keys()) # get the list of keys so that we can reference them on assigning.
            for i, v in enumerate(values): # for every filtered value.
                dataDict[keys[i]] = v # assign value to key.
        else:
            return None # cannot guarantee that data is correct so return None.
    else:
        return None # cannot guarantee that data is as expected, return None
            
    return IpData(**dataDict) # return an IpData instance, input unpacked dictionary.

#------------------------------------------------------------
#	getIPs()
#		Description: returns a dictionary containing the 
#           logical names (key) of available NIC's and their 
#           corresponding IP's (value) if available. 
#------------------------------------------------------------
def getIPs():
    out = SysUtils.runSys('ifconfig | grep -E "BROADCAST|netmask"')
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

#------------------------------------------------------------
#	checkConnections()
#		Description: adjusts the values of the dictionary 
#           returned from getIPs() to reflect any lost IP 
#           connections. Will take at most 1 second
#           if no connection.
#------------------------------------------------------------
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
            pingResult = SysUtils.runSys(f'ping -c 1 -W 2 -I {nic} {localIP}')
            if('0 received, 100% packet loss' in pingResult):
                iPs[nic] = 'No Connection'
            else:
                continue


if __name__ == "__main__":
    # print(getPublicIP())
    print(str(getPublicIpData()))

