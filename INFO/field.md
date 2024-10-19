[BACK](../README.MD)

# Field.md

## Field Class
The `Field` class represents a field with a certain number of rows and columns. Each cell in the field has a water level, which is a floating-point number between 0 and the maximum water level. The class provides methods to get and set the water level of a cell, get the average water level of the field, and copy the field to a new instance.

### Methods
- `__init__(self, rows: int, cols: int, max_water_level: float)`: Initializes the field with the specified number of rows, columns, and maximum water level.
- `get_water_level(self, row: int, col: int) -> float`: Returns the water level of the cell at the specified row and column.
- `set_water_level(self, row: int, col: int, water_level: float)`: Sets the water level of the cell at the specified row and column.
- `get_average_water_level(self) -> float`: Returns the average water level of the field.
- `copy(self) -> Field`: Returns a copy of the field.
