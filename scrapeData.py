#!/usr/bin/env python
# -*- coding: utf-8 -*-

# scraping from coingecko.com. Called every ~1 minute to update token metrics
# does nothing except regularly updating metrics.csv file

import urllib.request
from bs4 import BeautifulSoup
import time


url = 'https://www.coingecko.com/en/coins/yield'
userAgent = (
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    )

#TODO make this function abstract to iterate over four tokens
#   ->  for token in tokens:
#           dict = getMetrics(token)
#           add token metrics + position to dict of dicts

def getMetrics():
    """
    Returns a tuple:
    (dict of dicts of token metrics scraped from coingecko.com,
     current unix time)
    """

    req = urllib.request.Request(url, headers= {'User-Agent' : userAgent})
    html = urllib.request.urlopen(req)

    # parse data
    bs = BeautifulSoup(html.read(), 'html.parser')
    varList = bs.findAll('span', {'class': 'no-wrap'})

    # get data
    keys = ['priceUSD', 'marketCap', '24hVol', '24hLow', '24hHigh']
    metrics = {}
    for i, key in enumerate(keys):
        metrics[key] = varList[i].get_text()

    # clean data
    for key, val in metrics.items():
        metrics[key] = float(val.replace(',','').replace('$',''))

    # get and clean circulating supply of token
    varList = bs.findAll('div', {'class': 'mt-1'})
    circSupply = varList[6]
    circSupply = float(circSupply.get_text().split('/')[0].strip().replace(',',''))
    metrics['circSupply'] = circSupply




#TODO return an actual dict of dicts for the four tokens needed

    # temporary way to produce a dict of dicts for testing:

    dictOfDicts = {
        'AAVE': {
        'pos': (15,168),
        'priceUSD': 447.09,
        'marketCap': 19093615940.0,
        '24hVol': 2682487.0,
        '24hLow': 47.15,
        '24hHigh': 60.27,
        'circSupply': 13008758.0
        },

        'COMP': {
        'pos': (311,168),
        'priceUSD': 999.09,
        'marketCap': 1300615940.0,
        '24hVol': 2682487.0,
        '24hLow': 47.15,
        '24hHigh': 60.27,
        'circSupply': 5000758.0
        },

        'CEL': {
        'pos': (607,168),
        'priceUSD': 47.09,
        'marketCap': 19940.0,
        '24hVol': 2682487.0,
        '24hLow': 47.15,
        '24hHigh': 60.27,
        'circSupply': 2388758.0
        },

        'YLD': {
        'pos': (900,168),
        'priceUSD': 47.09,
        'marketCap': 13615940.0,
        '24hVol': 2682487.0,
        '24hLow': 47.15,
        '24hHigh': 60.27,
        'circSupply': 288758.0
        }
        }



    return dictOfDicts
