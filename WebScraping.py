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
currentIpData = None

#------------------------------------------------------------
#	getPublicIP()
#		Description: requests from "WhatIsMyIP.org" for public 
#       IP Address
#------------------------------------------------------------
def getPublicIP():
    global currentIpData
    if(currentIpData is None):
        currentIpData = getIpData()
    return currentIpData.ip

class IpData():
    def __init__(self, dataDictionary: dict):
        self.ip = dataDictionary['Your IP']
        self.city = dataDictionary['City']
        self.region = dataDictionary['Region']
        self.country = dataDictionary['Country']
        self.isp = dataDictionary['ISP']
        self.latitude = dataDictionary['Latitude']
        self.longitude = dataDictionary['Longitude']

    def __repr__(self):
        return str(self.__dict__)

#------------------------------------------------------------
#	getIpData()
#		Description: Creates an object containg ip data.
#------------------------------------------------------------
def getIpData():
    page = requests.get('https://www.whatismyip.org/my-ip-address')
    soup = BeautifulSoup(page.content, 'html.parser')
    tableData = [d.text for d in soup.find_all('td')]
    dataDict = {
        'Your IP': None,
        'City': None,
        'Region': None,
        'Country': None,
        'ISP': None,
        'Latitude': None,
        'Longitude': None
    }
    if(len(tableData) % 2 == 0):
        for i, d in enumerate(tableData):
            if(i % 2 == 0): # even number i, is key for data table
                dataDict[d] = tableData[i+1]
    return IpData(dataDict)

if __name__ == "__main__":
    print(getPublicIP())
    print(str(getIpData()))

