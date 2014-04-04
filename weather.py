#!/usr/bin/env python2
#weather.py
#Original author: Josh McSavaney (mcsaucy@csh.rit.edu)
#Current maintainer: Jeff Haak (zemon1@csh.rit.edu)
#A script used to scrape and parse weather information

import urllib, re, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gets weather info from weather.gov')
    
    parser.add_argument('--noTroll'
                        , help='Display temp in Kelvin'
                        , default=False
                        , required=False)
    
    args = vars(parser.parse_args())
    
    #print args
     
    # get the file from the site
    file = urllib.urlopen('http://www.weather.gov/data/current_obs/KROC.xml')

    # make the file into a string
    data = file.read()


    weather = "N/A"
    temp = "N/A"
    windchill = "N/A"

    # search the file for the weather and store the string
    try:
        re2 = re.search(r'<weather>(.*?)</weather>', data)
        weather = re2.group(1)
    except (AttributeError):
        pass

    # search the file for the temp and store the string
    try:
        re3 = re.search(r'<temperature_string>(.*?)</temperature_string>', data)
        temp = re3.group(1)
    except (AttributeError):
        pass

    # search the file for the windchill and store the string
    try:
        re4 = re.search(r'<windchill_string>(.*?)</windchill_string>', data)
        windchill = re4.group(1)
    except (AttributeError):
        pass
   
    #use Kelvin
    if not args['noTroll']:
        windchill = float(windchill.split()[2][1:]) + 273.15
        temp = float(temp.split()[2][1:]) + 273.15
        
        windchill = "Windchill:" + str(windchill) + "K"
        temp = "Temp:" + str(temp) + "K"
         
        res = temp + " " + windchill + " " + weather             
    
    else:
        windchill = int(windchill.split()[0].split(".")[0])
        temp = int(temp.split()[0].split(".")[0])
        
        windchill = "Windchill:" + str(windchill) + "F"
        temp = "Temp:" + str(temp) + "F"
         
        res = temp + " " + windchill + " " + weather             
    
    print res 









