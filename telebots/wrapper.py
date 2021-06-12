from telegram import Update
from telegram.ext import (
    CallbackContext,
    Filters,
    InlineQueryHandler,
    InlineQueryResultArticle,
    InputTextMessageContent,
    MessageHandler,
    Updater,
)
from typing import Callable
from uuid import uuid4
import click
import subprocess
import telebots.token


def run_command(argv: str, stdin: str) -> str:
    stdout, _ = subprocess.Popen(
        argv, stdout=subprocess.PIPE, stdin=subprocess.PIPE
    ).communicate(input=stdin.encode())
    return stdout.decode()


def send_inline_with(command: str) -> Callable:
    def send_inline(update: Update, context: CallbackContext) -> None:
        stdout = run_command(command, update.inline_query.query)
        update.inline_query.answer(
            [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title=stdout,
                    input_message_content=InputTextMessageContent(stdout),
                ),
            ]
        )

    return send_inline


def reply_with(command: str) -> Callable:
    def reply(update: Update, context: CallbackContext) -> None:
        update.message.reply_text(run_command(command, update.message.text))

    return reply


@click.command()
@click.argument("command")
def run(command: str):
    """A telegram bot which runs every message through a specific stdin-stdout filter."""
    updater = Updater(telebots.token.get_token())

    updater.dispatcher.add_handler(MessageHandler(Filters.text, reply_with(command)))
    updater.dispatcher.add_handler(InlineQueryHandler(send_inline_with(command)))

    updater.start_polling()
    updater.idle()
