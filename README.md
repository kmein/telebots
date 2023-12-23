# telebots

## Introducing:

## telegram-betacode
This bot converts [Greek beta code](https://en.wikipedia.org/wiki/Beta_Code#Greek_alphabet) to the precomposed [polytonic](https://en.wikipedia.org/wiki/Greek_diacritics) Unicode symbols.

## telegram-horoscope
This bot generates astrological [birth charts](https://en.wikipedia.org/wiki/Horoscope) for a supplied date/time and location. Note that this bot depends on `pdflatex` being installed and requires a Google Maps API key for using the [Timezone API](https://developers.google.com/maps/documentation/timezone/overview).

## telegram-reverse
This bot reverses what you send it, whether it be text, audio, or images.

## telegram-proverb
This bot generates inspiring but nonsensical proverbs and images.

## telegram-wrapper
This bot pipes every text it gets through a shell command (supplied as a command-line argument to `telegram-wrapper`).
For example, `telegram-wrapper rev` will call the UNIX `rev` program on every text the bot is sent, reversing it.

## telegram-streaming-link
This bot converts from YouTube Music to Spotify links, utilizing [@omijn's website](https://github.com/omijn/yt2spotify).

## Installation
Please run `poetry install` and then contact the
[BotFather](https://telegram.me/botfather) and send `/newbot` to obtain a bot token.

This token has to be stored in the `TELEGRAM_BOT_TOKEN` environment variable when running one of the bots.
