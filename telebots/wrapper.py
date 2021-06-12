#!/usr/bin/env python3
from telegram import Update
from telegram.ext import Updater, MessageHandler, CallbackContext, Filters
from typing import Callable
import click
import subprocess
import telebots.bcolors
import telebots.token


def run_command(argv: str, stdin: str) -> str:
    stdout, _ = subprocess.Popen(
        argv, stdout=subprocess.PIPE, stdin=subprocess.PIPE
    ).communicate(input=stdin.encode())
    return stdout.decode()


def reply_with(command: str) -> Callable:
    def reply(update: Update, context: CallbackContext) -> None:
        update.message.reply_text(run_command(command, update.message.text))

    return reply


@click.command()
@click.argument("command")
def run(command: str):
    """Run a telegram bot which runs a stdin-stdout filter on every message."""
    updater = Updater(telebots.token.get_token())

    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, reply_with(command))
    )

    updater.start_polling()
    updater.idle()
