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
import DeskClockSettings 
sg.theme('DarkAmber') # nicer color theme

_fixedResolution = (800, 480) # fixed resolution size for RPi Touch screen
_screenResolution = sg.Window.get_screen_size()
_screenResolution = _fixedResolution # Used to test and debug, comment out for variable screen sizes.
_mainFontType = 'Everson Mono'
_mainFontPair = (_mainFontType, 16)


window = None # main window of application.
settings = DeskClockSettings.loadSettings()

#------------------------------------------------------------
#	main()
#		Description: Main function for the program. Called
#           by "if __name__ == __main__" @ gottom of file.
#------------------------------------------------------------
def main():
    createMainWindow(getMainLayout())
    while (True):
        event, values = window.read(timeout=1000) # times out every 1 second to perform other functions.
        if(event == '-button.Exit-'):
            window.close()
            break
        else:
            mainWinEvents(event, values)
            updateGUI() # updates visuals on every timout AND every user provoked event for responsiveness.
    DeskClockSettings.saveSettings(settings) # save settings so that they persist on next load.

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
        margins=(5,3), 
        element_padding=(5,3), 
        element_justification='center', 
        finalize=True, 
        )

#------------------------------------------------------------
#	getMainLayout()
#		Description: returns the layout of the main 
#           GUI window.
#------------------------------------------------------------
def getMainLayout():
    timeFontSize = 64
    ampmFontSize = 20
    row_time = [[
        sg.Column(element_justification='center', pad=(0,50), layout=[[
            sg.Column(pad=((120,0), (0,0)), layout=[[
                sg.Text('00:00', key='-text.altTime-', font=(_mainFontType, timeFontSize), pad=((0,0), (0,0))),
                sg.Column(element_justification='left', key='-column.altTimeSpecs-', pad=(10,0), layout=[
                    [sg.Text('PDT', key='-text.altTimeZone-', font=(_mainFontType, int(ampmFontSize/2)), pad=((0,0),(15,15)))],
                    [sg.Text('PM', key='-text.altAmpm-', font=(_mainFontType, ampmFontSize), pad=((0,0), (0,0)), visible=not(settings.enableMilitaryTime))]
                    ])
                ]]),
            sg.Column(pad=((40,0), (0,0)), layout=[[
                sg.Text('00:00', key='-text.time-', font=(_mainFontType, timeFontSize), pad=((0,0), (0,0))),
                sg.Column(element_justification='left', key='-column.timeSpecs-', pad=(10,0), layout=[
                    [sg.Text(utils.getTimeZone(), key='-text.timeZone-', font=(_mainFontType, int(ampmFontSize/2)), pad=((0,0),(15,15)))],
                    [sg.Text('PM', key='-text.ampm-', font=(_mainFontType, ampmFontSize), pad=((0,0), (0,0)), visible=not(settings.enableMilitaryTime))]
                    ])
                ]])
            ]])
        ]]

    row_control = [[sg.Button('Military', key='-button.military-'), sg.Exit(key='-button.Exit-')]]

    layout = []
    layout += row_time
    layout += row_control

    return layout

#------------------------------------------------------------
#	mainWinEvents()
#		Description: handles any GUI events
#           from the main window of the application.
#------------------------------------------------------------
def mainWinEvents(event, values):
    if(event == sg.TIMEOUT_EVENT):
        # perform timeout events here.
        updateTime()
        # return since we know there are no user provoked events. 
        return
    if(event == '-button.military-'):
        settings.enableMilitaryTime = not(settings.enableMilitaryTime)
        window['-text.ampm-'].update(visible=not(settings.enableMilitaryTime))
        window['-text.altAmpm-'].update(visible=not(settings.enableMilitaryTime))
        updateTime()

    # The following should be any user provoked events.


#------------------------------------------------------------
#	updateGUI()
#		Description: Performs any GUI visual updates to the
#           main window. 
#------------------------------------------------------------
def updateGUI():
    # do any visual updates here

    # finalize changes and apply on finish
    window.finalize()

#------------------------------------------------------------
#	updateTime()
#		Description: Updates the time displayed on the main
#           window. This function also blinks the colon
#           in between the hour and minute after every sec.
#------------------------------------------------------------
def updateTime():
    t, ap = utils.getTime(settings.enableMilitaryTime)
    tic = ':' if int(t.split(':')[-1]) % 2 == 0 else ' '
    window['-text.time-'].Update(tic.join(t.split(':')[:-1]))
    window['-text.ampm-'].Update(ap)

    t, ap = utils.getTime(settings.enableMilitaryTime, adjust=-3)
    tic = ':' if int(t.split(':')[-1]) % 2 == 0 else ' '
    window['-text.altTime-'].Update(tic.join(t.split(':')[:-1]))

if __name__ == "__main__":
    main()