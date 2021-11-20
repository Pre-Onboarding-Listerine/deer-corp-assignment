from geopy.distance import distance

from src.rate_policies.domain.models import Location


def distance_between(p1: Location, p2: Location) -> float:
    point1 = (p1.lat, p1.lng)
    point2 = (p2.lat, p2.lng)
    return distance(point1, point2).m
