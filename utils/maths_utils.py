import math
from typing import Tuple


def distance_calculator_metres(loc_one_pos: Tuple[float, float], loc_two_pos: Tuple[float, float]) -> float:
    earth_radius = 6371000  # metres
    phi_one = math.radians(loc_one_pos[0])
    phi_two = math.radians(loc_two_pos[0])
    delta_phi = math.radians(loc_two_pos[0] - loc_one_pos[0])
    delta_lambda = math.radians(loc_two_pos[1] - loc_one_pos[1])

    arc = math.sin(delta_phi / 2) ** 2 + (math.cos(phi_one) * math.cos(phi_two) * math.sin(delta_lambda / 2) ** 2)
    distance = 2 * math.atan2(math.sqrt(arc), math.sqrt(1 - arc))
    result = earth_radius * distance

    # give to 4 significant figures, which is how precise we can realistically expect this caluculator to be.
    return set_to_significant_figures(result, 4)


def set_to_significant_figures(input: float, figure) -> float:
    return float(f"%.{figure}g" % input)
