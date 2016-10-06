# telebots
Various Telegram Bots

## reverse.py
This bot simply listens for messages and replies to each one with just the reversed message text.
It also mirrors images and reverses music / voice notes.

## sendmessage.py
This bot reads all of stdin and sends that to any chat it is part of.

# Installation
Please run `pip3 install -r requirements.txt` and then contact the
[BotFather](telegram.me/botfather) and send `/newbot` to obtain a bot token.
This token then has to be saved as a text file whose path can be adjusted in the
bot's source. For `sendmessage.py` it's the file `sendmessage.token`.
