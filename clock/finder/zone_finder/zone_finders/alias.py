from clock.finder.zone_finder.find_util import FindUtil
from clock.finder.zone_finder.zone_finders.name import NameZoneFinder


ZONE_ALIASES = {
}


class AliasZoneFinder:
    def __init__(self, name_zone_finder: NameZoneFinder):
        self.aliases_lower = self.__build_aliases_lower(name_zone_finder, ZONE_ALIASES)

    @staticmethod
    def __build_aliases_lower(name_zone_finder: NameZoneFinder, aliases: dict):
        aliases_lower = {}
        for alias, zone_name in aliases.items():
            zone = name_zone_finder[zone_name]
            aliases_lower[alias.lower()] = zone
        return aliases_lower

    def match_lower(self, query_lower: str):
        return FindUtil.match_key(self.aliases_lower.items(), query_lower)
