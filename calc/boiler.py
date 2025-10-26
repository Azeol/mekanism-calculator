from calc.constants import CONST
from math import ceil

def compute_boiler_size(reactor_fuel_rate: float):
    """
    Compute the boiler size needed to handle the steam output from a reactor.
    
    :param reactor_fuel_rate: Fuel burn rate of the reactor in mB/t
    :return: Required boiler size as (base, height)
    """
    #