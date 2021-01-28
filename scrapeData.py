#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Web Scraping Module for MerchBot
"""
import urllib.request
from bs4 import BeautifulSoup
import time
import random


def scrape(dict_, dictKey):
    """
    Returns a dictionary of token metrics for the token specified
    """

    commonUrl = 'https://www.coingecko.com/en/coins/'
    userAgent = (
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        )


    url = commonUrl + dictKey
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

    # add position tuple for drawing onto the image
    metrics['pos'] = dict_[dictKey]

    return metrics


def getMetrics():

    # Dict to determine which tokens to scrape information for, as well
    # as for the positioning in the image
    tokens = {
        'aave': (15,168),
        'compound': (311,168),
        'celsius-network-token': (607,168),
        'yield': (900,168),
        }

    dictOfDicts = {}


    for key in tokens.keys():

        # get data for token
        dictOfDicts[key] = scrape(tokens, key)

        # wait a tiny bit to hopefully not get banned on Coingecko
        time.sleep(random.randrange(20,30,1)/100)


    return dictOfDicts
