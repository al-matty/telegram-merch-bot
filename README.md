# TelegramMerchBot


A Telegram bot that produces merchandise for the cryptocurrency 'YLD' on demand.
You can add this bot on Telegram by searching for its handle `@YLDMerchBot`.
Send it `/merch` and it sends back this image with the always up-to-date token
metrics circulating supply and market capitalization:

![Preview](https://github.com/al-matty/TelegramMerchBot/blob/main/currentMerch.png)

It does so in three steps:

1. Scrape and store up-to-date token metrics from coingecko.com.
2. Draw scraped data onto the template image.
3. Send image to user on demand.
