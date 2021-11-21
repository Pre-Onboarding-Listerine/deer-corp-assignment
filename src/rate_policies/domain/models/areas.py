from __future__ import annotations
from typing import List

from geojson_pydantic import Polygon
from geopy.distance import distance
from pydantic import BaseModel


class Location(BaseModel):
    lat: float
    lng: float

    def __init__(self, lat: float, lng: float):
        super().__init__(lat=lat, lng=lng)

    def __composite_values__(self):
        return [self.lat, self.lng]

    def tuple(self) -> tuple:
        return self.lat, self.lng

    def distance_from(self, other: Location) -> float:
        return distance(self.tuple(), other.tuple()).m

    def to_point(self) -> str:
        return f"POINT({self.lat} {self.lng})"


class Area(BaseModel):
    area_id: int
    area_boundary: Polygon
    area_center: Location

    class Config:
        orm_mode = True

    def boundary_geom(self):
        coords = ",".join([f"{lat} {lng}" for lat, lng in self.area_boundary.coordinates[0]])
        return self.area_boundary.type.upper() + "((" + coords + "))"


class ForbiddenArea(BaseModel):
    forbidden_area_id: int
    forbidden_area_boundary: Polygon


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
