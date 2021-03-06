#!/usr/bin/python3
# -*- coding: utf-8 -*-

#=========================================================================
#	DeskClockSettings.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		Module providing a settings object for deskClock.py and allow for 
#       user preference persistance.
#=========================================================================


import json

class Settings():
    def __init__(self, **Settings):
        self.settings = Settings
    

#------------------------------------------------------------
#	loadSettings()
#		Description: Deserializes a saved settings object if
#           it exists.
#------------------------------------------------------------
def loadSettings(fPath='Settings.json'):
    try:
        with open(fPath, 'r') as f:
            settings = Settings(**json.load(f))
    except IOError:
        print('Settings file not found, loading default settings.')
        settings = Settings()
    return settings

#------------------------------------------------------------
#	saveSettings(settings: Settings)
#		Description: Serializes a settings object.
#------------------------------------------------------------
def saveSettings(settings_obj: Settings, fPath='Settings.json'):
    inputType = str(type(settings_obj))
    with open(fPath, 'w') as f:
        if(inputType == "<class 'DeskClockSettings.Settings'>" or inputType == "<class '__main__.Settings'>"):
            json.dump(settings_obj.__dict__, f, indent=4)
        else:
            raise TypeError("Expecting an object of type: <class 'DeskClockSettings.Settings'>")

s = loadSettings()
saveSettings(s)
print('complete')