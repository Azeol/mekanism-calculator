from calc.constants import CONST
from math import ceil

def compute_reactor_size(fuel_rate_wanted: float):
    """
    Compute the reactor size needed to achieve a desired fuel burn rate.
    
    :param fuel_rate_wanted: Desired fuel burn rate in mB/t
    :return: Numbers of fissile fuel assembly needed and an example size (as base x height)
    """
    # Validate input fuel rate
    if fuel_rate_wanted < CONST["MIN_BURN_RATE"] or fuel_rate_wanted > CONST["MAX_BURN_RATE"]:
        raise ValueError("Fuel burn rate out of bounds. Only one reactor is supported")
    
    # Calculate the number of fuel assemblies needed
    assembly_needed = fuel_rate_wanted # 1 assembly = 1 mB/t fuel burn rate
    
    # Calculate an example reactor size assuming checker pattern of fuel rods
    for base in range(CONST["MIN_REACTOR_BASE"], CONST["MAX_REACTOR_BASE"]):
        for height in range(CONST["MIN_REACTOR_HEIGHT"], CONST["MAX_REACTOR_HEIGHT"] ):
            internal_volume = (base - 2) * (base - 2) * (height - 3)  # Subtract structure blocks
            
            if internal_volume >= ceil(assembly_needed * 2): # Checker pattern: half the internal volume is fuel rods and ceiled because we can't have half a fuel rod
                return assembly_needed, (base, height)