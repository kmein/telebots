#!/usr/bin/env python3

import PIL.Image, PIL.ImageOps
import os
import pydub
import telepot

def reverse_image_inplace(img_file_path):
    img = PIL.Image.open(img_file_path)
    mirror_img = PIL.ImageOps.mirror(img)
    os.remove(img_file_path)
    mirror_img.save(img_file_path)

def reverse_audio_inplace(audio_file_path, mimetype):
    category, audiotype = mimetype.split("/")
    if category != "audio":
        raise ValueError("The mimetype " + mimetype + " does not belong to an audio file.")
    audio = pydub.AudioSegment.from_file(audio_file_path, audiotype)
    reverse_audio = audio.reverse()
    os.remove(audio_file_path)
    reverse_audio.export(audio_file_path, audiotype)

def handle(msg):
    content_type, _, chat_id, _, message_id = telepot.glance(msg, long=True)
    if content_type == "text":
        bot.sendMessage(chat_id, msg["text"][::-1], reply_to_message_id=message_id)
    elif content_type == "photo":
        photo = sorted(msg["photo"], key=lambda ph: ph["file_size"], reverse=True)[0]
        file_obj = bot.getFile(photo["file_id"])
        img_file_path = os.path.basename(file_obj["file_path"])
        bot.download_file(file_obj["file_id"], img_file_path)
        reverse_image_inplace(img_file_path)
        bot.sendPhoto(
            chat_id,
            (img_file_path, open(img_file_path, "rb")),
            caption=msg["caption"][::-1] if "caption" in msg else None,
            reply_to_message_id=message_id
        )
        os.remove(img_file_path)
    elif content_type == "voice" or content_type == "audio":
        audio = msg[content_type]
        file_obj = bot.getFile(audio["file_id"])
        audio_file_path = os.path.basename(file_obj["file_path"])
        bot.download_file(file_obj["file_id"], audio_file_path)
        reverse_audio_inplace(audio_file_path, audio["mime_type"] if "mime_type" in audio else "audio/ogg")
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
        os.remove(audio_file_path)

if __name__ == "__main__":
    TOKEN = open("meerschweinchen.token").read().strip()

    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle, run_forever="Listening ...")
