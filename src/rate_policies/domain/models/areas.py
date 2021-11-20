from __future__ import annotations
from typing import List

from geojson_pydantic import Polygon
from geopy.distance import distance
from pydantic import BaseModel


class Location(BaseModel):
    lat: float
    lng: float

    def tuple(self) -> tuple:
        return self.lat, self.lng

    def distance_from(self, other: Location) -> float:
        return distance(self.tuple(), other.tuple()).m


class Area(BaseModel):
    area_id: int
    area_boundary: Polygon
    area_center: Location
    area_coords: List[Location]


class ForbiddenArea(BaseModel):
    forbidden_area_id: int
    forbidden_area_boundary: Polygon
    forbidden_area_coords: List[Location]


class ParkingZone(BaseModel):
    parkingzone_id: int
    parkingzone_center: Location
    parkingzone_radius: float

    def includes(self, location: Location):
        dist = self.parkingzone_center.distance_from(location)
        if dist > self.parkingzone_radius:
            return False
        else:
            return True
