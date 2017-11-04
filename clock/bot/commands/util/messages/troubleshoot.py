from bot.action.util.textformat import FormattedText
from bot.api.domain import ApiObject

from clock.bot.commands.util.message_builder import MessageWithReplyMarkupBuilder
from clock.domain.zone import ZoneFormatter
from clock.finder.api import ZoneFinderApi
from clock.locale.country_code import CountryCode
from clock.locale.getter import LocaleGetter
from clock.locale.territory import Territory
from clock.locale.zone import LocaleToZone


class TroubleshootMessageBuilder(MessageWithReplyMarkupBuilder):
    def __init__(self, user: ApiObject, zone_finder: ZoneFinderApi):
        locale = LocaleGetter.from_user(user)
        self.language = locale.display_name
        self.country_name = Territory.with_territory(locale).territory_name or ""
        self.country_code = CountryCode.from_locale(locale)
        zone = LocaleToZone.get_zone_from_locale(locale, zone_finder)
        self.location = ZoneFormatter.location_city(zone, locale)
        self.name = zone.name(locale)
        self.zone_name = zone.zone_name

    def get_text(self):
        return FormattedText()\
            .bold("🛑 Can't find what you're looking for? 🛑").newline().newline()\
            .normal("Please, note that you have to type the search in your language.").newline()\
            .normal("The language you are currently using is: {language}").newline().newline()\
            .normal("Try typing:").newline()\
            .concat(self._bullet("country name", self.country_name))\
            .concat(self._bullet("country code", self.country_code))\
            .concat(self._bullet("time zone location", self.location))\
            .concat(self._bullet("time zone name", self.name))\
            .concat(self._bullet("time zone identifier", self.zone_name, last=True)).newline()\
            .normal("👉 Use the /help command to get more info and some cool examples.").newline().newline()\
            .normal("👉 Read the {search_page} for technical information and advanced search options.")\
            .start_format()\
            .bold(language=self.language)\
            .url(
                "search documentation page",
                "https://github.com/alvarogzp/clock-bot/wiki/Search",
                "search_page"
            )\
            .end_format()

    @staticmethod
    def _bullet(label: str, example: str, last: bool = False):
        bullet = FormattedText()\
            .normal("🔹 a {label} (eg. {example})")\
            .start_format()\
            .bold(label=label)\
            .code_inline(example=example)\
            .end_format()
        if not last:
            bullet.normal(",")
        return bullet.newline()

    def get_reply_markup(self):
        # do not return any switch_inline_query button to avoid Telegram returning the user to
        # where (s)he came from using the query string of the first switch_inline_query button in the message
        return None
