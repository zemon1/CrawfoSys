#!/usr/bin/env python2
#sWeather.py
#Original author: Josh McSavaney (mcsaucy@csh.rit.edu)
#Current maintainer: Jeff Haak (zemon1@csh.rit.edu)
#Other developer: Matt Soucy (msoucy@csh.rit.edu)
#A script used to scrape and parse weather information

import re, sys
from urllib import urlopen
from argparse import ArgumentParser
from time import sleep
# PySerial library
import serial

def parse_args(args=None):
    args = args or sys.argv[1:]
    parser = ArgumentParser(description='Gets weather info from weather.gov')

    parser.add_argument('--kelvin', '--noTroll', '-k',
                        help='Display temp in Kelvin',
                        action='store_true'
                        )
    parser.add_argument('--delay', '-d',
                        help='Delay between sending cycles',
                        default=5.5,
                        type=float
                        )
    parser.add_argument("--update", "-u",
                        help='Time in minutes between data updates',
                        type=float,
                        default=5,
                        )
    parser.add_argument("port",
                        help="COM port to use")

    return parser.parse_args(args)

def get_data():
    # get the file from the site
    data = urlopen('http://www.weather.gov/data/current_obs/KROC.xml').read()

    def searchTag(tag):
        reg = re.search(r'<{0}>(.*?)</{0}>'.format(tag), data)
        return reg.group(1) if reg else "N/A"

    # search the file for the weather and store the string
    weather = searchTag('weather')

    # search the file for the temp and store the string
    temp = searchTag('temperature_string')

    # search the file for the windchill and store the string
    windchill = searchTag('windchill_string')

    def convert_temp(tmp):
        tmp = float(tmp.split()[0])
        if args.kelvin:
            tmp = (tmp-32)*(5.0/9.0) + 273.15
        return "{0:.2f}".format(tmp) + 'FK'[args.kelvin]

    windchill = "Windchill:{0}".format(convert_temp(windchill))
    temp = "Temp:{0}".format(convert_temp(temp))

    return "{0} {1} {2} - ".format(temp, windchill, weather)

if __name__ == "__main__":

    args = parse_args()

    # Create the serial port
    port = serial.Serial(port=args.port)
    ssend = port.write

    res = get_data()
    print res
    upclock = 0
    delay = args.update * 60.0 / args.delay
    while True:
        if upclock >= delay:
            res = get_data()
            print res
            upclock = 0
        upclock += 1
        ssend(res)
        sleep(args.delay)









