#!/usr/bin/env python3
import bcolors
import telepot
import logging
import subprocess
import sys
import telepot

def run_command(argv, stdin):
    stdout, _ = subprocess.Popen(argv,
        stdout=subprocess.PIPE, stdin=subprocess.PIPE
    ).communicate(input=stdin.encode())
    return stdout.decode()

def handle(msg):
    content_type, _, chat_id, _, message_id = telepot.glance(msg, long=True)
    logging.info("Received a {} in chat {} with ID {}".format(content_type, chat_id, message_id))
    if content_type == "text":
        text = msg["text"]
        reply = run_command(sys.argv[1:], text)
        logging.info("Message is a {}, namely \"{}\"".format(content_type, text))
        logging.info("Sending response \"{}\" in chat {} to ID {}".format(reply, chat_id, message_id))
        bot.sendMessage(chat_id, reply, reply_to_message_id=message_id)
    else:
        logging.info("Ignoring {}".format(content_type))
    logging.info("Done")

if __name__ == "__main__":
    logging.basicConfig(
        format="{}[%(levelname)s %(asctime)s]{} %(message)s".format(
            bcolors.BOLD,
            bcolors.ENDC
        ), level=logging.INFO
    )
    TOKEN = open("meerschweinchen.token").read().strip()

    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle, run_forever=True)
