#!/usr/bin/env python3
from collections import namedtuple
from datetime import datetime
import json
import os
import pytz
import re
import subprocess
import telepot
import tempfile
import time
import urllib.request

# START_COMMAND = '✨'
DOB_COMMAND = "/zeit"
INFO_COMMAND = "/info"
START_COMMAND = "/astro"
DT_FORMAT = "%Y-%m-%d %H:%M"
API_KEY = open("horobot.key").read().strip()

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

def location_to_degrees(dms):
    dd = float(dms.degrees) + float(dms.minutes)/60 + float(dms.seconds)/(60*60);
    if dms.direction == "W" or dms.direction == "S":
        dd *= -1
    return dd

def adjust_dst(dt, longitude, latitude):
    if dt is None:
        return None
    location = "{},{}".format(location_to_degrees(latitude), location_to_degrees(longitude))
    timestamp = time.mktime(dt.timetuple())
    request = "https://maps.googleapis.com/maps/api/timezone/json?location={}&timestamp={}&key={}".format(location, timestamp, API_KEY)
    tz_info = json.loads(urllib.request.urlopen(request).read().decode("utf-8"))
    time_zone = pytz.timezone(tz_info["timeZoneId"])
    local_dt = time_zone.localize(dt, is_dst=False) # Note: is_dst doesn't do anything, only in ambiguous scenarios
    return dt - local_dt.dst()

# dictionary: from chat_id to values, to keep multiple threads of conversation
latitude = dict()
longitude = dict()
dob = dict()

def handle(msg):
    global latitude, longitude, dob
    print(latitude, longitude, dob)
    content_type, _, chat_id = telepot.glance(msg)
    if content_type in ["location", "venue"]:
        if content_type == "location":
            location = msg["location"]
        elif content_type == "venue":
            location = msg["venue"]["location"]
        latitude[chat_id] = degrees_to_location(location["latitude"], "N")
        longitude[chat_id] = degrees_to_location(location["longitude"], "E")
    elif content_type == "text":
        date_of_birth = dob.setdefault(chat_id)
        lon = longitude.setdefault(chat_id)
        lat = latitude.setdefault(chat_id)
        adjusted_dob = adjust_dst(date_of_birth, lon, lat)
        caption = "Zeit: " + (adjusted_dob.strftime(DT_FORMAT) if date_of_birth is not None else "None") + "\nOrt: " + str(lat) + " " + str(lon)
        if msg["text"].startswith(START_COMMAND):
            tmp_pdf = compile(generate_latex(adjusted_dob, lon, lat))
            pdf = adjusted_dob.strftime("%Y-%m-%dT%H%MZ") + ".pdf"
            os.rename(tmp_pdf, pdf)
            bot.sendDocument(chat_id, (pdf, open(pdf, "rb")), caption=caption)
            os.remove(pdf)
        elif msg["text"].startswith(INFO_COMMAND):
            bot.sendMessage(chat_id, caption)
        elif msg["text"].startswith(DOB_COMMAND):
            try:
                dob[chat_id] = datetime.strptime(msg["text"], DOB_COMMAND + " " + DT_FORMAT)
            except ValueError:
                bot.sendMessage(chat_id, "Bitte Datum in Format \"%s\" angeben" % DT_FORMAT)
    print(latitude.setdefault(chat_id), longitude.setdefault(chat_id), dob.setdefault(chat_id))

if __name__ == "__main__":
    TOKEN = open("horobot.token").read().strip()
    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle, run_forever=True)
