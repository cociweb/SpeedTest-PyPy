import math
import random
import string

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * \
        math.sin(delta_lon/2) * math.sin(delta_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def generate_payload(size: int) -> bytes:
    """Generate random payload of specified size"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()