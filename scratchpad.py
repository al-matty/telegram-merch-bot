# -*- coding: UTF8 -*-
# loose collection of code snippets for possible later use


# code snippet as example for some basic NLP functionality

@bot.message_handler(func=lambda m: True)
def chat(message):
    txt = message.text
    if any(x for txt.lower() for x in ['thank','cool','thx']):
        msg = 'Anytime.'
    elif any(x in txt.lower() for x in ['hi','hallo','yo','hey']):
        msg = 'Hi.'
    else:
        msg = 'Get merch with \n/merch'
    bot.send_message(message.chat.id, msg)



# way to send images via the bot?

def send_image(botToken, imageFile, chat_id):
        command = 'curl -s -X POST https://api.telegram.org/bot' + botToken + '/sendPhoto -F chat_id=' + chat_id + " -F photo=@" + imageFile
        subprocess.call(command.split(' '))
        return
