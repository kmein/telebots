#!/usr/bin/env python3

import bcolors

import logging
import PIL.Image, PIL.ImageOps
import os
import pydub
import telepot

def reverse_image_inplace(img_file_path):
    img = PIL.Image.open(img_file_path)
    mirror_img = PIL.ImageOps.mirror(img)
    os.remove(img_file_path)
    mirror_img.save(img_file_path)

def reverse_audio_inplace(audio_file_path):
    audio = pydub.AudioSegment.from_file(audio_file_path)
    reverse_audio = audio.reverse()
    os.remove(audio_file_path)
    reverse_audio.export(audio_file_path)

def handle(msg):
    content_type, _, chat_id, _, message_id = telepot.glance(msg, long=True)
    logging.info("Received a {} in chat {} with ID {}".format(content_type, chat_id, message_id))
    if content_type == "text":
        text = msg["text"]
        reply = text[::-1]
        logging.info("Message is a {}, namely \"{}\"".format(content_type, text))
        logging.info("Sending response \"{}\" in chat {} to ID {}".format(reply, chat_id, message_id))
        bot.sendMessage(chat_id, reply, reply_to_message_id=message_id)
    elif content_type == "photo":
        photo = sorted(msg["photo"], key=lambda ph: ph["file_size"], reverse=True)[0]
        logging.info("Message is a {}, namely {}".format(content_type, photo))
        file_obj = bot.getFile(photo["file_id"])
        img_file_path = os.path.basename(file_obj["file_path"])
        logging.info("Downloading {} {}".format(content_type, img_file_path))
        bot.download_file(file_obj["file_id"], img_file_path)
        logging.info("Reversing {} {}".format(content_type, img_file_path))
        reverse_image_inplace(img_file_path)
        logging.info("Sending reversed {} in chat {} to ID {}".format(img_file_path, chat_id, message_id))
        bot.sendPhoto(
            chat_id,
            (img_file_path, open(img_file_path, "rb")),
            caption=msg["caption"][::-1] if "caption" in msg else None,
            reply_to_message_id=message_id
        )
        logging.info("Deleting {}".format(img_file_path))
        os.remove(img_file_path)
        logging.info("Done")
    elif content_type == "voice" or content_type == "audio":
        audio = msg[content_type]
        logging.info("Message is a {}, namely {}".format(content_type, audio))
        file_obj = bot.getFile(audio["file_id"])
        audio_file_path = os.path.basename(file_obj["file_path"])
        logging.info("Downloading {} {}".format(content_type, audio_file_path))
        bot.download_file(file_obj["file_id"], audio_file_path)
        logging.info("Reversing {} {}".format(content_type, audio_file_path))
        reverse_audio_inplace(audio_file_path)
        logging.info("Sending reversed {} in chat {} to ID {}".format(audio_file_path, chat_id, message_id))
        if content_type == "voice":
            bot.sendVoice(
                chat_id,
                (audio_file_path, open(audio_file_path, "rb")),
                reply_to_message_id=message_id
            )
        elif content_type == "audio":
            bot.sendAudio(
                chat_id,
                (audio_file_path, open(audio_file_path, "rb")),
                reply_to_message_id=message_id,
                performer=audio["performer"][::-1] if "performer" in audio else None,
                title=audio["title"][::-1] if "title" in audio else None
            )
        logging.info("Deleting {}".format(audio_file_path))
        os.remove(audio_file_path)
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
    bot.message_loop(handle, run_forever="Listening ...")
