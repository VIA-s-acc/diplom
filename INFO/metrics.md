[BACK](../README.MD)

# HarvestMetrics.md

## HarvestMetrics Class
The `HarvestMetrics` class represents the harvest metrics for different crops such as wheat, corn, soybean, and potato. Each crop has a maximum harvest level and a metric function that calculates the harvest based on the water level. The class provides properties to get the maximum harvest level of each crop.

### Properties
- `wheat_max_harvest_level`: Maximum harvest level for wheat.
- `corn_max_harvest_level`: Maximum harvest level for corn.
- `soybean_max_harvest_level`: Maximum harvest level for soybean.
- `potato_max_harvest_level`: Maximum harvest level for potato.

### Methods
- `__init__(self)`: Initializes the harvest metrics with the maximum harvest levels for each crop.
- `wheat_metric_function(self, water_level: float) -> float`: Calculates the harvest for wheat based on the water level.
- `corn_metric_function(self, water_level: float) -> float`: Calculates the harvest for corn based on the water level.
- `soybean_metric_function(self, water_level: float) -> float`: Calculates the harvest for soybean based on the water level.
- `potato_metric_function(self, water_level: float) -> float`: Calculates the harvest for potato based on the water level.
