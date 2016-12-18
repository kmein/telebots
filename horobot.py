#!/usr/bin/env python3
from collections import namedtuple
from datetime import datetime
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import os
import re
import subprocess
import telepot
import tempfile

START = '✨'
DT_FORMAT = "%d.%m.%Y, %H:%M"

class Location(namedtuple("Location", ["direction", "degrees", "minutes", "seconds"])):
    def __str__(self):
        return "%d°%d\"%d'%s" % (self.degrees, self.minutes, self.seconds, self.direction)

def generate_latex(dt, longitude, latitude):

    def coords_show(location):
        return "%s%02d:%02d:%02d" % (location.direction, location.degrees, location.minutes, location.seconds)

    def coords_latex(location):
        return "%d\horodegrees %d\horominutes %s" % (location.degrees, location.minutes, location.direction)

    birthdate = "%d.%d.%d, %d:%02d" % (dt.day, dt.month, dt.year, dt.hour, dt.minute)
    birthplace = coords_latex(longitude) + " " + coords_latex(latitude)

    return r"""\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{mathpazo}
\usepackage[wasysym]{horoscop}
\pagestyle{empty}
\begin{document}
\def\horoobjects{Sun,Moon,Mercury,Venus,Mars,Jupiter,Saturn,Uranus,Neptune,Pluto,Ascendant,MC}
\horointhouselabelstrue
\horocalcparms{%04d}{%02d}{%02d}{%02d:%02d:00}{%s}{%s}
\horocalculate
\begin{horoscope}
    \horowheelVancouver
    \horoULnote{%s\\%s}
\end{horoscope}
\end{document}""" % (dt.year, dt.month, dt.day, dt.hour, dt.minute,
        coords_show(longitude), coords_show(latitude), birthdate, birthplace)

def replace_extension(path, ext):
    return os.path.splitext(path)[0] + ext

def compile(code):
    with tempfile.NamedTemporaryFile(mode="w+", dir=".", suffix=".tex") as temp:
        pdf_name = replace_extension(temp.name, ".pdf") # we wanna save the pdf file
        temp.write(code)
        temp.seek(0) # rewind because pdflatex is a bitch
        subprocess.call(["pdflatex", "--enable-write18", temp.name])
        for ext in (".log", ".aux", ".hor"):
            # remove files created by pdflatex command above
            try:
                os.remove(replace_extension(temp.name, ext))
            except FileNotFoundError:
                pass
    return pdf_name

def degrees_to_location(dd, direction):
    assert direction in ["E", "W", "S", "N"]
    is_positive = dd >= 0
    dd = abs(dd)
    minutes, seconds = divmod(dd*3600, 60)
    degrees, minutes = divmod(minutes, 60)
    # flip direction in case of negative degrees
    if not is_positive:
        if direction == "W":
            direction = "E"
        elif direction == "E":
            direction = "W"
        elif direction == "N":
            direction = "S"
        elif direction == "S":
            direction = "N"
    return Location(direction, round(degrees), round(minutes), round(seconds))

latitude = None
longitude = None
dob = None

def handle(msg):
    global latitude, longitude, dob
    content_type, _, chat_id = telepot.glance(msg)

    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=START)]])

    if content_type in ["location", "venue"]:
        if content_type == "location":
            location = msg["location"]
        elif content_type == "venue":
            location = msg["venue"]["location"]
        latitude = degrees_to_location(location["latitude"], "N")
        longitude = degrees_to_location(location["longitude"], "E")
    elif content_type == "text":
        if msg["text"] == START:
            tmp_pdf = compile(generate_latex(dob, longitude, latitude))
            pdf = dob.strftime("%Y-%m-%dT%H%MZ") + ".pdf"
            os.rename(tmp_pdf, pdf)
            bot.sendDocument(chat_id, (pdf, open(pdf, "rb")),
                    caption=dob.strftime(DT_FORMAT) + "\n" + str(latitude) + " " + str(longitude),
                    reply_markup=keyboard)
            os.remove(pdf)
        else:
            try:
                dob = datetime.strptime(msg["text"], DT_FORMAT)
            except ValueError:
                bot.sendMessage(chat_id, "Bitte Datum in Format \"%s\" angeben" % DT_FORMAT)
    print(latitude, longitude, dob)

if __name__ == "__main__":
    TOKEN = open("horobot.token").read().strip()
    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle, run_forever=True)
