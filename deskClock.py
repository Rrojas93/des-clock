#!/usr/bin/python3
# -*- coding: utf-8 -*-

#=========================================================================
#	deskClock.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		This application is a full screen desk clock designed for a 
#       Raspberry Pi using the official Raspberry Pi touch screen. Other 
#       screens may be used but resolution and scaling of GUI elements 
#       may not translate as intentionally designed. 
#=========================================================================

import PySimpleGUI as sg 
sg.theme('DarkAmber')

# Raspberry Pi TS Res. = (800, 480)
_screenResolution = sg.Window.get_screen_size()
_mainFontType = 'Calibri'
_mainFontPair = (_mainFontType, 12)

window = None

def main():
    createMainWindow(getMainLayout())
    while (True):
        event, values = window.read()
        if(event == '-button.Exit-'):
            window.close()
            break
        else:
            handleMainWindowEvents(event, values)

def handleMainWindowEvents(event, values):
    pass

def createMainWindow(layout):
    global window 
    window = sg.Window(
        title='Desk Clock', 
        layout=layout, 
        font=_mainFontPair, 
        no_titlebar=True, 
        size=_screenResolution, 
        resizable=True, 
        auto_size_buttons=True, 
        auto_size_text=True, 
        keep_on_top=True, 
        margins=(0,0), 
        element_padding=(0,0), 
        element_justification='center'
        )

def getMainLayout():
    layout = [
        [sg.Text('Desk Clock App', font=(_mainFontType, 16), )],
        [sg.Exit(key='-button.Exit-')]
    ]
    return layout

if __name__ == "__main__":
    main()