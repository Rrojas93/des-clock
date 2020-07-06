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
import DeskClockUtilities as utils
sg.theme('DarkAmber')


_fixedResolution = (800, 480) # fixed resolution size for RPi Touch screen
_screenResolution = sg.Window.get_screen_size()
_screenResolution = _fixedResolution # Used to test and debug, comment out for variable screen sizes.
_mainFontType = 'Calibri'
_mainFontPair = (_mainFontType, 12)

window = None

#------------------------------------------------------------
#	main()
#		Description: Main function for the program. Called
#           by "if __name__ == __main__" @ gottom of file.
#------------------------------------------------------------
def main():
    createMainWindow(getMainLayout())
    while (True):
        event, values = window.read()
        if(event == '-button.Exit-'):
            window.close()
            break
        else:
            mainWinEvents(event, values)
            updateGUI()

#------------------------------------------------------------
#	createMainWindow()
#		Description: Creates the main window of the application.
#------------------------------------------------------------
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

#------------------------------------------------------------
#	getMainLayout()
#		Description: returns the layout of the main 
#           GUI window.
#------------------------------------------------------------
def getMainLayout():
    layout = [
        [sg.Text('<time>', key='-text.time-', font=(_mainFontType, 16)), sg.Text('<ampm>', key='-text.ampm-', font=(_mainFontType, 16))],
        [sg.Exit(key='-button.Exit-')]
    ]
    return layout

#------------------------------------------------------------
#	mainWinEvents()
#		Description: handles any GUI events
#           from the main window of the application.
#------------------------------------------------------------
def mainWinEvents(event, values):
    pass

#------------------------------------------------------------
#	updateGUI()
#		Description: Performs any GUI visual updates to the
#           main window. 
#------------------------------------------------------------
def updateGUI():
    pass

if __name__ == "__main__":
    main()