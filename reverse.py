#!/usr/bin/env python3

import sys
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space
class Reverser(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Reverser, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.sender.sendMessage(msg["text"][::-1], reply_to_message_id=msg["message_id"])

TOKEN = open("reverse.token").read().strip()

bot = telepot.DelegatorBot(TOKEN, [pave_event_space()(per_chat_id(), create_open, Reverser, timeout=10)])
bot.message_loop(run_forever='Listening ...')
