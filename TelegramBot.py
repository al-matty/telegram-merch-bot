# -*- coding: UTF8 -*-
# bot framework by @magnito, rest by @al-matty

import time
import random
import requests
import datetime
import imageio
from imageManipulation import updatePic
from scrapeData import getMetrics


class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    # def send_image(self, chat_id, imageFile):
    #         command = 'curl -s -X POST https://api.telegram.org/bot' + str(token) + '/sendPhoto -F chat_id=' + str(chat_id) + " -F photo=@" + imageFile
    #         subprocess.call(command.split(' '))
    #         return



    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = '1515330813:AAFymu9nZtJ9vhPovYfmolQ-SyCjna-5D_c' #Token of your bot
al_bot = BotHandler(token) #Your bot's name
#picPath = './testPic.png'
picUrl = 'https://cdn.publish0x.com/prod/fs/cachedimages/4085357584-80ce03db23204e1f181d30d21c8e80750d0d67f88307f08c77f553fba78b2f4f.png'
picData = imageio.imread(picUrl)

def main():
    new_offset = 0
    print('Bot launched.')

    # update token and set delay for fetching metrics (~ once per minute)
    randDelay = [random.randrange(45,75) for i in range(10)]
    tokenData, lastFetched = getMetrics()

    while True:
        all_updates=al_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text='New member'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"


              # Some chat functions

                if first_chat_text == 'Hi':
                    al_bot.send_message(first_chat_id, 'Morning ' + first_chat_name + '.')
                    new_offset = first_update_id + 1

                elif first_chat_text == '/merch':
#                    upToDateMerch = updatePic(picPath)

                    # update token data
                    currentTime = int(time.time())
                    delay = random.choice(randDelay)

                    if currentTime - delay  < lastFetched:
                        lastMetrics = tokenData
                    else:
                        lastMetrics, lastFetched = getMetrics()

                    sendStr = ''
                    for key, val in lastMetrics.items():
                        sendStr += f'{key}: {val}\n'

#                    al_bot.send_image(first_chat_id, picData)
                    print(picData)
                    al_bot.send_message(first_chat_id, sendStr + first_chat_name)
                    new_offset = first_update_id + 1
                else:
                    new_offset = first_update_id + 1

                    al_bot.send_message(first_chat_id, 'How are you doing, '+first_chat_name+'?')







if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
