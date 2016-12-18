#!/usr/bin/env python3
from cltk.corpus.greek.beta_to_unicode import Replacer
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
import bcolors
import logging
import telepot

replacer = Replacer()

def on_inline_query(msg):
    try:
        query_id, _, query_string = telepot.glance(msg, flavor="inline_query")
        greek = replacer.beta_code(query_string.upper())

        logging.info("Message is query #{}, namely \"{}\"".format(query_id, query_string))

        articles = [InlineQueryResultArticle(
            id="betacode",
            title=greek,
            input_message_content=InputTextMessageContent(message_text=greek)
            )]

        bot.answerInlineQuery(query_id, articles)
        logging.info("Proposing {}".format(greek))
    except telepot.exception.TelegramError:
        pass

if __name__ == "__main__":
    logging.basicConfig(
        format="{}[%(levelname)s %(asctime)s]{} %(message)s".format(
            bcolors.BOLD,
            bcolors.ENDC
        ), level=logging.INFO
    )
    TOKEN = open("betacode.token").read().strip()

    bot = telepot.Bot(TOKEN)
    bot.message_loop({"inline_query": on_inline_query}, run_forever=True)

