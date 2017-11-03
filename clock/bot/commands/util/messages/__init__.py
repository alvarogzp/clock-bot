from bot.storage import Cache

from clock.bot.commands.util.messages.help import HelpMessageBuilder
from clock.bot.commands.util.messages.no_results import NoResultsMessageBuilder
from clock.bot.commands.util.messages.start import StartMessageBuilder


def start(cache: Cache):
    return StartMessageBuilder(cache).get_message()


def help(cache: Cache):
    return HelpMessageBuilder(cache).get_message()
