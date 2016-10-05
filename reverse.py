#!/usr/bin/env python3

import PIL.Image, PIL.ImageOps
import os
import telepot

def reverse_image_inplace(img_file_path):
    img = PIL.Image.open(img_file_path)
    mirror_img = PIL.ImageOps.mirror(img)
    os.remove(img_file_path)
    mirror_img.save(img_file_path)

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

if __name__ == "__main__":
    TOKEN = open("meerschweinchen.token").read().strip()

    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle, run_forever="Listening ...")
