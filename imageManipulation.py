#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Image Manipulation Module for MerchBot
"""
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from scrapeData import getMetrics


def updatePic():
    '''
    Calls scrapeData.getMetrics() and prints token data on template image.
    Returns tuple (image, unix time stamp).
    '''
    dictOfDicts = getMetrics()
    template = 'YLDTemplate.png'

    def getMcStr(dict_, int_=False):
        '''return market cap string'''
        if dict_['marketCap'] < 1000000000:
            if int_:
                return str(round(dict_['marketCap'] / 1000000)) + 'm'
            else:
                return str(round(dict_['marketCap'] / 1000000, 1)) + 'm'
        else:
            if int_:
                return str(round(dict_['marketCap'] / 1000000000)) + 'b'
            else:
                return str(round(dict_['marketCap'] / 1000000000, 1)) + 'b'

    def getSupplStr(dict_, int_=False):
        '''Returns circulating supply string'''
        if dict_['circSupply'] < 1000000:
            if int_:
                return str(round(dict_['circSupply'] / 1000)) + 'k'
            else:
                return str(round(dict_['circSupply'] / 1000, 1)) + 'k'
        else:
            if int_:
                return str(round(dict_['circSupply'] / 1000000)) + 'm'
            else:
                return str(round(dict_['circSupply'] / 1000000, 1)) + 'm'

    def drawData(img, dictOfDicts):
        '''
        Assumes an image and a dict of dicts of a position tuple and token metrics.
        Cycles through keys and draws values under 'marketCap' and 'circSupply'
        keys on image, depending on the 'pos' tuple (position).
        Returns updated image.
        '''

        def drawTokenData(img, position, dict_):
            '''
            Assumes image, position and token metrics dict.
            Prints data on image and returns it.
            '''
            # Draw token metrics
            d1 = ImageDraw.Draw(img)
            myFont = ImageFont.truetype('GothamBook.ttf', 18)

            posMc = position
            posSup = (position[0] + 148, position[1])
            strMc = getMcStr(dict_)
            strSup = getSupplStr(dict_)

            d1.text(posMc, strMc, font=myFont, fill =(237, 187, 130))
            d1.text(posSup, strSup, font=myFont, fill =(237, 187, 130))

            # Draw current time
            timeStamp = int(time.time())    # Get current time in unix format
            parsedTs = datetime.utcfromtimestamp(timeStamp).strftime('%d %b %Y')
            drawTime = 'Figures as at ' + str(parsedTs)

            dateFont = ImageFont.truetype('GothamBook.ttf', 14)
            d1.text((1018, 462), drawTime, font=dateFont, fill =(237, 187, 130))

            return img

        # Update, return and save 'currentmerch.png'
        for key in dictOfDicts.keys():
            # Some position adjustment to factor in the changed font
            pos = (dictOfDicts[key]['pos'][0], dictOfDicts[key]['pos'][1] + 2)
            # Draw token metrics on image
            updatedPic = drawTokenData(img, pos, dictOfDicts[key])
        updatedPic.save('currentMerch.png')
        return updatedPic


    def drawExtras():
        '''
        Draws extra stuff as specified in customizable extrasDict.
        Saves to finlenames as in extrasDict.keys().
        Does not return anything.
        '''
        extrasDict = {
            'YLD1.jpg':{'mcPos': (351,66), 'supPos': (528,66), 'fontSize': 20, 'color': (237, 187, 130)},
            'YLD2.jpg':{'mcPos': (452,667), 'supPos': (646,667), 'fontSize': 22, 'color': (237, 187, 130)},
            'YLD3.jpg':{'mcPos': (70,468), 'supPos': (450,468), 'fontSize': 44, 'color': (254, 254, 254)}
            }

        marketCap = '$' + getMcStr(dictOfDicts['yield'], int_=True)
        circSupply = getSupplStr(dictOfDicts['yield'], int_=True)

        for pic in extrasDict.keys():
            img = Image.open('Template' + pic)
            d1 = ImageDraw.Draw(img)
            myFont = ImageFont.truetype('GothamBook.ttf', extrasDict[pic]['fontSize'])

            if extrasDict[pic]['mcPos']:
                d1.text(extrasDict[pic]['mcPos'], \
                    marketCap, font=myFont, fill=extrasDict[pic]['color'])
            if extrasDict[pic]['supPos']:
                d1.text(extrasDict[pic]['supPos'], \
                    circSupply, font=myFont, fill=extrasDict[pic]['color'])
            img.save(pic)

    # Get current time in unix format
    timeStamp = int(time.time())
    img = Image.open(template)
    updatedPic = drawData(img, dictOfDicts)

    # Draw and save extra images specified within drawExtras() function
    drawExtras()

    return updatedPic, timeStamp
