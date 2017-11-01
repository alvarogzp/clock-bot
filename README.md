# [🌍 🕒 World Times 🕘 🌎](https://t.me/WorldTimesBot)

This repository contains the source code of [@WorldTimesBot](https://t.me/WorldTimesBot),
a telegram bot that allows to get the current time of any place in the world.


## Usage

The bot works in [inline mode](https://core.telegram.org/bots/inline),
so you can use it in any chat or group without having to add the bot to it.

To use it, you must write a message on the chat where you would like to use it.
The message must start with an `@` character followed by the bot name (`WorldTimesBot`).
Then add an empty space and you will start immediately seeing the current times
in your country (based on the locale telegram sends to us).

You can tap on any of the results to send it to the current chat.

If you want to get the current time of any other place, just type (after the `@WorldTimesBot ` part)
the country name, the time-zone location or the time-zone name and you will see the times
that matches it.

Results are always displayed in the language that Telegram tells to us that you are currently using
(usually, your device or OS language).
Also, the search is also performed on that same language, so you must write the countries and
locations in your language for them to be correctly recognized.

The language exceptions are:
  - The country codes that you can type to get all current times
    in them (eg. `US`, `ES`, `DE`).
    They are universal, so they are not translated.
  - The time-zone identifiers (eg. `America/New_York`, `Europe/Madrid`).
    They must be writen as they are defined by the standard, that is, in English.


## Configuration

If you want to run your own bot instance,
the telegram-bot framework requires a few configuration values
that must be set before running it (the auth token and admin user).

Please, refer to the [telegram-bot configuration section](https://github.com/alvarogzp/telegram-bot/blob/develop/README.md#set-up-your-own-bot-using-this-framework)
to set them.

Once configured, you can run the `main.py` file directly, or the
`run.sh` script that will set-up a virtual environment and install
all dependencies before running the bot.


## Architecture

This bot uses the [**telegram-bot**](https://github.com/alvarogzp/telegram-bot) framework.
The code that integrates with it is in the [`clock.bot`](clock/bot) package.
Other frameworks may be added in the future.

The [`clock.finder`](clock/finder) package contains the search component of the bot.
It has several search strategies that are used based on the type of query received and the user locale.


## Developed by

- Alvaro Gutierrez Perez
  - alvarogzp@gmail.com
  - https://linkedin.com/in/alvarogzp
