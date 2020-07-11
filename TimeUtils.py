#!/usr/bin/python3
# -*- coding: utf-8 -*-

#=========================================================================
#	DeskClockUtilities.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		Provides utilities related to the clock or date/time.
#=========================================================================

import time

#------------------------------------------------------------
#	getTime()
#		Description: Returns a tuple (size of 2) representing the current
#           time. First element in tuple is the time, second element 
#           is "am" or "pm". Can adjust for different time
#           zones relative to your local.
#------------------------------------------------------------
def getTime(militaryTime=False, adjust=0):
    t = time.localtime(time.time())
    tHour = adjustHourRelLocal(adjustFromLocal=adjust, inputHour=t.tm_hour)
    ampm = 'PM' if tHour>= 12 else 'AM'
    hour = tHour - 12 if tHour > 12 and not(militaryTime) else tHour
    hour = 12 if hour == 0 and not(militaryTime) else hour
    return ('{0}:{1:0>2d}:{2:2}'.format(hour, t.tm_min, t.tm_sec), ampm)

#------------------------------------------------------------
#	getTimeZone()
#		Description: Returns the local time zone.
#------------------------------------------------------------
def getTimeZone():
    tz = time.localtime(time.time()).tm_zone
    splitTz = tz.split(' ')
    if(len(splitTz) > 1):
        tz = ''.join([w[0] for w in splitTz]) # return time zone acronym
    return tz

#------------------------------------------------------------
#	adjustHourRelLocal()
#		Description: Returns an adjusted time relative
#           to your local time. 
#------------------------------------------------------------
def adjustHourRelLocal(adjustFromLocal=0, inputHour=None):
    t = time.localtime(time.time())
    tHour = t.tm_hour if inputHour == None else inputHour
    hour = tHour + adjustFromLocal
    hour = hour + 24 if hour < 1 else hour
    hour = 0 if hour == 24 else hour
    return hour
    

if __name__ == "__main__":
    pass