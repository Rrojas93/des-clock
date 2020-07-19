import sys, inspect
import PySimpleGUI as sg 
import VanillaFeatures

class LayoutManager():
    def __init__(self, thirdPartyFeatures=None):
        self.vanillaFeats = inspect.getmembers(VanillaFeatures, inspect.isclass)
        self.vanillaFeatsDict = {}
        for f in self.vanillaFeats:
            self.vanillaFeatsDict[f[0]] = f[1]
        self.availableFeatures = []
        self.nextAvailableIndex = 0
        self.activeFeatures = []
        self.boxDimensions = (300, 200)
        self.buttonSize = (35,2)
        self.numOfRows = 2
        self.numOfCol = 2
        self.maxNumberOfFeatures = self.numOfRows * self.numOfCol
        self.selectedFeature = None
        self.defaultButtonColor = sg.theme_button_color()
        self.buttonSelectedColor = (self.defaultButtonColor[0], 'gray')
        print(self.defaultButtonColor)
        for i, feat in enumerate(self.vanillaFeats):
            self.availableFeatures.append(sg.Button(feat[0], key=f'button.available.{i}', size=self.buttonSize))
        for i in range(self.maxNumberOfFeatures): # Maximum features.
            self.activeFeatures.append(sg.Button(' ', key=f'button.active.{i}', visible=True, size=self.buttonSize))

        self.window = sg.Window(
            title='Layout Manager', 
            layout=self._getLayout(),
            size=(800,480), 
            element_justification='center',
            finalize=True, 
            font=('Everson Mono', 10)
        )
        for f in self.activeFeatures:
            f.update(visible=False)
        self.window.finalize()

    def _getLayout(self):
        availableList = [[f] for f in self.availableFeatures]
        activeList = [[f] for f in self.activeFeatures]
        infoSize = (self.boxDimensions[0]*2+59,70)
        layout = [[sg.Column(justification='center', layout=[
            [sg.Text('Layout Manager', justification='center', size=(100,0))],
            [sg.Column(justification='center', layout=[[
                sg.Frame(title='Available Features', layout=[[
                    sg.Column(scrollable=True, vertical_scroll_only=True, size=self.boxDimensions, layout=availableList)
                ]]),
                sg.Column(layout=[
                    [sg.Button(' >> ', key='button.addFeature', pad=(0,(75,0)), disabled=True)],
                    [sg.Button(' << ', key='button.removeFeature', pad=(0, 30), disabled=True)]
                ]),
                sg.Frame(title='Active Features', layout=[[
                    sg.Column(size=self.boxDimensions, scrollable=True, vertical_scroll_only=True, layout=activeList)
                ]])
            ]])],
            [sg.Column(justification='center', element_justification='center', layout=[[
                sg.Text(' ', key='feedbackText', auto_size_text=True, size=(50, 1), text_color='dark red'),
                sg.Text(f'Rows: {self.numOfRows} | Columns: {self.numOfCol} | Max Elements: {self.maxNumberOfFeatures}', key='text.dimensions', size=(30, 1))
            ]])],
            [sg.Column(element_justification='center', justification='center', layout=[[sg.Frame('Feature Description', element_justification='center', layout=[[
                sg.Column(size=infoSize, element_justification='center', justification='center', layout=[
                    [
                        sg.Text('-- Select a feature to see its description --', key='text.featureDescription')
                    ]
                ])
            ]])]])],
            [sg.Column(justification='center', element_justification='center', layout=[[
                sg.Button('Save and Apply', key='button.saveExit'),
                sg.Button('Exit', key='button.exit')
            ]])],
            [sg.Column(element_justification='center', justification='center', layout=[

            ])]
        ])]]
        return layout

    def read(self, timeout=None):
        return self.window.read(timeout=timeout)
    
    def addElementToActive(self, element: sg.Button):
        if(len(self.activeFeatures) != self.nextAvailableIndex): # not at last index.
            self.activeFeatures[self.nextAvailableIndex].update(text=element.GetText(), visible=True)
            self.nextAvailableIndex += 1
        else:
            self.window['feedbackText'].update("Can't add, max number of elements reached.")

    def removeElementFromActive(self, element):
        location = int(element.Key.split('.')[-1])
        element.update(text=' ') # reset button text
        for i in enumerate(range(self.nextAvailableIndex), start=location): # enumerate a range because we need a start index which range does not provide.
            i = i[0]
            if(len(self.activeFeatures)-1 != i):
                if(self.activeFeatures[i+1].GetText() != ' '): # check the next index to see if it is empty.
                    self.activeFeatures[i].update(text=self.activeFeatures[i+1].GetText()) # move the next button contents to the current one
                else:
                    self.activeFeatures[i].update(text=' ', visible=False) # no contents to get from next button so empty this one (which has already been moved.)
                    break
            else:
                self.activeFeatures[i].update(text=' ', visible=False) # no contents to get from next button so empty this one (which has already been moved.)
                break
        self.nextAvailableIndex = self.nextAvailableIndex - 1 if self.nextAvailableIndex >= 0 else 0
        if(self.nextAvailableIndex != len(self.activeFeatures)):
                self.window['feedbackText'].update(' ')

    def getFeatureDescription(self, element):
        element = element

    def handleEvents(self, event, values):
        if(event == sg.WINDOW_CLOSED or event == 'button.exit'):
            self.window.close()
            return False # close program

        # button selected
        if(event[:17] == 'button.available.'):
            self.focusButton(self._getElementWithKey(self.availableFeatures, event))
            self.enableAddButton()
        if(event[:13] == 'button.active'):
            self.focusButton(self._getElementWithKey(self.activeFeatures, event))
            self.enableRemoveButton()

        # adding/Removing Feature
        if(event == 'button.addFeature'):
            if(self.selectedFeature):
                self.addElementToActive(self.selectedFeature)
            else:
                self.displayMessage('Select a feature from the Available Feature list to add.')
        if(event == 'button.removeFeature'):
            if(self.selectedFeature):
                self.removeElementFromActive(self.selectedFeature)
                self.removeButtonFocus()
            else:
                self.displayMessage('Select a feature from the Active Feature list to remove.')
                
        return True # complete and continue
    
    def focusButton(self, newButton):
        self.removeButtonFocus()
        newButton.update(button_color=self.buttonSelectedColor)
        self.selectedFeature = newButton

    def removeButtonFocus(self):
        if(self.selectedFeature):
            self.selectedFeature.update(button_color=self.defaultButtonColor)
            self.selectedFeature = None

    def enableAddButton(self, enable=True):
        self.window['button.addFeature'].update(disabled=not(enable))
        self.window['button.removeFeature'].update(disabled=enable)

    def enableRemoveButton(self, enable=True):
        self.window['button.removeFeature'].update(disabled=not(enable))
        self.window['button.addFeature'].update(disabled=enable)

    def displayMessage(self, message: str):
        self.window['feedbackText'].update(str(message))

    def _getIndexOfElementWithKey(self, featureList, key):
        for i, f in enumerate(featureList):
            if(f.Key == key):
                return i

    def _getElementWithKey(self, featureList, key):
        return featureList[self._getIndexOfElementWithKey(featureList, key)]

    def _getClassFromFeats(self, name: str):
        for pair in self.vanillaFeats:
            if(pair[0] == name):
                return pair[1]

    def getListOfActiveFeats(self):
        feats = []
        row = 0
        col = 0
        for i, button in enumerate(self.activeFeatures):
            feats.append(self.vanillaFeatsDict[button.GetText()](row, col, timeAdjust=i))
            if(i >= (self.numOfCol-1)+(row * self.numOfCol)):
                row += 1
                col = 0
            else:
                col += 1
        return feats


layouts = LayoutManager()
exitApp = False
while(not(exitApp)):
    event, values = layouts.read()
    if(event == 'button.saveExit'):
        features = layouts.getListOfActiveFeats()
        print('generated layout')
    else:
        exitApp = not(layouts.handleEvents(event, values))
