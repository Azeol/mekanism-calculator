from mekanism.turbine import Turbine
from mekanism.boiler import Boiler
from mekanism.fission_reactor import FissionReactor

def main():
    print("=== Mekanism Structure Calculator ===")
    print("1. Calculate Turbine dimensions")
    print("2. Calculate Boiler dimensions")
    print("3. Calculate Fission Reactor dimensions")
    print("4. Calculate from Fission Reactor mb/t")
    
    choice = input("Select an option : ")
    
    if choice == '1':
        width = int(input("Width: "))
        height = int(input("Height: "))
        length = int(input("Length: "))
        turbine = Turbine(width, height, length)
        print(f"Turbine Volume: {turbine.calculate_volume()}")
