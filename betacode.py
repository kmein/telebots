#!/usr/bin/env python3
from cltk.corpus.greek.beta_to_unicode import Replacer
import bcolors
import logging
import telepot

replacer = Replacer()

def handle(msg):
    content_type, _, chat_id = telepot.glance(msg)
    logging.info("Received a {} in chat {}".format(content_type, chat_id))
    if content_type == "text":
        text = msg["text"]
        reply = replacer.beta_code(text.upper())
        logging.info("Message is a {}, namely \"{}\"".format(content_type, text))
        logging.info("Sending response \"{}\" in chat {}".format(reply, chat_id))
        bot.sendMessage(chat_id, reply)
    logging.info("Done")

if __name__ == "__main__":
    logging.basicConfig(
        format="{}[%(levelname)s %(asctime)s]{} %(message)s".format(
            bcolors.BOLD,
            bcolors.ENDC
        ), level=logging.INFO
    )
    TOKEN = open("betacode.token").read().strip()

    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle, run_forever=True)
