from clock.finder.zone_finder.find_util import FindUtil


class NameZoneFinder:
    def __init__(self, zones: list):
        self._zones_lower = self.__build_zones_lower(zones)

    @staticmethod
    def __build_zones_lower(zones: list):
        return {zone.zone_name.lower(): zone for zone in zones}

    def __getitem__(self, zone_name: str):
        zone = self._zones_lower[zone_name.lower()]
        if zone.zone_name != zone_name:
            raise KeyError(zone_name)
        return zone

    def get_multiple(self, zone_names):
        return [self[zone_name] for zone_name in zone_names]

    def get_lower(self, zone_name_lower):
        return self._zones_lower.get(zone_name_lower)

    def match_lower(self, query_lower):
        return FindUtil.match_key(self._zones_lower.items(), query_lower)
