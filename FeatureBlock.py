#=========================================================================
#	Layouts.py  
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: This module provides the building blocks for DeskClock 
#       features and instructions on how to implement them.
#=========================================================================

import PySimpleGUI as sg
import abc
import time


'''
----------------------------------------------------------------------------------------------------------
    class FeatureBlock(metaclass=abc.ABCMeta)
    Description: 
        An abstract class that provides a blueprint on how to create a new feature block 
        for DeskClock. 
    Attributes:
        globalKeySet: This is a set that contains unique keys that are being used by various
            other feature blocks.
----------------------------------------------------------------------------------------------------------
'''
class FeatureBlock(metaclass=abc.ABCMeta):
    globalKeySet = set()

    def __init__(self, posRow, posCol):
        ''' 
        If you need to override to set your own features attributes, be sure to call "super().__init__()" as
        these attributes may be necessary.
        '''
        self.safeKeys = self.__generateSafeKeys(self.myFeaturesKeys())
        self.posRow = posRow
        self.posCol = posCol
    
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'getFeatureColumn') and callable(subclass.getFeatureColumn) and 
            hasattr(subclass, 'update') and callable(subclass.update) and 
            hasattr(subclass, 'events') and callable(subclass.events) or 
            NotImplemented) 

    def __generateSafeKeys(self, featuresKeys):
        '''Generates Safe keys'''
        safeKeys = dict()
        for k in featuresKeys:
            v = str(featuresKeys[k])
            count = 0
            while(v in FeatureBlock.globalKeySet):
                count += 1
                v = v.split('<#>:')
                v = '{}<#>:{}'.format(v[0], count)
            safeKeys[k] = v
            FeatureBlock.globalKeySet.add(v)
        return safeKeys

    @abc.abstractmethod
    def getFeatureDescription(self) -> str:
        '''
        A short description to be displayed in the layout manager describing your feature.
        '''
        raise NotImplementedError
    '''
    ----------------------------------------------------------------------------------------------------------
        To create safe keys that your feature can use, create a dictionary in which the dictonaries key and value
        strings are the key you want to use for your gui element. Then, when refering to elements by key, use the
        "self.safeKeys" attribute (example: window[self.safeKeys["-text.example.mainText-]].update("NewText")). 
        Refer to the example below:
            Example key format: -sg_elem.your_feature_className.id-
            Examples:
                for a button element:   -button.MyFeatureClass.button1-
                for a text element:     -text.MyFeatureClass.text1-
            The dictionary to return for the above examples:
                return {
                    "-button.MyFeatureClass.button1-": "-button.MyFeatureClass.button1-",
                    "-text.MyFeatureClass.text1-": "-text.MyFeatureClass.text1-"
                    }
    ----------------------------------------------------------------------------------------------------------                
    '''
    def myFeaturesKeys(self):
        raise NotImplementedError('You must provide a dictonary containing the keys you intend to use by overriding this method.')

    @abc.abstractmethod
    def getFeatureColumn(self) -> sg.Column:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self):
        '''
        Should perform any updates to Your elements that is not tied to events.
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def events(self, event: str, values: dict):
        '''
        Should handle any events for your layout.
        '''
        raise NotImplementedError

    def __eq__(self, other):
        if(self.posRow == other.posRow and self.posCol == other.posCol):
            return True
        else:
            return False

    def __lt__(self, other):
        if(self.posRow < other.posRow):
            if(self.posCol < other.posCol):
                return True
        return False
    
    def __le__(self, other):
        if(self.posRow <= other.posRow):
            if(self.posCol <= other.posCol):
                return True
        return False

    def __gt__(self, other):
        if(self.posRow > other.posRow):
            if(self.posCol > other.posCol):
                return True
        return False
    
    def __ge__(self, other):
        if(self.posRow >= other.posRow):
            if(self.posCol >= other.posCol):
                return True
        return False

    def __ne__(self, other):
        if(self.posRow != other.posRow):
            if(self.posCol != other.posCol):
                return True
        return False
        

'''
----------------------------------------------------------------------------------------------------------
    TestMyFeature(class, int, int)
        Description:
            This function will test your feature by putting it in a test window
            where it will create multiple instances of the same class you insert.
            This is to allow you to see how your feature will interact with other
            features so that you have an idea of whether it will "play nice". 
        Arguments:
            myFeatureClass  = This should be your class. 
            numOfRows       = how many rows you want to display on the main window.
            numOfInst       = number of instances you want the test to generate for each row.
----------------------------------------------------------------------------------------------------------            
'''
def TestMyFeature(myFeatureClass, numOfRows=1, numOfInst=1):
    print('Beginning Feature Block Test.')
    testResults = []
    inheritOk = issubclass(myFeatureClass, FeatureBlock)
    testResults.append(inheritOk)
    print('Class Inherits From FeatureBlock: {}'.format(inheritOk))

    layout = []
    featureList = []
    for r in range(numOfRows):
        cols = []
        for c in range(numOfInst):
            featureObjInst = myFeatureClass()
            cols.append(featureObjInst.getFeatureColumn())
            featureList.append(featureObjInst)
        layout.append(cols)
    # print(str(layout))
    window = sg.Window(title='Your Feature Test', layout=layout, size=(800, 480), finalize=True, resizable=True)
    timed = False # used to time how long a timout event takes to handle feature block.
    while True:
        event, values = window.read(50)
        if(event != sg.TIMEOUT_EVENT and event != sg.WINDOW_CLOSED):
            print('\nEvent: ' + event + '\nValues: {}'.format(values))
        if(event == sg.WINDOW_CLOSED):
            window.close()
            break
        else:
            if(not(timed) or event != sg.TIMEOUT_EVENT):
                start = time.time()
            for f in featureList:
                if(not(timed) or event != sg.TIMEOUT_EVENT):
                    singleStart = time.time()
                
                f.events(event, values, window)
                f.update(window)
                window.finalize()
                
                if(not(timed) or event != sg.TIMEOUT_EVENT):
                    singleTimeDelta = time.time() - singleStart
                    print("A single element took {:.5f}ms to handle.".format(singleTimeDelta*1000))
            if(not(timed) or event != sg.TIMEOUT_EVENT):
                timedelta = time.time() - start
                print("All elements to a total time of {:.5f}ms to handle".format(timedelta*1000))
                timed = True
    return all(testResults)
