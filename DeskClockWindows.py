#!/usr/bin/python3
# -*- coding: utf-8 -*-

#=========================================================================
#	DeskClockWindows.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		Contains custom window objects easier handling of windows.
#=========================================================================


import PySimpleGUI as sg 
import FeatureBlock
import VanillaFeatures
from typing import List

_fixedResolution = (800, 480) # fixed resolution size for RPi Touch screen
_screenResolution = sg.Window.get_screen_size()
_screenResolution = _fixedResolution # Used to test and debug, comment out for variable screen sizes.
_mainFontType = 'Everson Mono'
_mainFontPair = (_mainFontType, 16)
_defaultTheme = 'DarkAmber'

class DCWindow():
    '''
    Do not override __init__(), override start() for custom class vars using self.varName.
    '''
    def __init__(self, theme=_defaultTheme, timeout=None, **kwargs):
        self.window = None
        self.timeout = timeout
        sg.theme(theme)
        self.start(**kwargs)
        if(not(self.window)): # if window was not created in start function from override.
            raise ValueError('This class does not have a window. Create one in start() function.')
            # self.window = sg.Window(title=title, layout=self.windowLayout(), finalize=True, **kwargs)

    def windowLayout(self):
        '''Override with your windows layout'''
        return [[]]

    def start(self, **kwargs):
        '''
        Provides a function to be overriden for custom __init__ necessities w/o calling super().__init__().
        Does not need to be called. DCWindow.__init__() calls this function.
        '''
        pass

    def read(self, timeout=None, **kwargs):
        '''Wrapper function for the sg window.read() function.'''
        return self.window.read(timeout=timeout, **kwargs)

    def handleEvents(self, event, values):
        '''Handles this classes events. Should be inherited with your own custom class events'''
        pass

    def update(self, event, values, window):
        '''
        Provides a method for updating gui elements without the need for user interaction. 
        Will be called as a result from a timeout by the read function and will not be called 
        during a user generated event (Those visual updates should be made by the event handler)
        '''
        pass

    def finalize(self):
        self.window.finalize()

    def attend(self, timeout=None, **kwargs):
        to = timeout if timeout else self.timeout # give timeout from the call priority over the self attribute.
        event, values = self.read(timeout=to, **kwargs)
        self.handleEvents(event, values)
        return (event, values)
    
    def close(self):
        self.window.close()
        del(self)

class MainWindow(DCWindow):
    def start(self, listOfFeatures=None, timeout=100):
        if(not(listOfFeatures)):
            listOfFeatures = [
                VanillaFeatures.Clock(0, 1),
                VanillaFeatures.Clock(0, 0, timeAdjust=-3)
            ]
        self.features = listOfFeatures
        self.timeout = timeout
        layout = self.windowLayout(listOfFeatures)
        self.window = sg.Window(
            title='DeskClock',
            layout=layout,
            no_titlebar=True,
            font=_mainFontPair,
            size=_screenResolution,
            auto_size_buttons=True,
            auto_size_text=True,
            keep_on_top=False,
            margins=(5,3),
            element_padding=(5,3),
            element_justification='center',
            finalize=True
            )

    def windowLayout(self, listOfFeatures: List[FeatureBlock.FeatureBlock]):
        featureLayout = []
        listOfFeatures.sort()
        maxR, maxC = self.getLayoutDimensions(listOfFeatures)
        i = 0
        for r in range(maxR):
            row = []
            for c in range(maxC):
                if(i >= len(listOfFeatures)): # if reached end of feature list.
                    break
                row.append(listOfFeatures[i].getFeatureColumn())
                i += 1
            if(row): # if items were added to the list.
                featureLayout.append(row[:])
            if(i >= len(listOfFeatures)): # if reached end of feature list.
                break
        featureLayout += [[sg.Button('Layout', key='-button.main.layout-'), sg.Exit(key='-button.main.exit-')]]

        layout = [[
            sg.Column(
                layout=featureLayout,
                element_justification='center',
                justification='center'
            )
        ]]
        return layout

    def getLayoutDimensions(self, sortedList: List[FeatureBlock.FeatureBlock]):
        maxR = -1
        maxC = -1
        for f in sortedList:
            if(f.posRow > maxR):
                maxR = f.posRow
            if(f.posCol > maxC):
                maxC = f.posCol
        return (maxR+1, maxC+1)

    def update(self):
        for feature in self.features:
            feature.update(self.window)

    def handleEvents(self, event, values):
        for feature in self.features:
            feature.events(event, values, self.window)
        

class BGWindow(DCWindow):
    def start(self):
        self.window = sg.Window(
            title='DeskClock_Background',
            layout=self.windowLayout(),
            size=_screenResolution,
            finalize=True,
            )

    def windowLayout(self):
        pass


if __name__ == "__main__":
    pass
