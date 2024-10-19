[BACK](../README.MD)

# WateringMachine.md

## WateringMachine Class
The `WateringMachine` class represents a watering machine with certain parameters such as speed, water per second, horizontal and vertical radius, maximum water level, and the field it is watering. The class provides methods to calculate the harvest coefficient, calculate the harvest in kg, calculate the profit after adding water to the field, and water the field.

### Methods
- `__init__(self, speed: float, water_per_second: float, horizontal_radius: float, vertical_radius: float, max_water_level: float, field: Field)`: Initializes the watering machine with the specified parameters and the field it is watering.
- `calculate_harvest_coefficient(self, metric_function: Callable[[float], float]) -> float`: Calculates the harvest coefficient based on the selected metric function.
- `calculate_harvest_in_kg(self, metric_function: Callable[[float], float]) -> float`: Calculates the harvest in kg based on the selected metric function.
- `calculate_profit_after_watering(self, metric_function: Callable[[float], float]) -> float`: Calculates the profit after adding water to the field based on the selected metric function.
- `water_field(self)`: Waters the field based on the parameters of the watering machine.
