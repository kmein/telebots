from telegram import File, Update, PhotoSize, Audio
from telegram.ext import MessageHandler, Updater, Filters, CallbackContext
import click
import os
import re
import requests
import sys
import telebots.token


def convert_link(link: str) -> str:
    if "spotify" in link:
        to_service = "youtube_music"
    elif "youtube" in link:
        to_service = "spotify"
        link = re.sub(r"//(www\.)?youtube.com", "//music.youtube.com", link)
    else:
        raise ValueError("Invalid streaming service: " + link)
    print(f"Trying to convert {link}", file=sys.stderr)
    r = requests.get(f'https://ytm2spotify.com/convert?url={link}&to_service={to_service}')
    print(r.text, file=sys.stderr)
    json = r.json()
    print(json, file=sys.stderr)
    return json["results"][0]["url"]



def streaming_link(update: Update, context: CallbackContext) -> None:
    try:
        converted = convert_link(update.message.text)
        update.message.reply_text(converted)
    except Exception as e:
        print(e, file=sys.stderr)
        update.message.reply_text("Cannot convert this.")


@click.command()
def run():
    bot = Updater(token=telebots.token.get_token())
    bot.dispatcher.add_handler(MessageHandler(Filters.text, streaming_link))

    bot.start_polling()
    bot.idle()
