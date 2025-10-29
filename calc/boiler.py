from dataclasses import dataclass
from typing import Optional, Dict
from calc.constants import CONST


@dataclass
class Boiler:
	x: int = 0
	z: int = 0
	y: int = 0
	heating_element: int = 0  # number of Superheating Elements
	dispersers: int = 0       # number of Pressure Dispersers (should fill one internal slice)
	steam_cavity_height: int = 0  # blocks above the catch layer
	water_cavity_height: int = 0  # blocks below the catch layer
	# Derived capacities (mB)
	water_capacity: int = 0
	coolant_capacity: int = 0
	steam_capacity: int = 0
	heated_coolant_capacity: int = 0
	boil_capacity: int = 0

	def boiler_print(self) -> None:
		print(f"A {self.x}x{self.z}x{self.y} Boiler")
		print(f"- Super Heating Elements {self.heating_element}")
		print(f"- Dispersers {self.dispersers}")
		print(f"- Cavity heights (steam/water): {self.steam_cavity_height}/{self.water_cavity_height}")
		print(f"- Water Capacity {self.water_capacity} mB, Coolant Capacity {self.coolant_capacity} mB")
		print(f"- Steam Capacity {self.steam_capacity} mB, Heated Coolant Capacity {self.heated_coolant_capacity} mB")
		print(f"- Boil Capacity {self.boil_capacity} mB/t (upper bound)")

	def summarize(self) -> str:
		return f"{self.x}x{self.z}x{self.y} Boiler"

# ---------- Utility Functions ----------

# ---------- Core Functions ----------