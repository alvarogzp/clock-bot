from bot.api.domain import ApiObject

from clock.bot.commands.util.messages.help import HelpMessageBuilder
from clock.bot.commands.util.messages.start import StartMessageBuilder
from clock.bot.commands.util.messages.troubleshoot import TroubleshootMessageBuilder
from clock.finder.api import ZoneFinderApi


def start(bot_user: ApiObject):
    return StartMessageBuilder(bot_user).get_message()


def help(bot_user: ApiObject):
    return HelpMessageBuilder(bot_user).get_message()


def troubleshoot(user: ApiObject, zone_finder: ZoneFinderApi):
    return TroubleshootMessageBuilder(user, zone_finder).get_message()
