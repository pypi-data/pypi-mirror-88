from vade_api_src.vade_enums import *
from datetime import datetime
from dateutil import parser


class GeoPoint:
    lat: float
    long: float

    def __init__(self, lat, long):
        if isinstance(lat, str):
            self.lat = float(lat)
        if isinstance(long, str):
            self.long = float(long)
        else:
            self.lat = lat
            self.long = long

    def geopy_format(self):
        return (self.lat, self.long)

    @staticmethod
    def array_from_json(j: dict):
        try:
            ret_arr:[GeoPoint] = []
            for point in j["coordinates"][0]:
                new = GeoPoint.from_json(point)
                ret_arr.append(new)
            return ret_arr
        except:
            return None

    @staticmethod
    def from_json(j):
        if isinstance(j, dict):
            loc_dict = j.get("location", None)
            if loc_dict:
                try:
                    new_one = GeoPoint(lat=j["location"]["coordinates"][1], long=j["location"]["coordinates"][0])
                    return new_one
                except: x = 5

            geo_dict = j.get("coordinates")
            if geo_dict:
                try:
                    new_one = GeoPoint(lat=j["coordinates"][1], long=j["coordinates"][0])
                    return new_one
                except: x = 5

        try:
            new_one = GeoPoint(lat=j[1], long=j[0])
            return new_one
        except:
            return None

    @classmethod
    def fromAny(cls, lat, long):
        new_one = GeoPoint(0.0, 0.0)
        try:
            if isinstance(lat, str):
                new_one.lat = float(lat)
            if isinstance(long, str):
                new_one.long = float(long)
            if isinstance(lat, float):
                new_one.lat = lat
            if isinstance(long, float):
                new_one.long = long
            return new_one
        except Exception as e:
            return None

    def to_json(self):
        return {
            "type": "Point",
            "coordinates": [self.long, self.lat]
        }


class DefaultGeoPoints:
    new_york = GeoPoint(40.701363, -74.015451)
    raleigh = GeoPoint(35.786388, -78.647284)
    marcom_st = GeoPoint(35.778966, -78.686155)
    austin_texas = GeoPoint(30.4036922, -97.8540649)
    seattle = GeoPoint(47.59325962698753, -122.32440174831653)



class VadeSpotPoint:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y


class VadeSpotBounds:
    points: [int] = []

    @staticmethod
    def from_json(j: dict):
        try:
            new_bounds = VadeSpotBounds()
            if isinstance(j, dict):
                for bound in j["bounds"]:
                    new_bounds.points.append(VadeSpotPoint(x=bound[0], y=bound[1]))
                return new_bounds
            else:
                for bound in j:
                    new_bounds.points.append(VadeSpotPoint(x=bound[0], y=bound[1]))
                return new_bounds
        except:
            return None


class VadeSpotRealtime:
    uuid: str = None
    name: str = None
    mdid: str = None
    location: GeoPoint = None
    occupancy_threshold: float = None
    raw_score: float = None
    last_updated: datetime
    occupied: bool = None

    @staticmethod
    def from_json(j: dict):
        try:
            new_spot = VadeSpotRealtime()
            new_spot.uuid = j["uuid"]
            new_spot.name = j["name"]
            new_spot.mdid = j.get("mdid", None)
            new_spot.location = GeoPoint.from_json(j)
            if not new_spot.location:
                print("failed to create spot from json: spot has no location")
                print("original data: {}".format(j))
                return None
            new_spot.occupancy_threshold = j.get("occupancyThreshold", None)
            new_spot.raw_score = j.get("rawScore", 0.0)
            updated_str = j.get("lastUpdated", None)
            if updated_str:
                new_spot.last_updated = parser.parse(updated_str)
                new_spot.occupied = j["occupied"]
            return new_spot
        except Exception as e:
            print("failed to create spot from json: {}".format(str(e)))
            print("original data: {}".format(j))
            return None


class VadeSpotCrud(VadeSpotRealtime):

    zone: str = None
    bounds: VadeSpotBounds = []
    primary_camera: str = None
    type: VadeSpotType = VadeSpotType.STANDARD
    secondary_cameras: [str] = None

    @staticmethod
    def from_json(j: dict):
        try:
            new_spot = VadeSpotRealtime.from_json(j=j)
            new_spot.type = VadeSpotType.from_str(j.get("type", "standard"))
            new_spot.zone = j.get("zone", None)
            new_spot.bounds = VadeSpotBounds.from_json(j["bounds"])
            if not new_spot.bounds:
                return None
            new_spot.primary_camera = j["primaryCamera"]
            new_spot.secondary_cameras = j.get("secondaryCameras", None)
            new_spot.occupancy_threshold = j.get("occupancyThreshold", None)
            return new_spot
        except Exception as e:
            print("failed to create spot from json: {}".format(str(e)))
            return None


