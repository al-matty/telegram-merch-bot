# -*- coding: UTF8 -*-
# This file contains all the actual processing of the image

import time
from PIL import Image, ImageDraw, ImageFont
from scrapeData import getMetrics


def updatePic():
    '''
    Calls scrapeData.getMetrics() and prints token data on template image.
    Returns tuple (image, unix time stamp).
    '''
    dictOfDicts = getMetrics()
    template = 'YLDtest.png'

    def drawData(img, dictOfDicts):
        '''
        Assumes an image and a dict of dicts of a position tuple and token metrics.
        Cycles through keys and draws values under 'marketCap' and 'circSupply'
        keys on image, depending on the 'pos' tuple (position).
        Returns updated image.
        '''

        def getMcStr(dict_):
            '''return market cap string'''
            if dict_['marketCap'] < 1000000000:
                return str(round(dict_['marketCap'] / 1000000, 1)) + 'm'
            else:
                return str(round(dict_['marketCap'] / 1000000000, 1)) + 'b'

        def getSupplStr(dict_):
            '''return circulating supply string'''
            if dict_['circSupply'] < 1000000:
                return str(round(dict_['circSupply'] / 1000)) + 'k'
            else:
                return str(round(dict_['circSupply'] / 1000000)) + 'm'

        def drawTokenData(img, position, dict_):
            '''assume image, position and token metrics dict and print on image'''

            d1 = ImageDraw.Draw(img)
            myFont = ImageFont.truetype('Arial.ttf', 18)

            posMc = position
            posSup = (position[0] + 148, position[1])
            strMc = getMcStr(dict_)
            strSup = getSupplStr(dict_)

            d1.text(posMc, strMc, font=myFont, fill =(237, 187, 130))
            d1.text(posSup, strSup, font=myFont, fill =(237, 187, 130))

            return img

        for key in dictOfDicts.keys():

            pos = dictOfDicts[key]['pos']
            updatedPic = drawTokenData(img, pos, dictOfDicts[key])

        return updatedPic

    img = Image.open(template)
    updatedPic = drawData(img, dictOfDicts)

    # get current time (unix format)
    timeStamp = int(time.time())

    return updatedPic, timeStamp
