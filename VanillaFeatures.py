#!/usr/bin/python3
# -*- coding: utf-8 -*-
import FeatureBlock
import PySimpleGUI as sg 
import DeskClockSettings
import time
import TimeUtils

class Clock(FeatureBlock.FeatureBlock):
    def __init__(self, posRow, posCol, font=('Everson Mono', 16), militaryTime=False, blink=True, timeAdjust=0):
        self.clockFont = font
        self.militaryTime = militaryTime
        self.prevTime = int(time.time())
        self.blink = blink
        self.timeAdjust = timeAdjust
        super().__init__(posRow = posRow, posCol = posCol)

    def getFeatureDescription(self):
        return "Simple clock."

    def myFeaturesKeys(self):
        keys = {
            'time': 'time',
            'timeSpecs': 'timeSpecs', 
            'timeZone': 'timeZone', 
            'ampm': 'ampm'
        }
        return keys

    def getFeatureColumn(self):
        layout = [[
            sg.Text('00:00', key=self.safeKeys['time'], font=(self.clockFont[0], 64), pad=((0,0), (0,0))),
            sg.Column(element_justification='center', key=self.safeKeys['timeSpecs'], pad=(10,0), layout=[
                [sg.Text(TimeUtils.getTimeZone(), key=self.safeKeys['timeZone'], font=(self.clockFont[0], 10), pad=((0,0),(15,15)))],
                [sg.Text('PM', key=self.safeKeys['ampm'], font=(self.clockFont[0], 20), pad=((0,0), (0,0)), visible=not(self.militaryTime))] 
                ])
            ]]
        return sg.Column(layout=layout, element_justification='center', pad=(30,10))

    def update(self, window):
        if(int(time.time()) != self.prevTime):
            t, ampm = TimeUtils.getTime(militaryTime=self.militaryTime, adjust=self.timeAdjust)
            tSplit = t.split(':')
            if(self.blink):
                t = ':'.join(tSplit[:2]) if int(tSplit[-1]) % 2 == 0 else ' '.join(tSplit[:2])
            else:
                t = tSplit[:2]
            window[self.safeKeys['time']].update(str(':'.join(t.split(':')[:2])))
            window[self.safeKeys['ampm']].update(str(ampm))
            self.prevTime = int(time.time())

    def events(self, event, value, window):
        pass


class Clock2(FeatureBlock.FeatureBlock):
    def __init__(self, posRow, posCol, font=('Everson Mono', 16), militaryTime=False, blink=True, timeAdjust=0):
        self.clockFont = font
        self.militaryTime = militaryTime
        self.prevTime = int(time.time())
        self.blink = blink
        self.timeAdjust = timeAdjust
        super().__init__(posRow = posRow, posCol = posCol)

    def myFeaturesKeys(self):
        keys = {
            'time': 'time',
            'timeSpecs': 'timeSpecs', 
            'timeZone': 'timeZone', 
            'ampm': 'ampm'
        }
        return keys

    def getFeatureDescription(self):
        return "Simple clock 2."

    def getFeatureColumn(self):
        layout = [[
            sg.Text('00:00', key=self.safeKeys['time'], font=(self.clockFont[0], 64), pad=((0,0), (0,0))),
            sg.Column(element_justification='center', key=self.safeKeys['timeSpecs'], pad=(10,0), layout=[
                [sg.Text(TimeUtils.getTimeZone(), key=self.safeKeys['timeZone'], font=(self.clockFont[0], 10), pad=((0,0),(15,15)))],
                [sg.Text('PM', key=self.safeKeys['ampm'], font=(self.clockFont[0], 20), pad=((0,0), (0,0)), visible=not(self.militaryTime))] 
                ])
            ]]
        return sg.Column(layout=layout, element_justification='center', pad=(30,10))

    def update(self, window):
        if(int(time.time()) != self.prevTime):
            t, ampm = TimeUtils.getTime(militaryTime=self.militaryTime, adjust=self.timeAdjust)
            tSplit = t.split(':')
            if(self.blink):
                t = ':'.join(tSplit[:2]) if int(tSplit[-1]) % 2 == 0 else ' '.join(tSplit[:2])
            else:
                t = tSplit[:2]
            window[self.safeKeys['time']].update(str(':'.join(t.split(':')[:2])))
            window[self.safeKeys['ampm']].update(str(ampm))
            self.prevTime = int(time.time())

    def events(self, event, value, window):
        pass


# FeatureBlock.TestMyFeature(Clock, 4, 4)