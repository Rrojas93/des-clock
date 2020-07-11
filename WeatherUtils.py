#=========================================================================
#	WeatherUtils.py
#	Author: Raul Rojas
#	Contact: rrojas994@gmail.com
#	Description: 
#		Provides some weather data gathering utilities. 
#=========================================================================

import requests
from bs4 import BeautifulSoup as bSoup 
import _secrets
secrets = _secrets.MySecrets()

#------------------------------------------------------------
#	getOutdoorTemp()
#		Description: Retrieves current outdoor temperature of
#           current location. 
#------------------------------------------------------------
# TODO: Gather data based on an API interface or by IP location data. Currently gets temperature of only one static city.
def getOutdoorTemp():
    URL = secrets.weatherLink # hidden Weather link for location privacy reasons.. 
    page = requests.get(URL)
    # <span data-testid="TemperatureValue" class="_-_-components-src-organism-CurrentConditions-CurrentConditions--tempValue--MHmYY">79°</span>
    soup = bSoup(page.content, 'html.parser')
    temp = soup.find('span', class_='_-_-components-src-organism-CurrentConditions-CurrentConditions--tempValue--MHmYY')
    return temp.text

    
if __name__ == "__main__":
    print(getOutdoorTemp())