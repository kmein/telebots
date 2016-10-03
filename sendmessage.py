#!/usr/bin/env python3
import telepot
import sys

if __name__ == "__main__":
    TOKEN = open("sendmessage.token").read().strip()
    bot = telepot.Bot(TOKEN)
    contents = sys.stdin.read()
    for update in bot.getUpdates(offset=-1, limit=1):
        chat_id = update["message"]["chat"]["id"]
        bot.sendMessage(chat_id=chat_id, text=contents)
