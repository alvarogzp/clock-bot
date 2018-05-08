import itertools

from clock.finder.zone_finder.find_util import FindUtil
from clock.finder.zone_finder.zone_finders.name import NameZoneFinder


ZONE_ALIASES = {
    # sorted by no-results search popularity on @ClockBot at 2018/05/07
    "Mumbai": "Asia/Kolkata",
    "Texas": ["US/Central", "US/Mountain"],
    "NewYork": "America/New_York",
    "Miami": "US/Eastern",
    "Amritsar": "Asia/Kolkata",
    "Ciudad de Mexico": "America/Mexico_City",
    "Boston": "US/Eastern",
    "San Francisco": "US/Pacific",
    "Moscu": "Europe/Moscow",
    "Houston": "US/Central",
    "Barcelona": "Europe/Madrid",
    "Milan": "Europe/Rome",
    "Stavropol": "Europe/Moscow",
    "Washington": "US/Pacific",
    "Japon": "Asia/Tokyo",
    "Lyon": "Europe/Paris",
    "Curitiba": "America/Sao_Paulo",
    "California": "US/Pacific",
    "Bandar Abbas": "Asia/Tehran",
    "Florida": ["US/Eastern", "US/Central"],
    "Karbala": "Asia/Baghdad",
    "Shiraz": "Asia/Tehran",

    "Cochabamba": "America/La_Paz",

    "La Habana": "America/Havana",

    "Catalonia": "Europe/Madrid",
    "Catalunya": "Europe/Madrid",
    "Cataluña": "Europe/Madrid",
}


class AliasZoneFinder:
    def __init__(self, name_zone_finder: NameZoneFinder):
        self.aliases_lower = self.__build_aliases_lower(name_zone_finder, ZONE_ALIASES)

    @staticmethod
    def __build_aliases_lower(name_zone_finder: NameZoneFinder, aliases: dict):
        aliases_lower = {}
        for alias, zone_names in aliases.items():
            if type(zone_names) is str:
                zone_names = [zone_names]
            zones = [name_zone_finder[zone_name] for zone_name in zone_names]
            aliases_lower[alias.lower()] = zones
        return aliases_lower

    def match_lower(self, query_lower: str):
        return [itertools.chain.from_iterable(i) for i in FindUtil.match_key(self.aliases_lower.items(), query_lower)]
