#!/usr/bin/env python2
#weather.py
#Original author: Josh McSavaney (mcsaucy@csh.rit.edu)
#Current maintainer: Jeff Haak (zemon1@csh.rit.edu)
#Serial developer: Matt Soucy (msoucy@csh.rit.edu)
#A script used to scrape and parse weather information

import urllib, re, argparse
# PySerial library
import serial

SER_READY = '101'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gets weather info from weather.gov')
    
    parser.add_argument('--noTroll',
                        help='Display temp in Kelvin',
                        default=False)
    parser.add_argument("port",
                        help="COM port to use")
    
    args = parser.parse_args()

    # Create the serial port
    port = serial.Serial(port=args.port)
    def ssend(data):
        port.write(SER_READY)
        for c in data:
            port.write(c)
    
    # get the file from the site
    data = urllib.urlopen('http://www.weather.gov/data/current_obs/KROC.xml').read()

    # search the file for the weather and store the string
    reg = re.search(r'<weather>(.*?)</weather>', data)
    weather = reg.group(1) if reg else "N/A"

    # search the file for the temp and store the string
    reg = re.search(r'<temperature_string>(.*?)</temperature_string>', data)
    temp = reg.group(1) if reg else "N/A"

    # search the file for the windchill and store the string
    reg = re.search(r'<windchill_string>(.*?)</windchill_string>', data)
    windchill = reg.group(1) if reg else "N/A"
   
    #use Kelvin
    if not args.noTroll:
        windchill = float(windchill.split()[2][1:]) + 273.15
        temp = float(temp.split()[2][1:]) + 273.15
        
        windchill = "Windchill:" + str(windchill) + "K"
        temp = "Temp:" + str(temp) + "K"
         
    else:
        windchill = int(windchill.split()[0].split(".")[0])
        temp = int(temp.split()[0].split(".")[0])
        
        windchill = "Windchill:" + str(windchill) + "F"
        temp = "Temp:" + str(temp) + "F"
    
    res = temp + " " + windchill + " " + weather             
    
    while True:
        ssend(res)









