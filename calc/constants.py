CONST = {
    # == General Units ==
    "MB_PER_BUCKET": 1000,  # Millibuckets in one bucket
    "TICKS_PER_SECOND": 20, # Game ticks per second
    
    # == Fission Reactor ==
    "FISSION_STEAM_PER_FUEL": 20_000,     # mB of steam produced per mB of water per mB of fuel
    "FISSION_SODIUM_HEATED_PER_FUEL": 200_000,  # mB of heated sodium produced per mB of fuel
    "SODIUM_TO_STEAM_RATIO": 10,                # Ratio of sodium to steam in boilers
    "FISSION_SURFACE_AREA_TARGET": 4.0,         # target average surface area per fuel assembly
    "CASING_HEAT_CAPACITY": 1_000,              # J/K per casing block

    "MAX_REACTOR_BASE": 18,                     # Maximum base of the reactor (in blocks)
    "MAX_REACTOR_HEIGHT": 18,                   # Maximum height of the reactor (in blocks)
    "MAX_BURN_RATE": 1435,                      # Maximum burn rate (mB/t)

    "MIN_REACTOR_BASE": 3,                      # Minimum base of the reactor (in blocks)
    "MIN_REACTOR_HEIGHT": 4,                    # Minimum height of the reactor (in blocks)
    "MIN_BURN_RATE": 0.1,                       # Minimum burn rate (mB/t)
    
    "MAX_TEMPERATURE": 1200,                    # Maximum operating temperature (°K)

    # == Boiler ==
    "BOILER_WATER_PER_BLOCK": 16_000,           # mB of water processed per boiler block
    "BOILER_HEATED_COOLANT_MULT": 16,           # Multiplier for heated coolant production per boiler block
    "BOILER_STEAM_PER_BLOCK": 160_000,          # mB of steam produced per boiler block
    "BOILER_COOLANT_MULT": 1.6,                 # Multiplier for coolant consumption per boiler block
    "BOILER_SUPERHEATER_CAPACITY": 320_000,     # mB of steam superheated per superheater block
    
    "BOILER_MAX_BASE": 18,                      # Maximum base dimension of the boiler
    "BOILER_MAX_HEIGHT": 18,                     # Maximum height dimension of the boiler
    
    "BOILER_MIN_BASE": 3,                       # Minimum base dimension of the boiler
    "BOILER_MIN_HEIGHT": 4,                     # Minimum height dimension of the boiler
    
    # == Turbine ==
    "GENERAL_VENT_GAS_FLOW": 32_000,            # mB of steam vented per turbine vent block
    "GENERAL_CONDENSER_RATE": 64_000,           # mB of water condensed per turbine condenser block
    "GENERAL_DISPERSER_GAS_FLOW": 1_280,        # mB of steam dispersed per turbine disperser block
    "MAX_ENERGY_PER_STEAM": 10,                 # Maximum RF per mB of steam
    "GAS_PER_TANK": 64_000,                      # mB of gas per turbine tank block
    "TURBINE_MAX_ROTOR_HEIGHT": 14,             # to avoid blade collision
    "TURBINE_COIL_PER_BLADES": 4,               # 1 coil supports 4 blades
    "TURBINE_MAX_COILS": 7,                     # never more than 7 coils (no need beyond that)
    
    "TURBINE_MAX_BASE": 18,                     # Maximum base of the turbine (in blocks)
    "TURBINE_MAX_HEIGHT": 18,                   # Maximum height of the turbine (in blocks)
    
    "TURBINE_MIN_BASE": 5,                      # Minimum base of the turbine (in blocks)
    "TURBINE_MIN_HEIGHT": 5,                    # Minimum height of the turbine (in blocks)

    
    # == Derived Examples ==
    
    "BOILER_SODIUM_CONVERSION_FACTOR": 200_000 / 10, #sodium heat -> steam flow equivalence
    "TURBINE_FLOW_FORMULA": "min(dispersers * 1280 * volume, vents * 32000)",
}