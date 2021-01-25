#!/usr/bin/env python
# -*- coding: utf-8 -*-

# scraping from coingecko.com. Called every ~1 minute to update token metrics
# does nothing except regularly updating metrics.csv file

import urllib.request
from bs4 import BeautifulSoup
import time
import random


url = 'https://www.coingecko.com/en/coins/yield'
userAgent = (
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    )


def getMetrics():
    """
    returns a tuple:
    (dict of token metrics scraped from coingecko.com, current unix time)
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

    # get current time (unix format)
    timeStamp = int(time.time())

    return metrics, timeStamp
