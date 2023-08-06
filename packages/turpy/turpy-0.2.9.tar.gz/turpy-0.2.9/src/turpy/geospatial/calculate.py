import math
import geopy
from decimal import Decimal



class GeoLocation:
    """
    Class representing a coordinate on a sphere, most likely Earth.

    This class is based from the code smaple in this paper:
        http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates

    The owner of that website, Jan Philip Matuschek, is the full owner of
    his intellectual property. This class is simply a Python port of his very
    useful Java code. All code written by Jan Philip Matuschek and ported by me
    (which is all of this class) is owned by Jan Philip Matuschek.

    :example:
    latlon = [(63.734347, 20.361874), (63.734885, 20.361887), (63.734437, 20.361876), (63.733899, 20.361862)]

    loc = GeoLocation.from_degrees(deg_lat=latlon[0][0], deg_lon=latlon[0][1]) # (63.734347, 20.361874))
    distance = 1 # 1 kilometer, 0.01 # 10 meters

    SW_loc, NE_loc = loc.bounding_locations(distance)

    # combining with s2sphere
    sw = s2sphere.LatLng.from_degrees(SW_loc.deg_lat, SW_loc.deg_lon)
    ne = s2sphere.LatLng.from_degrees(NE_loc.deg_lat, NE_loc.deg_lon)

    """

    MIN_LAT = math.radians(-90)
    MAX_LAT = math.radians(90)
    MIN_LON = math.radians(-180)
    MAX_LON = math.radians(180)

    EARTH_RADIUS = 6378.1  # kilometers

    @classmethod
    def from_degrees(cls, deg_lat, deg_lon):
        rad_lat = math.radians(deg_lat)
        rad_lon = math.radians(deg_lon)
        return GeoLocation(rad_lat, rad_lon, deg_lat, deg_lon)

    @classmethod
    def from_radians(cls, rad_lat, rad_lon):
        deg_lat = math.degrees(rad_lat)
        deg_lon = math.degrees(rad_lon)
        return GeoLocation(rad_lat, rad_lon, deg_lat, deg_lon)

    def __init__(
            self,
            rad_lat,
            rad_lon,
            deg_lat,
            deg_lon
    ):
        self.rad_lat = float(rad_lat)
        self.rad_lon = float(rad_lon)
        self.deg_lat = float(deg_lat)
        self.deg_lon = float(deg_lon)
        self._check_bounds()

    def __str__(self):
        degree_sign = u'\N{DEGREE SIGN}'
        return ("({0:.4f}deg, {1:.4f}deg) = ({2:.6f}rad, {3:.6f}rad)").format(
            self.deg_lat, self.deg_lon, self.rad_lat, self.rad_lon)

    def _check_bounds(self):
        if (self.rad_lat < GeoLocation.MIN_LAT or self.rad_lat > GeoLocation.MAX_LAT or
                self.rad_lon < GeoLocation.MIN_LON or self.rad_lon > GeoLocation.MAX_LON):
            raise Exception("Illegal arguments")

    def distance_to(self, other, radius=EARTH_RADIUS):
        """
        Computes the great circle distance between this GeoLocation instance
        and the other.
        """
        return radius * math.acos(
            math.sin(self.rad_lat) * math.sin(other.rad_lat) +
            math.cos(self.rad_lat) *
            math.cos(other.rad_lat) *
            math.cos(self.rad_lon - other.rad_lon)
        )

    def bounding_locations(self, distance, radius=EARTH_RADIUS):
        """
        Computes the bounding coordinates of all points on the surface
        of a sphere that has a great circle distance to the point represented
        by this GeoLocation instance that is less or equal to the distance argument.

        Param:
            distance - the distance from the point represented by this GeoLocation
                       instance. Must be measured in the same unit as the radius
                       argument (which is kilometers by default)

            radius   - the radius of the sphere. defaults to Earth's radius.

        Returns a list of two GeoLoations - the SW corner and the NE corner - that
        represents the bounding box.
        """

        if radius < 0 or distance < 0:
            raise Exception("Illegal arguments")

        # angular distance in radians on a great circle
        rad_dist = distance / radius

        min_lat = self.rad_lat - rad_dist
        max_lat = self.rad_lat + rad_dist

        if min_lat > GeoLocation.MIN_LAT and max_lat < GeoLocation.MAX_LAT:
            delta_lon = math.asin(math.sin(rad_dist) / math.cos(self.rad_lat))

            min_lon = self.rad_lon - delta_lon
            if min_lon < GeoLocation.MIN_LON:
                min_lon += 2 * math.pi

            max_lon = self.rad_lon + delta_lon
            if max_lon > GeoLocation.MAX_LON:
                max_lon -= 2 * math.pi
        # a pole is within the distance
        else:
            min_lat = max(min_lat, GeoLocation.MIN_LAT)
            max_lat = min(max_lat, GeoLocation.MAX_LAT)
            min_lon = GeoLocation.MIN_LON
            max_lon = GeoLocation.MAX_LON

        return [GeoLocation.from_radians(min_lat, min_lon),
                GeoLocation.from_radians(max_lat, max_lon)]


#
def midpoint_location(
    start_latitude_dd:float, 
    start_longitude_dd:float, 
    stop_latitude_dd:float, 
    stop_longitude_dd:float) -> dict():
    """Calculates a midpoint location based on the start and stop coordinates given by
    a `geolocation_dict`.

    :params :
    
    """
    #  Point tuple of(latitude, longitude)

    start = geopy.Point(latitude=Decimal(start_latitude_dd),
                        longitude=Decimal(start_longitude_dd))

    end = geopy.Point(latitude=Decimal(stop_latitude_dd),
                      longitude=Decimal(stop_longitude_dd))

    a_lat, a_lon = math.radians(start.latitude), math.radians(start.longitude)
    b_lat, b_lon = math.radians(end.latitude), math.radians(end.longitude)
    delta_lon = b_lon - a_lon
    b_x = math.cos(b_lat) * math.cos(delta_lon)
    b_y = math.cos(b_lat) * math.sin(delta_lon)
    mid_lat = math.atan2(
        math.sin(a_lat) + math.sin(b_lat),
        math.sqrt(((math.cos(a_lat) + b_x) ** 2 + b_y ** 2))
    )
    mid_lon = a_lon + math.atan2(b_y, math.cos(a_lat) + b_x)
    # Normalise
    mid_lon = (mid_lon + 3 * math.pi) % (2 * math.pi) - math.pi
    return {'latitude_dd': format(math.degrees(mid_lat), '.6f'),
            'longitude_dd': format(math.degrees(mid_lon), '.6f')}


def initial_compass_bearing(point_a, point_b):
    """Calculates the bearing between two points.

    Source: https://gist.github.com/jeromer/2005586

    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

    :Parameters:
      - `point_a: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `point_b: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

    :Returns:
      The bearing in degrees

    :Returns Type:
      float
    """
    if (type(point_a) != tuple) or (type(point_b) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(point_a[0])
    lat2 = math.radians(point_b[0])

    diff_long = math.radians(point_b[1] - point_a[1])

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
