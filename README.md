# DesClock
## DesClock is a customizable clock application designed for a Raspberry Pi using the Official Raspberry Pi Touchscreen.

### About
DesClock is intended to be a helpful display with useful relavent information about various things. The goal 
is to have customization functionality by allowing the user to select what is visible by taking advantage of 
the flexability of GUI elements that PySimpleGUi provides. The user will be able to select what features are 
shown on the screen and in what order. 

### Built With
* Python
    * PySimpleGUI
* Raspberry Pi 4
* Official Raspberry Pi 7" [Touchscreen](https://www.raspberrypi.org/products/raspberry-pi-touch-display/)


### Progress Images
#### Version 0.1:
* Basic functionality.
* No modularity. 
* Can switch between military/non military time

![Progress Image](/images/version_0.1/v0.1-Military.png)
![Progress Image](/images/version_0.1/v0.1-standard.png)


#### Version 0.2:
* Implemented modularity with "FeatureBlocks"
* Added a layout manager with a basic interface.
* Can select a layout with multiple feature blocks
* Selected layouts will actually load the selected features.

![Progress Image](/images/version_0.2/layout_manager.jpg)
![Progress Image](/images/version_0.2/DeskClock_layouts.gif)
