#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bot framework taken from Andrés Ignacio Torres <andresitorresm@gmail.com>,
all other files by Al Matty <almatty@gmail.com>.
"""
import time
import random
#import logging
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from PIL import Image
from imageManipulation import updatePic


class MerchBot:

    TELEGRAM_GROUP = 'group'

    """
    A class to encapsulate all relevant methods of the bot.
    """

    def __init__(self):
        """
        Constructor of the class. Initializes certain instance variables
        and checks if everything's O.K. for the bot to work as expected.
        """

        # This environment variable should be set before using the bot
        self.token = '1515330813:AAFymu9nZtJ9vhPovYfmolQ-SyCjna-5D_c'

        # Create some delay sequence to not overdo the web scraping
        self.randDelay = [random.randrange(45,75) for i in range(10)]

        # Fetches data right at the start
        self.currentMerch, self.lastFetched = updatePic()

        # These will be checked against as substrings within each
        # message, so different variations are not required if their
        # radix is present (e.g. "pup" covers "puppy" and "pupper" too)
        self.merch_trigger = ['/merch']


        # Same as earlier triggers, but for sad messages
        self.alt_trigger = ['alt']


        # Stops runtime if the token has not been set
        if self.token is None:
            raise RuntimeError(
                "FATAL: No token was found. " + \
                "You might need to specify one or more environment variables.")

        # Configures logging in debug level to check for errors
#        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                            level=logging.DEBUG)



    def run_bot(self):
        """
        Sets up the required bot handlers and starts the polling
        thread in order to successfully reply to messages.
        """

        # Instantiates the bot updater
        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        # Declares and adds handlers for commands that shows help info
        start_handler = CommandHandler('start', self.show_help)
        help_handler = CommandHandler('help', self.show_help)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(help_handler)

        # Declares and adds a handler to send a picture on demand
        merch_handler = CommandHandler('merch', self.sendPic)
        self.dispatcher.add_handler(merch_handler)

        # Declares and adds a handler for text messages that will reply with
        # a pic if the message includes a trigger word
        text_handler = MessageHandler(Filters.text, self.handle_text_messages)
        self.dispatcher.add_handler(text_handler)

        # Fires up the polling thread. We're live!
        self.updater.start_polling()


    def show_help(self, update, context):
        """
        Sends the user a brief message explaining how to use the bot.
        """
        pass
        #HELP_MSG = "If you're down for some merch bro, use the" + \
        #            "/merch command bro.."
        #context.bot.send_message(chat_id=update.message.chat_id, text=HELP_MSG)


    def handle_text_messages(self, update, context):
        """
        Checks if a message comes from a group. If that is not the case,
        or if the message includes a trigger word, replies with a dog picture.
        """
        words = set(update.message.text.lower().split())
#        logging.debug(f'Received message: {update.message.text}')
#        logging.debug(f'Splitted words: {", ".join(words)}')


        # Possibility: received command '/merch'
        shouldTriggerPicture = False
        for Trigger in self.merch_trigger:
            for word in words:
                if word.startswith(Trigger):
                    shouldTriggerPicture = True
                    break

        if shouldTriggerPicture:
            self.sendPic(update, context)


    def getMerch(self):
        """
        Sends either the stored merch or updates it if necessary.
        Returns the image data to be sent.
        """

        currentTime = int(time.time())
        delay = random.choice(self.randDelay)

        if currentTime - delay  < self.lastFetched:
            pass
        else:
            self.currentMerch, self.lastFetched = updatePic()

        return self.currentMerch

    # Send out whatever specified in images
    def sendPic(self, update, context, caption=None):
        """
        Sends the merch.
        """

        self.getMerch()
        time.sleep(1)

        images = ['currentMerch.png', 'YLD1.jpg', 'YLD2.jpg', 'YLD3.jpg']

        for image in images:
            with open(image, 'rb') as img:

                # Sends the picture
                context.bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=img,
                    caption=caption
                    )


def main():
    """
    Entry point of the script. If run directly, instantiates the
    MerchBot class and fires it up!
    """

    merch_bot = MerchBot()
    merch_bot.run_bot()


# If the script is run directly, fires the main procedure
if __name__ == "__main__":
    main()
