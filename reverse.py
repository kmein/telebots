#!/usr/bin/env python3

import sys
import telepot

def handle(msg):
    content_type, _, chat_id, _, message_id = telepot.glance(msg, long=True)
    if content_type == "text":
        bot.sendMessage(chat_id, msg["text"][::-1], reply_to_message_id=message_id)

TOKEN = open("reverse.token").read().strip()

bot = telepot.Bot(TOKEN)
bot.message_loop(handle, run_forever="Listening ...")
