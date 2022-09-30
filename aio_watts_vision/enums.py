from enum import Enum

class TempUnit(str, Enum):
    # A list of all defined temperature units
    CELSIUS = "c"
    FAHRENHEIT = "f"