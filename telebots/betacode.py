#!/usr/bin/env python3
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    Updater,
    InlineQueryHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from uuid import uuid4
import betacode.conv
import click
import telebots.token


def on_inline_query(update: Update, context: CallbackContext) -> None:
    greek = betacode.conv.beta_to_uni(update.inline_query.query)

    update.inline_query.answer(
        [
            InlineQueryResultArticle(
                id=uuid4(),
                title=greek,
                input_message_content=InputTextMessageContent(greek),
            ),
            InlineQueryResultArticle(
                id=uuid4(),
                title=greek.upper(),
                input_message_content=InputTextMessageContent(greek.upper()),
            ),
        ]
    )


def on_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(betacode.conv.beta_to_uni(update.message.text))


@click.command()
def run():
    bot = Updater(token=telebots.token.get_token())
    bot.dispatcher.add_handler(InlineQueryHandler(on_inline_query))
    bot.dispatcher.add_handler(MessageHandler(Filters.text, on_message))

    bot.start_polling()
    bot.idle()
