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
the telegram-bot-framework requires a few configuration options
that must be set before running it (like the auth token and admin user).

Please, refer to the [telegram-bot-framework configuration section](https://github.com/alvarogzp/telegram-bot-framework#configuration)
to set them.

There are also configuration options specific to this bot.
They are optional and if not specified their default values are used.
They must be defined along with telegram-bot-framework configuration options (ie. in the same directory).
The recognised options are:
 - `enable_countries`, which, if defined and not empty, will make the bot return a 'country' as the first result with all country time zones when a country code is specified. By default, it is disabled.
 - `locales_to_cache_on_startup`, that can have a space-separated or newline-separated list of locale codes to be cached on startup. By default, `en_US` and `es_ES` locales are cached.
 - `min_query_workers`, with the number of minimum workers that must be always ready to process inline requests. By default, 1 worker is always ready.
 - `max_query_workers`, with the number of maximum workers that can be spawned to process inline requests under heavy load situations. By default, 8 workers are allowed.

Once configured, you can run the `main.py` file directly, or the
`run.sh` script that will set-up a virtual environment and install
all dependencies before running the bot.


## Architecture

This bot uses the [**telegram-bot-framework**](https://github.com/alvarogzp/telegram-bot-framework).
The code that integrates with it is in the [`clock.bot`](clock/bot) package.
Other frameworks may be added in the future.

The [`clock.finder`](clock/finder) package contains the search component of the bot.
It has several search strategies that are used based on the type of query received and the user locale.


## Developed by

- Alvaro Gutierrez Perez
  - alvarogzp@gmail.com
  - https://linkedin.com/in/alvarogzp
