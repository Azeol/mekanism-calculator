from dataclasses import dataclass
from typing import Tuple, List, Optional
from math import ceil
from calc.constants import CONST

@dataclass
class Turbine:
    x_z: int = 0
    y: int = 0
    vents: int = 0
    dispersers: int = 0
    condensers: int = 0
    shaft_height: int = 0
    blades: int = 0   
    coils: int = 0
    capacity: int = 0  # mB of steam the turbine can hold
    max_flow: int = 0  # mB/t of steam the turbine can handle
    tank_volume: int = 0  # mB of steam the tanks can hold
    max_production: float = 0  # mB/t of water the turbine can output
    max_water_output: int = 0  # mB/t of water the turbine can output
    energy_si_prefix: str = "base"
        
    def turbine_print(self):
        print(f"A {self.x_z}x{self.x_z}x{self.y} Turbine")
        print(f"- Shaft {self.shaft_height}, Blades {self.blades}, Coils {self.coils}")
        print(f"- Vents {self.vents}")
        print(f"- Dispersers {self.dispersers}")
        print(f"- Condensers {self.condensers}")
        print(f"- Max Flow Rate {self.max_flow} mB/t, Max Water Output {self.max_water_output} mB/t")
        print(f"- Capacity {self.capacity} mB, Max Energy Production {self.max_production:.2f} mJ\n")
        
    def summarize(self) -> str:
        return f"A {self.x_z}x{self.x_z}x{self.y} Turbine"

# ---------- Utility Functions ----------

def pressure_dispersers(x_z: int) -> int:
    """Calculate number of dispersers for given turbine base dimension."""
    area_slice = (x_z - 2) ** 2 - 1 # exclude shaft
    return area_slice

def coils_needed(num_blades: int) -> int:
    """Calculate number of coils needed for given number of blades."""
    return max(int(ceil(num_blades / CONST["TURBINE_COIL_PER_BLADES"])), 2)

def lower_volume(x_z: int, shaft_height: int) -> int:
    """Calculate the volume of the lower part of the turbine (below blades)."""
    return x_z ** 2 * shaft_height

def max_vents(x_z: int, y: int, shaft_height: int) -> int:
    """Calculate maximum number of vents for given turbine dimensions."""
    remaining_height = y - 2 - shaft_height
    if remaining_height <= 0:
        return 0
    top_vents = (x_z - 2) ** 2
    side_vents = max(remaining_height * (x_z - 2) * 4, 0)
    return top_vents + side_vents

def max_flow_rate(x_z: int, shaft_height: int, vent_count: int) -> int:
    """Calculate maximum flow rate for given turbine dimensions and vent count."""
    tank_flow = pressure_dispersers(x_z) * CONST["GENERAL_DISPERSER_GAS_FLOW"] * lower_volume(x_z, shaft_height)
    vent_flow = vent_count * CONST["GENERAL_VENT_GAS_FLOW"]
    return min(tank_flow, vent_flow)

def optimal_condensers(x_z: int, y: int, shaft_height: int, coils: int, max_flow: int) -> int:
    """Calculate optimal number of condensers for given turbine dimensions and coils."""
    remaining_y = (y - 3) - shaft_height
    available_space = remaining_y * (x_z - 2) ** 2 - coils
    return min(int(ceil(max_flow / CONST["GENERAL_CONDENSER_RATE"])), available_space)

def max_water_output(condensers: int) -> int:
    """Calculate water output for given number of condensers."""
    return condensers * CONST["GENERAL_CONDENSER_RATE"]

def blade_rate(blades: int, coils: int) -> float:
    """Calculate energy production rate for given number of blades and coils."""
    blade_rate_1 = blades / 28.0
    blade_rate_2 = (coils * CONST["TURBINE_COIL_PER_BLADES"]) / 28.0
    return min(blade_rate_1, blade_rate_2)

def max_energy_prod(blades: int, coils: int, x_z: int, shaft_height: int, vents: int) -> float:
    """Calculate maximum energy production for given turbine parameters."""
    return CONST["MAX_ENERGY_PER_STEAM"] * blade_rate(blades, coils) * max_flow_rate(x_z, shaft_height, vents)

def steam_capacity(x_z: int, shaft_height: int) -> int:
    """Calculate steam capacity for given turbine dimensions."""
    return x_z ** 2 * shaft_height * CONST["GAS_PER_TANK"]

def energy_capacity(x_z: int, shaft_height: int) -> int:
    """Calculate energy capacity for given turbine dimensions."""
    return x_z ** 2 * shaft_height * 16_000

# ---------- Core Functions ----------

def min_height(shaft_height: int, coils: int, condensers: int, x_z: int, vents: int) -> int:
    """Finds minimum height where all components fit inside the turbine."""
    for y in range(shaft_height + 3, CONST["TURBINE_MAX_HEIGHT"] + 1):
        upper_y = y - shaft_height - 2
        internal_volume = (upper_y - 1) * (x_z - 2) ** 2
        if internal_volume < (coils + condensers):
            continue
        
        side_area = upper_y * (x_z - 2) * 4
        top_area = (x_z - 2) ** 2
        if (side_area + top_area) >= vents:
            return y  
    return 0

def best_vent_count(turbine: Turbine) -> Tuple[int, float]:
    """Find vent count giving best energy output for given turbine geometry."""
    best_vent_count = 0
    best_energy_production = 0.0
    
    for vent_count in range(1, max_vents(turbine.x_z, turbine.y, turbine.shaft_height) + 1):
        max_flow = max_flow_rate(turbine.x_z, turbine.shaft_height, vent_count)
        condensers = optimal_condensers(turbine.x_z, turbine.y, turbine.shaft_height, turbine.coils, max_flow)
        if condensers < 0:
            continue
        
        energy_prod = max_energy_prod(turbine.blades, turbine.coils, turbine.x_z, turbine.shaft_height, vent_count)
        if energy_prod > best_energy_production:
            best_energy_production = energy_prod
            best_vent_count = vent_count
    
    return best_vent_count, best_energy_production

def turbine_size(
    x_z: int,
    y: int,
    condensers: int,
    dispersers: int,
    vents: int,
    shaft_height: int,
    blades: int,
    coils: int
) -> Turbine:
    """Builds a turbine object based on the provided parameters."""
    return Turbine(
        x_z= x_z,
        y= y,
        vents= vents,
        dispersers= dispersers,
        condensers= condensers,
        shaft_height= shaft_height,
        blades= blades,
        coils= coils,
        capacity= energy_capacity(x_z, y),
        max_flow= max_flow_rate(x_z, shaft_height, vents),
        tank_volume= lower_volume(x_z, shaft_height),
        max_water_output= max_water_output(condensers)
    )
    
def turbine_based_on_fission_reactor(water_burn_rate: int) -> Optional[Turbine]:
    """Return most optimal turbine for given fission reactor water burn rate."""
    requiered_condensers = ceil(water_burn_rate / CONST["GENERAL_CONDENSER_RATE"])
    vents = ceil(water_burn_rate / CONST["GENERAL_VENT_GAS_FLOW"])
    all_turbines: List[Turbine] = []
    
    for length in range(5, 18, 2):
        dispersers = pressure_dispersers(length)
        max_shaft_height = min(2 * length - 5, CONST["TURBINE_MAX_ROTOR_HEIGHT"])
        
        for shaft_height in range(1, max_shaft_height):
            blades = shaft_height * 2
            coils = coils_needed(blades)
            
            t = Turbine(
                x_z= length,
                shaft_height = shaft_height,
                dispersers= dispersers,
                blades= blades,
                coils= coils,
                vents= vents
            )
            t.y = min_height(shaft_height, coils, requiered_condensers, length, vents)
            t.max_production = max_energy_prod(blades, coils, length, shaft_height, vents)
            t.max_flow = max_flow_rate(length, shaft_height, vents)
            t.condensers = optimal_condensers(length, t.y, shaft_height, coils, t.max_flow)
            t.max_water_output = max_water_output(t.condensers)
            t.capacity = energy_capacity(length, t.y)
            t.tank_volume = lower_volume(length, shaft_height)
            all_turbines.append(t)
    
    # Filter only valid turbines
    valid = [
        t for t in all_turbines
        if min(t.max_flow, t.max_water_output) >= water_burn_rate
        and t.condensers >= requiered_condensers
    ]
    
    if not valid:
        raise ValueError("No valid turbine configuration found for the given water burn rate.")
    
    # Remove inefficient turbines
    final_list = []
    for t in valid:
        keep = True
        for other in valid:
            if t.x_z == other.x_z and t.max_production < other.max_production:
                keep = False
                break
            if keep:
                final_list.append(t)

    return max(final_list, key=lambda t: t.max_production)

def optimal_turbine_with_dimensions(x_z: int, y: int) -> Turbine :
    """Returns most optimal turbine for given dimensions."""
    if x_z < CONST["TURBINE_MIN_BASE"] or x_z > CONST["TURBINE_MAX_BASE"]:
        raise ValueError(f"Turbine base {x_z} out of bounds ({CONST['TURBINE_MIN_BASE']}-{CONST['TURBINE_MAX_BASE']})")
    if y < CONST["TURBINE_MIN_HEIGHT"] or y > CONST["TURBINE_MAX_HEIGHT"]:
        raise ValueError(f"Turbine height {y} out of bounds ({CONST['TURBINE_MIN_HEIGHT']}-{CONST['TURBINE_MAX_HEIGHT']})")
    if x_z % 2 == 0:
        raise ValueError("Turbine length cannot be even (shaft must be centered).")
    
    best_turbine = None
    best_energy = 0.0

    for shaft_height in range(1, min(2 * y - CONST["TURBINE_MIN_ROTOR_HEIGHT"], CONST["TURBINE_MAX_ROTOR_HEIGHT"])):
        blades = shaft_height * 2
        coils = coils_needed(blades)
        
        tmp = Turbine(x_z=x_z, y=y, shaft_height=shaft_height, blades=blades, coils=coils)
        vent_count, energy_prod = best_vent_count(tmp)
        max_flow = max_flow_rate(x_z, shaft_height, vent_count)
        condensers = optimal_condensers(x_z, y, shaft_height, coils, max_flow)
        water_output = max_water_output(condensers)
        
        if energy_prod > best_energy:
            best_energy = energy_prod
            best_turbine = Turbine(
                x_z= x_z,
                y= y,
                vents= vent_count,
                dispersers= pressure_dispersers(x_z),
                condensers= condensers,
                shaft_height= shaft_height,
                blades= blades,
                coils= coils,
                capacity= energy_capacity(x_z, y),
                max_flow= max_flow,
                tank_volume= lower_volume(x_z, shaft_height),
                max_water_output= water_output,
                max_production= energy_prod
            )
            
    if not best_turbine:
        raise ValueError("No valid turbine configuration found for the given dimensions.")
    return best_turbine