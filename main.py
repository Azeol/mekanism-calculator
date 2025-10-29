from calc.reactor import *
from calc.turbine import *
from calc.boiler import *


def main():
    print("=== Mekanism Fission Reactor Calculation ===")
    print("Choose an option :")
    print("1. Water-cool reactor setup")
    print("2. Sodium-cool reactor setup")
    print("3. Other calculations")
    
    choice1 = input("Enter choice (1/2/3): ")
    
    if choice1 == '1':
        print("You selected Water-cool reactor setup.")
        setup = "water"
        sub_choice1 = input("Calculate reactor from (1) Desired Turbine Flow or (2) Reactor Dimensions : ")
        if sub_choice1 == '1':
            max_flow = int(input("Enter the desired max steam flow rate (mB/t): "))
            reactor = turbine_based_fission_reactor(max_flow)
            turbine = turbine_based_on_fission_reactor(reactor.water_burn_rate)
            
            reactor.fission_print()
            turbine.turbine_print()
            
        elif sub_choice1 == '2':
            x = int(input("Enter reactor length (x): "))
            z = int(input("Enter reactor width (z): "))
            y = int(input("Enter reactor height (y): "))
            reactor = optimal_fission_with_dimensions(x, z, y)
            turbine = turbine_based_on_fission_reactor(reactor.water_burn_rate)
            
            reactor.fission_print()
            print("\n")
            turbine.turbine_print()

    elif choice1 == '2':
        print("You selected Sodium-cool reactor setup.")
        setup = "sodium"
        
    elif choice1 == '3':
        print("You selected Other calculations.")
        

if __name__ == "__main__":
    main()