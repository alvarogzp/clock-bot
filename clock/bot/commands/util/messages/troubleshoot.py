from bot.action.util.reply_markup.inline_keyboard.button import InlineKeyboardButton
from bot.action.util.reply_markup.inline_keyboard.markup import InlineKeyboardMarkup
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
        country_name = Territory.with_territory(locale).territory_name or ""
        country_code = CountryCode.from_locale(locale)
        zone = LocaleToZone.get_zone_from_locale(locale, zone_finder)
        location = ZoneFormatter.location_city(zone, locale)
        name = zone.name(locale)
        zone_name = zone.zone_name
        self.search_types = (
            ("country name", country_name),
            ("country code", country_code),
            ("time zone location", location),
            ("time zone name", name),
            ("time zone identifier", zone_name)
        )

    def get_text(self):
        return FormattedText()\
            .bold("🛑 Can't find what you're looking for? 🛑").newline().newline()\
            .normal("Please, note that you have to type the search in your language.").newline()\
            .normal("The language you are currently using is: {language}").newline().newline()\
            .normal("Try typing:").newline()\
            .normal("{search_types}").newline().newline()\
            .normal("👉 Use the /help command to get more info and some cool examples.").newline().newline()\
            .normal("👉 Read the {search_page} for technical information and "
                    "advanced search options.").newline().newline()\
            .bold("👇 Try the suggested searches below 👇")\
            .start_format()\
            .bold(language=self.language)\
            .concat(search_types=self._formatted_search_types())\
            .url(
                "search documentation page",
                "https://github.com/alvarogzp/clock-bot/wiki/Search",
                "search_page"
            )\
            .end_format()

    def _formatted_search_types(self):
        bullets = [self._bullet(name, value) for name, value in self.search_types]
        return FormattedText().newline().join(bullets)

    @staticmethod
    def _bullet(label: str, example: str):
        return FormattedText()\
            .normal("🔹 a {label} (eg. {example})")\
            .start_format()\
            .bold(label=label)\
            .code_inline(example=example)\
            .end_format()

    def get_reply_markup(self):
        # do not return any switch_inline_query button not using the current chat
        # to avoid Telegram returning the user to where (s)he came from
        # using the query string of that button
        button = InlineKeyboardButton.switch_inline_query
        markup = InlineKeyboardMarkup.with_fixed_columns(1)
        for name, value in self.search_types:
            text = "Search by {name} ({value})".format(name=name, value=value)
            markup.add(button(text, value))
        return markup
