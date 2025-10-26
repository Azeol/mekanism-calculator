from calc.reactor import *
#from calc.boiler import *
#from calc.turbine import *

def main():
    print("=== Fission Reactor Calculation (Sodium Reactor) ===")
    print("1. Calculate boiler and turbine size from fuel burn rate")
    print("2. Calculate reactor size for wanted fuel burn rate")
    
    choice = input("Select an option : ")

    if choice == '1':
        try:
            rate_str = input("Enter desired fuel burn rate (mB/t): ")
            fuel_rate = float(rate_str)
        except ValueError:
            print("Invalid number. Please enter a numeric value (e.g., 5.0)")
            return

        try:
            assemblies, (base, height) = compute_reactor_size(fuel_rate)
            print("\n=== Reactor size result ===")
            print(f"Fuel burn rate: {fuel_rate} mB/t")
            print(f"Fuel assemblies needed: {assemblies:.0f}")
            print(f"Example reactor size (base x height): {base} x {height}")
        except ValueError as e:
            print(f"Error: {e}")

        choice = input("\nDo you want to calculate boiler and turbine size for this reactor? (y/n): ")
        if choice.lower() == 'y':
            choice = '2'  # Proceed to boiler and turbine calculation
        else:
            print("Exiting the program.")
    elif choice == '2':
        print("Boiler and turbine calculation not yet implemented.")
    
        choice = input("\nDo you want to perform another calculation? (y/n): ")
        if choice.lower() == 'y':
            main()
        else:
            print("Exiting the program.")
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()