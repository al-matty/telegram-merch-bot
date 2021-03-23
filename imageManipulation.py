#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Image Manipulation Module for MerchBot
"""
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from scrapeData import getMetrics, get_moon_metrics
from math import floor

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
            'YLD1.jpg':{'mcPos': (350,67), 'supPos': (528,67), 'fontSize': 18, 'color': (237, 187, 130)},
            'YLD2.jpg':{'mcPos': (452,669), 'supPos': (646,669), 'fontSize': 20, 'color': (237, 187, 130)},
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

    def draw_moon_pic():

        moon_metrics = get_moon_metrics()

        pic = 'YLD_Moon.jpg'
        img = Image.open('TemplateYLD4.JPG')

        d1 = ImageDraw.Draw(img)
        myFont = ImageFont.truetype('GothamBook.ttf', size=26)

        draw_order = ['yield', 'cream', 'anchor-protocol', 'alpha-finance', 'compound', 'aave']
        yield_mc = moon_metrics['yield']['marketCap']
        yield_price = moon_metrics['yield']['priceUSD']

        def parse_str(float_, roundTo=1):
            '''
            Parses float to str.
            Conditionally appends nothing, 'k', 'm' or 'b'
            '''
            def round_or_not(float_, roundTo=roundTo):
                if roundTo:
                    return round(float_, roundTo)
                else:
                    return float_

            if float_ >= 1000000000:
                return str(round_or_not(float_/1000000000)) + 'bn'
            if float_ >= 1000000:
                return str(round(float_/1000000)) + 'm'
            else:
                return str(round(float_))


        def draw_row(moon_metric, pos_y):
            color = (237, 187, 130)

            # Draw mc twice
            mc = '$' + parse_str(moon_metric['marketCap'])
            pos_x = 525 - (len(mc) / 2)
            d1.text((pos_x, pos_y), mc, font=myFont, fill=color)
            d1.text((pos_x + 280, pos_y), mc, font=myFont, fill=color)

            # Draw ROI
            roi = str(int(moon_metric['marketCap'] // yield_mc)) + 'x'
            pos_x = 150 - (len(roi)/ 2)
            d1.text((pos_x, pos_y), roi, font=myFont, fill=color)

            # Draw YLD extrapolated price
            multiplier = moon_metric['marketCap'] / yield_mc
            yld_price = '$' + parse_str(floor(multiplier * yield_price))
            pos_x = 335 - (len(yld_price)/ 2)
            d1.text((pos_x, pos_y), yld_price, font=myFont, fill=color)



        pos_y = 348

        for token_str in draw_order:
            metrics = moon_metrics[token_str]

            draw_row(metrics, pos_y)

            pos_y += 107


        img.save(pic)



    # Get current time in unix format
    timeStamp = int(time.time())
    img = Image.open(template)
    updatedPic = drawData(img, dictOfDicts)

    # Draw and save extra images specified within drawExtras() function
    drawExtras()

    # Draw and save moon_pic with YLD mc extrapolation
    draw_moon_pic()

    return updatedPic, timeStamp
