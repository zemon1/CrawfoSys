#!/usr/bin/python
#Jeff Haak
#Scraper for stock data
import ystockquote as ystock
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Used for retrieving stock info from Yahoo')
    parser.add_argument('symbol', help='Stock symbol to retrieve data for')

    args = vars(parser.parse_args())

    #print args
    sym = args['symbol']

    if len(sym) == 6:
        sym += "=x"
    sData = ystock.get_all(sym)

    print "$" + sData['price'] + " " + sData['change'] + "%"






