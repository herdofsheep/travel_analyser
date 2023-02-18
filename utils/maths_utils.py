import math


def distance_calculator(
    lat_one: float, long_one: float, lat_two: float, long_two: float
) -> float:
    earth_radius = 6371000  # metres
    phi_one = math.radians(lat_one)
    phi_two = math.radians(lat_two)
    delta_phi = math.radians(lat_two - lat_one)
    delta_lambda = math.radians(long_two - long_one)

    arc = math.sin(delta_phi / 2) ** 2 + (
        math.cos(phi_one) * math.cos(phi_two) * math.sin(delta_lambda / 2) ** 2
    )
    distance = 2 * math.atan2(math.sqrt(arc), math.sqrt(1 - arc))
    result = earth_radius * distance

    # give to 4 significant figures, which is how accurate we can realistically expect this caluculator to be.
    return float("%.4g" % result)
