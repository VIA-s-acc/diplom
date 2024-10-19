# README.md

- [FIELD](INFO/field.md)
- [WATERING MACHINE](INFO/machine.md)
- [HARVEST METRICS](INFO/metrics.md)

## Field Class
The `Field` class represents a field with a certain number of rows and columns. Each cell in the field has a water level, which is a floating-point number between 0 and the maximum water level. The class provides methods to get and set the water level of a cell, get the average water level of the field, and copy the field to a new instance.

## WateringMachine Class
The `WateringMachine` class represents a watering machine with certain parameters such as speed, water per second, horizontal and vertical radius, maximum water level, and the field it is watering. The class provides methods to calculate the harvest coefficient, calculate the harvest in kg, calculate the profit after adding water to the field, and water the field.

## HarvestMetrics Class
The `HarvestMetrics` class represents the harvest metrics for different crops such as wheat, corn, soybean, and potato. Each crop has a maximum harvest level and a metric function that calculates the harvest based on the water level. The class provides properties to get the maximum harvest level of each crop.

## Field Machine Metric
The `Field Machine Metric` is a concept that represents the relationship between the field, the watering machine, and the harvest metrics. It describes how the watering machine affects the harvest of different crops in the field based on the water level. The `WateringMachine` class provides methods to calculate the harvest coefficient and harvest in kg based on the field and the selected metric function. The `HarvestMetrics` class provides the metric functions for different crops.