#!/usr/bin/env python3
from collections import namedtuple
from datetime import datetime
from telegram import Update, User
from typing import Dict
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)
import click
import os
import pytz
import requests
import subprocess
import telebots.token
import tempfile

DT_FORMAT = "%Y-%m-%d %H:%M"


class Location(namedtuple("Location", ["direction", "degrees", "minutes", "seconds"])):
    def __str__(self):
        return "%d°%d\"%d'%s" % (
            self.degrees,
            self.minutes,
            self.seconds,
            self.direction,
        )


def generate_latex(dt: datetime, longitude, latitude):
    def coords_show(location: Location):
        return "%s%02d:%02d:%02d" % (
            location.direction,
            location.degrees,
            location.minutes,
            location.seconds,
        )

    def coords_latex(location: Location):
        return fr"{location.degrees}\horodegrees {location.minutes}\horominutes {location.direction}"

    birthdate = f"{dt.day}.{dt.month}.{dt.year}, {dt.hour}:{dt.minute:02}"
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
\end{document}""" % (
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        coords_show(longitude),
        coords_show(latitude),
        birthdate,
        birthplace,
    )


def replace_extension(path, ext):
    return os.path.splitext(path)[0] + ext


def compile(code: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w+", dir=".", suffix=".tex") as temp:
        pdf_name = replace_extension(temp.name, ".pdf")  # we wanna save the pdf file
        temp.write(code)
        temp.seek(0)  # rewind because pdflatex is a bitch
        subprocess.call(["pdflatex", "--enable-write18", temp.name])
        for ext in (".log", ".aux", ".hor"):
            # remove files created by pdflatex command above
            try:
                os.remove(replace_extension(temp.name, ext))
            except FileNotFoundError:
                pass
    return pdf_name


def degrees_to_location(dd: float, direction) -> Location:
    assert direction in ["E", "W", "S", "N"]
    is_positive = dd >= 0
    dd = abs(dd)
    minutes, seconds = divmod(dd * 3600, 60)
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


def location_to_degrees(dms: Location) -> float:
    dd = float(dms.degrees) + float(dms.minutes) / 60 + float(dms.seconds) / (60 * 60)
    if dms.direction == "W" or dms.direction == "S":
        dd *= -1
    return dd


def adjust_dst(dt: datetime, longitude: Location, latitude: Location) -> datetime:
    if dt is None:
        return None
    tz_info = requests.get(
        "https://maps.googleapis.com/maps/api/timezone/json",
        params={
            "location": f"{location_to_degrees(latitude)},{location_to_degrees(longitude)}",
            "timestamp": str(dt.timestamp()),
            "key": telebots.token.get_maps_api_key(),
        },
    ).json()
    time_zone = pytz.timezone(tz_info["timeZoneId"])
    # Note: is_dst doesn't do anything, only in ambiguous scenarios
    local_dt = time_zone.localize(dt, is_dst=False)
    return dt - local_dt.dst()


###############################################################################

DATE_OF_BIRTH, LOCATION, REPORT = range(3)


# dictionary: from chat_id to values, to keep multiple threads of conversation
latitudes: Dict[User, Location] = dict()
longitudes: Dict[User, Location] = dict()
dates_of_birth: Dict[User, datetime] = dict()


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Wann (Datum und Uhrzeit) wurdest du geboren?")
    return DATE_OF_BIRTH


def date_of_birth(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    dates_of_birth[user] = datetime.strptime(update.message.text, DT_FORMAT)
    update.message.reply_text("Wo wurdest du geboren?")
    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_location = update.message.location
    latitudes[user] = degrees_to_location(user_location.latitude, "N")
    longitudes[user] = degrees_to_location(user_location.longitude, "E")

    date_of_birth = dates_of_birth.setdefault(user)
    longitude = longitudes.setdefault(user)
    latitude = latitudes.setdefault(user)
    adjusted_date_of_birth = adjust_dst(date_of_birth, longitude, latitude)

    tmp_pdf = compile(generate_latex(adjusted_date_of_birth, longitude, latitude))
    pdf = adjusted_date_of_birth.strftime("%Y-%m-%dT%H%MZ") + ".pdf"
    os.rename(tmp_pdf, pdf)
    caption = f"Zeit: {adjusted_date_of_birth.strftime(DT_FORMAT)}\nOrt: {latitude} {longitude}"
    update.message.reply_document((pdf, open(pdf, "rb")), caption=caption)
    os.remove(pdf)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    # user = update.message.from_user
    update.message.reply_text("Bye!")
    return ConversationHandler.END


@click.command()
def run():
    updater = Updater(token=telebots.token.get_token())
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                DATE_OF_BIRTH: [
                    MessageHandler(Filters.text, date_of_birth),
                ],
                LOCATION: [
                    MessageHandler(Filters.location, location),
                ],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
    )
    updater.start_polling()
    updater.idle()


# def handle(msg):
#    global latitude, longitude, dob
#    print(latitude, longitude, dob)
#    content_type, _, chat_id = telepot.glance(msg)
#    if content_type in ["location", "venue"]:
#        if content_type == "location":
#            location = msg["location"]
#        elif content_type == "venue":
#            location = msg["venue"]["location"]
#        latitude[chat_id] = degrees_to_location(location["latitude"], "N")
#        longitude[chat_id] = degrees_to_location(location["longitude"], "E")
#    elif content_type == "text":
#        date_of_birth = dob.setdefault(chat_id)
#        lon = longitude.setdefault(chat_id)
#        lat = latitude.setdefault(chat_id)
#        adjusted_dob = adjust_dst(date_of_birth, lon, lat)
#        caption = (
#            "Zeit: "
#            + (
#                adjusted_dob.strftime(DT_FORMAT)
#                if date_of_birth is not None
#                else "None"
#            )
#            + "\nOrt: "
#            + str(lat)
#            + " "
#            + str(lon)
#        )
#        if msg["text"].startswith(START_COMMAND):
#            tmp_pdf = compile(generate_latex(adjusted_dob, lon, lat))
#            pdf = adjusted_dob.strftime("%Y-%m-%dT%H%MZ") + ".pdf"
#            os.rename(tmp_pdf, pdf)
#            bot.sendDocument(chat_id, (pdf, open(pdf, "rb")), caption=caption)
#            os.remove(pdf)
#        elif msg["text"].startswith(INFO_COMMAND):
#            bot.sendMessage(chat_id, caption)
#        elif msg["text"].startswith(DOB_COMMAND):
#            try:
#                dob[chat_id] = datetime.strptime(
#                    msg["text"], DOB_COMMAND + " " + DT_FORMAT
#                )
#            except ValueError:
#                bot.sendMessage(
#                    chat_id, 'Bitte Datum in Format "%s" angeben' % DT_FORMAT
#                )
#    print(
#        latitude.setdefault(chat_id),
#        longitude.setdefault(chat_id),
#        dob.setdefault(chat_id),
#    )
