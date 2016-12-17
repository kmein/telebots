# telebots
Various Telegram Bots

## betacode.py
This bot converts Ancient Greek beta code to precomposed Unicode Greek.

## horobot.py
This bot interacts with the user sending a location and a date/time. It will
calculate an astrological birth/natal chart horoscope thingy and send it as PDF.

## reverse.py
This bot simply listens for messages and replies to each one with just the reversed message text.
It also mirrors images and reverses music / voice notes.

## sendmessage.py
This bot reads all of stdin and sends that to any chat it is part of.

## wrapper.py
This bot uses a command (passed as command line argument) as a filter for every
text. E.g. `./wrapper.py rev` will reverse every message.

# Installation
Please run `pip3 install -r requirements.txt` and then contact the
[BotFather](https://telegram.me/botfather) and send `/newbot` to obtain a bot token.
This token then has to be saved as a text file whose path can be adjusted in the
bot's source. For `sendmessage.py` it's the file `sendmessage.token`.
