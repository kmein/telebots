from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    CallbackContext,
    Filters,
    MessageHandler,
    Updater,
)
import telebots.token
import proverb_pro

SEND_PIC = "📷"  # ":camera:"
SEND_TEXT = "💬"  # ":speech_balloon:"
PHOTO_OR_TEXT = 0


def proverb_photo(update: Update, context: CallbackContext) -> None:
    img_file_path = proverb_pro.apply_proverb(
        proverb_pro.get_random_image(), proverb_pro.get_proverb()
    )
    update.message.reply_photo(open(img_file_path, "rb"))


def proverb_text(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(proverb_pro.get_proverb())


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Yo!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=SEND_PIC), KeyboardButton(text=SEND_TEXT)]]
        ),
    )


def run():
    """A telegram bot which generates German nonsense proverbs."""
    updater = Updater(token=telebots.token.get_token())
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex(SEND_PIC), proverb_photo)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex(SEND_TEXT), proverb_text)
    )
    updater.dispatcher.add_handler(MessageHandler(Filters.all, start))
    updater.start_polling()
    updater.idle()
