#!/bin/bash

# YLD Loan Tracker needs a Python 3.9 environment!

# Remove old outfiles
find . -name '*stderr*' -delete
find . -name '*stdout*' -delete

# Specify outfiles
#export LANG=en_US.UTF-8
TIMESTAMP=`date +"%Y %b %m %T"`
STDOUT=${TIMESTAMP}__stdout.txt
STDERR=${TIMESTAMP}__stderr.txt


# Set temporary environment variable
export TELEGRAM_BOT_TOKEN=1515330813:AAEV0_vPIMsWiMCTwFg7EAr4h3wx2DOfPxk


# Run script with specified outfiles

# auf Mac Mini:
#/opt/anaconda3/envs/3.6/bin/python3.6 TelegramBot_orig.py
/opt/anaconda3/envs/3.6/bin/python3.6 TelegramBot.py
# auf MacBook:
#/Users/matze/anaconda3/envs/3.9/bin/python main.py > "$STDOUT" 2> "$STDERR"

