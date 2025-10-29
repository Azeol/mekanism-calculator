from dataclasses import dataclass
from typing import Tuple, List
from math import ceil
from calc.constants import CONST

@dataclass
class FissionReactor:
    x: int = 0
    z: int = 0
    y: int = 0
    fuel_assemblies: int = 0
    control_rods: int = 0
    water_burn_rate: int = 0  # mB/t
    heat_capacity: int = 0    # J/K
    fuel_surface_area: int = 0  # m^2 (block faces)
    boil_efficiency: float = 0.0
    max_burn_rate: int = 0  # mB/t, equals number of fuel assemblies in this model

    def fission_print(self) -> None:
        print(f"A {self.x}x{self.z}x{self.y} Fission Reactor")
        print(f"- Fuel Assemblies {self.fuel_assemblies}, and Control Rods {self.control_rods}")
        print(f"- Water Burn Rate {self.water_burn_rate} mB/t")
        print(f"- Fuel Surface Area {self.fuel_surface_area} (m2), Boil Efficiency {self.boil_efficiency:.3f}")
        print(f"- Max Burn Rate {self.max_burn_rate} mB/t")
        print(f"- Heat Capacity {self.heat_capacity} J/K")

    def summarize(self) -> str:
        return f"A {self.x}x{self.z}x{self.y} Fission Reactor"


# ---------- Utility Functions ----------

def area_inside_reactor(x: int, z: int, y: int) -> int:
    """Area (volume) inside the casing, excluding structure thickness."""
    return (x - 2) * (z - 2) * (y - 2)


def fuel_assemblies_dimensions(x: int, z: int, y: int) -> Tuple[int, int]:
    """Compute number of fuel assemblies and control rods for given outer dims.
    Assumes checker pattern: approximately half of x*z positions are fuel rods per layer.
    """
    ideal_area_slice = ceil((x - 2) * (z - 2) / 2.0)
    num_fuel_assemblies = ideal_area_slice * (y - 3)
    num_control_rods = ideal_area_slice
    return num_fuel_assemblies, num_control_rods


def heat_capacity(x: int, z: int, y: int) -> int:
    top_bottom = x * z * 2
    front_back = x * (y - 2) * 2
    left_right = (z - 2) * (y - 2) * 2
    return (top_bottom + front_back + left_right) * CONST["CASING_HEAT_CAPACITY"]


def _divisors_sorted(n: int) -> List[int]:
    """Return all positive divisors of n sorted ascending."""
    if n <= 0:
        return []
    small, large = [], []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d * d != n:
                large.append(n // d)
        d += 1
    return small + list(reversed(large))


def optimal_structure(fuel_assemblies: int) -> Tuple[int, int, int]:
    """Pick an x,z,y based on the 'middle' factor pair heuristic.
    Returns outer dimensions (including casing), i.e., add +2 thickness each axis.
    """
    factors = _divisors_sorted(fuel_assemblies)
    if not factors:
        return 3, 3, 4  # minimal valid size fallback
    factor_length = len(factors)
    middle = factor_length // 2 - 1 if factor_length >= 2 else 0
    first_value = factors[middle]
    second_value = factors[factor_length - 1 - middle]
    difference = 2
    x = int(first_value) + 2
    z = int(second_value) + 2
    y = difference + 1 + 2  # Plus 1 for controllers, then casing +2
    return x, z, y

# ---------- Core Functions ----------

def optimal_fission_with_dimensions(x: int, z: int, y: int) -> FissionReactor:
    # Validate bounds 
    if x < CONST["MIN_REACTOR_BASE"]:
        print("Reactor length too small, min 3 blocks.")
    elif x > CONST["MAX_REACTOR_BASE"]:
        print("Reactor length too large, max 18 blocks.")
    if z < CONST["MIN_REACTOR_BASE"]:
        print("Reactor width too small, min 3 blocks.")
    elif z > CONST["MAX_REACTOR_BASE"]:
        print("Reactor width too large, max 18 blocks.")
    if y < CONST["MIN_REACTOR_HEIGHT"]:
        print("Reactor height too small, min 4 blocks.")
    elif y > CONST["MAX_REACTOR_HEIGHT"]:
        print("Reactor height too large, max 18 blocks.")

    fuel_assemblies, control_rods = fuel_assemblies_dimensions(x, z, y)
    water_burn_rate = fuel_assemblies * CONST["FISSION_STEAM_PER_FUEL"]
    return FissionReactor(
        x=x,
        z=z,
        y=y,
        fuel_assemblies=fuel_assemblies,
        control_rods=control_rods,
        water_burn_rate=water_burn_rate,
    )


def turbine_based_fission_reactor(max_flow: int) -> FissionReactor:
    """Creates a fission reactor based on the max flow rate from the turbine.
       Works with both water-cooled and sodium-cooled reactors.   
    """

    # Compute fuel assemblies from max flow
    # No need to convert coolant type here because sodium is passing though boiler not the turbine
    fuel_assemblies = max_flow // CONST["FISSION_STEAM_PER_FUEL"]
    
    reactor = FissionReactor(fuel_assemblies=fuel_assemblies)

    # Find larger than needed reactor, then shave it off
    for i in range(4, CONST["MAX_REACTOR_BASE"]):
        x_inner = i - 2
        y_inner = i - 2
        z_inner = i - 2
        efficient_area = int(ceil((x_inner * z_inner) / 2.0)) * y_inner
        control_rods = int(ceil((x_inner * x_inner) / 2.0))
        if efficient_area > fuel_assemblies + control_rods:
            reactor.x = x_inner + 2
            reactor.y = y_inner + 2
            reactor.z = z_inner + 2
            reactor.control_rods = control_rods
            break

    # Check if x can be reduced by 1
    x_inner = reactor.x - 3
    y_inner = reactor.y - 2
    z_inner = reactor.z - 2
    area = (x_inner * y_inner * z_inner) // 2
    control_rods = (x_inner * z_inner) // 2
    if area >= fuel_assemblies + control_rods:
        reactor.x -= 1
        reactor.control_rods = control_rods

    # Check if y can be reduced by 1
    y_inner = reactor.y - 3
    x_inner = reactor.x - 2
    z_inner = reactor.z - 2
    area = (x_inner * y_inner * z_inner) // 2
    if area >= fuel_assemblies + control_rods:
        reactor.y -= 1

    # Surface area
    surface_area = fuel_assemblies * 6
    levels = fuel_assemblies // max(reactor.control_rods, 1)
    if levels <= 1:
        touching_assemblies = 0
    elif levels == 2:
        touching_assemblies = reactor.control_rods * 2
    else:
        touching_assemblies = reactor.control_rods * 2 + reactor.control_rods * levels - 2
    surface_area -= touching_assemblies

    # Efficiency rate
    avg_surface_area = surface_area / fuel_assemblies if fuel_assemblies > 0 else 0.0
    boil_efficiency = min(avg_surface_area / CONST["FISSION_SURFACE_AREA_TARGET"], 1.0) if fuel_assemblies > 0 else 0.0

    reactor.water_burn_rate = fuel_assemblies * CONST["FISSION_STEAM_PER_FUEL"]
    reactor.heat_capacity = heat_capacity(reactor.x, reactor.z, reactor.y)
    reactor.fuel_surface_area = surface_area
    reactor.boil_efficiency = float(boil_efficiency)
    reactor.max_burn_rate = fuel_assemblies
    return reactor


def optimal_fuel_assemblies(turbine) -> int:
    """Given a turbine with attributes max_flow and max_water_output, return assemblies.
    Any decimal remainder truncated.
    """
    max_flow = getattr(turbine, "max_flow", None)
    max_water_output = getattr(turbine, "max_water_output", None)
    if max_flow is None or max_water_output is None:
        raise AttributeError("turbine must have 'max_flow' and 'max_water_output' attributes")
    return min(int(max_flow), int(max_water_output)) // CONST["FISSION_STEAM_PER_FUEL"]


# ---------- compatibility wrapper to preserve existing CLI ----------

def compute_reactor_size(fuel_rate_wanted: float) -> Tuple[int, Tuple[int, int]]:
    """Compatibility wrapper for the existing CLI.
    Returns (assemblies_needed, (base, height)).
    """
    if fuel_rate_wanted < CONST["MIN_BURN_RATE"] or fuel_rate_wanted > CONST["MAX_BURN_RATE"]:
        raise ValueError("Fuel burn rate out of bounds. Only one reactor is supported")

    assemblies_needed = int(ceil(fuel_rate_wanted))  # 1 assembly = 1 mB/t (ceil to ensure enough)

    for base in range(CONST["MIN_REACTOR_BASE"], CONST["MAX_REACTOR_BASE"]):
        for height in range(CONST["MIN_REACTOR_HEIGHT"], CONST["MAX_REACTOR_HEIGHT"]):
            internal_volume = (base - 2) * (base - 2) * (height - 3)
            if internal_volume >= ceil(assemblies_needed * 2):
                return assemblies_needed, (base, height)

    # Fallback to a structure derived from factorization if loops didn't return
    x, z, y = optimal_structure(assemblies_needed)
    return assemblies_needed, (x, y)