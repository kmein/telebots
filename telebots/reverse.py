#!/usr/bin/env python3
from telegram import File, Update, PhotoSize, Audio
from telegram.ext import MessageHandler, Updater, Filters, CallbackContext
from typing import Union, IO
import PIL.Image
import PIL.ImageOps
import click
import os
import pydub
import sys
import telebots.token
import tempfile

working_directory = tempfile.mkdtemp(prefix="reverse")


def reverse_image_inplace(img_file_path: str) -> None:
    img = PIL.Image.open(img_file_path)
    mirror_img = PIL.ImageOps.mirror(img)
    os.remove(img_file_path)
    mirror_img.save(img_file_path)


def reverse_audio_inplace(audio_file_path: str) -> None:
    audio = pydub.AudioSegment.from_file(audio_file_path)
    reverse_audio = audio.reverse()
    os.remove(audio_file_path)
    reverse_audio.export(audio_file_path)


def reverse_text(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text[::-1])


def reverse_photo(update: Update, context: CallbackContext) -> None:
    photo_file: File = update.message.photo[-1].get_file()
    photo_file_path: str = os.path.join(
        working_directory, os.path.basename(photo_file.file_path)
    )
    photo_file.download(custom_path=photo_file_path)
    reverse_image_inplace(photo_file_path)
    update.message.reply_photo(
        open(photo_file_path, "rb"),
        caption=update.message.caption[::-1] if update.message.caption else None,
    )
    os.remove(photo_file_path)


def reverse_voice(update: Update, context: CallbackContext) -> None:
    voice_file: File = update.message.voice.get_file()
    voice_file_path: str = os.path.join(
        working_directory, os.path.basename(voice_file.file_path)
    )
    voice_file.download(custom_path=voice_file_path)
    reverse_audio_inplace(voice_file_path)
    update.message.reply_voice(open(voice_file_path, "rb"))
    os.remove(voice_file_path)


def reverse_audio(update: Update, context: CallbackContext) -> None:
    audio: Audio = update.message.audio
    audio_file: File = audio.get_file()
    audio_file_path: str = os.path.join(
        working_directory, os.path.basename(audio_file.file_path)
    )
    audio_file.download(custom_path=audio_file_path)
    reverse_audio_inplace(audio_file_path)
    if audio.thumb:
        thumb_file = audio.thumb.get_file()
        thumb_file_path = os.path.join(
            working_directory, os.path.basename(thumb_file.file_path)
        )
        thumb_file.download(custom_path=thumb_file_path)
        reverse_image_inplace(thumb_file_path)
        thumb: Union[IO, None] = open(thumb_file_path, "rb")
    else:
        thumb = None
    update.message.reply_audio(
        open(audio_file_path, "rb"),
        title=audio.title[::-1] if audio.title else None,
        performer=audio.performer[::-1] if audio.performer else None,
        thumb=thumb,
    )
    os.remove(audio_file_path)
    os.remove(thumb_file_path)


@click.command()
def run():
    bot = Updater(token=telebots.token.get_token())
    bot.dispatcher.add_handler(MessageHandler(Filters.text, reverse_text))
    bot.dispatcher.add_handler(MessageHandler(Filters.audio, reverse_audio))
    bot.dispatcher.add_handler(MessageHandler(Filters.voice, reverse_voice))
    bot.dispatcher.add_handler(MessageHandler(Filters.photo, reverse_photo))

    bot.start_polling()
    bot.idle()
