#!/usr/bin/python3
# -*- coding: utf-8 -*-

#=========================================================================
#	DeskClockGUI.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		This application is a full screen desk clock designed for a 
#       Raspberry Pi using the official Raspberry Pi touch screen. Other 
#       screens may be used but resolution and scaling of GUI elements 
#       may not translate as intentionally designed. 
#=========================================================================

import PySimpleGUI as sg 
import LayoutManager
import DeskClockWindows
#TODO: add a theme picker feature.

windows = dict()
activeWindow = None

#------------------------------------------------------------
#	main()
#		Description: Main function for the program. Called
#           by "if __name__ == __main__" @ gottom of file.
#------------------------------------------------------------
def main():
    global windows
    global activeWindow
    windows['bg'] = DeskClockWindows.BGWindow()
    windows['main'] = DeskClockWindows.MainWindow()
    windows['layouts'] = None
    activeWindow = windows['main']

    while(activeWindow):
        event, values = activeWindow.attend()
        handleWindowEvents(event, values)
    
    closeAllWindows()

def handleWindowEvents(event, values):
    '''
    Handles any events that are not handled or cant be handled by the class because of scope restraint.
    '''
    global activeWindow
    global windows
    if(event == sg.WINDOW_CLOSED or event == '-button.main.exit-'):
        if(activeWindow == windows['layouts']):
            activeWindow.close()
            activeWindow = None 
            activeWindow = windows['main']
        else:
            activeWindow.close()
            activeWindow = None
    if(event == sg.TIMEOUT_EVENT):
        activeWindow.update()
        activeWindow.finalize()
    if(event == '-button.main.layout-'):
        activeWindow.close()
        activeWindow = None
        windows['layouts'] = LayoutManager.LayoutManager()
        activeWindow = windows['layouts']
    if(event == '-button.layouts.save-'):
        listOfFeatures = activeWindow.getListOfActiveFeats()
        activeWindow.close()
        activeWindow = None
        windows['main'] = DeskClockWindows.MainWindow(listOfFeatures=listOfFeatures)
        activeWindow = windows['main']

def closeAllWindows():
    '''
    Close any remaining windows that are stored in memory.
    '''
    global windows
    for w in windows.values():
        if(w):
            w.close()

if __name__ == "__main__":
    main()