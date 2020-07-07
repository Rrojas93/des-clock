import json

class Settings():
    def __init__(self, enableMilitaryTime=True):
        self.enableMilitaryTime = enableMilitaryTime
    

#------------------------------------------------------------
#	loadSettings()
#		Description: Deserializes a saved settings object if
#           it exists.
#------------------------------------------------------------
def loadSettings():
    try:
        with open('Settings.json', 'r') as f:
            settings = Settings(**json.load(f))
    except IOError:
        print('Settings file not found, loading default settings.')
        settings = Settings()
    return settings

#------------------------------------------------------------
#	saveSettings(settings: Settings)
#		Description: Serializes a settings object.
#------------------------------------------------------------
def saveSettings(settings_obj: Settings):
    inputType = str(type(settings_obj))
    with open('Settings.json', 'w') as f:
        if(inputType == "<class 'DeskClockSettings.Settings'>" or inputType == "<class '__main__.Settings'>"):
            json.dump(settings_obj.__dict__, f, indent=4)
        else:
            raise TypeError("Expecting an object of type: <class 'DeskClockSettings.Settings'>")

s = loadSettings()
saveSettings(s)
print('complete')