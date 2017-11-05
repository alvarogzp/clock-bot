import babel
from babel import Locale


DEFAULT_LOCALE = Locale.parse("en_US")


class LocaleParser:
    @classmethod
    def parse(cls, language_code: str):
        for language_code in cls._get_language_codes(language_code):
            locale = cls._try_parse(language_code)
            if locale is not None:
                return locale
        return DEFAULT_LOCALE

    @staticmethod
    def _try_parse(language_code: str):
        """
        Try to parse the language code, returning None on failure.
        """
        try:
            return Locale.parse(language_code, sep="-")
        except Exception:
            pass

    @staticmethod
    def _get_language_codes(language_code: str):
        """
        Return all acceptable language codes for a given language code, in order of priority.
        For example, for "en_US", it would return "en_US", "en", "und_US".
        """
        # first of all, return the language code as is
        yield language_code
        # if that does not produce a valid locale, split the language code in its individual parts
        try:
            language, territory, script, variant = babel.parse_locale(language_code, sep="-")
        except Exception:
            # the language code is not valid, we cannot give more codes for it
            pass
        else:
            # return the language only (eg. "en")
            if language:
                yield language
            # return a special language code that will try to get the most common language for the territory
            if territory:
                yield "und_" + territory
