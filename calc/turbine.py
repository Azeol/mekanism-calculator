from calc.constants import CONST
from math import ceil

def compute_turbine_size(fuel_rate_wanted: float):
    """
    Compute the turbine size needed to handle the steam output from a reactor.
    
    :param fuel_rate_wanted: Desired fuel burn rate of the reactor in mB/t
    :return: Required turbine size as (base, height), , water flow rate in mB/t and produced energy in RF/t
    """
    # Computes the water flow rate
    water_flow_rate = fuel_rate_wanted * CONST["FISSION_STEAM_PER_FUEL"]
    
    # Computes the turbine size needed
    
    