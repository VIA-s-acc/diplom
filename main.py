from Utils.field import Field
from Utils.machine import WateringMachine
import pprint
from Utils.metrics import Metrics


field = Field(rows=100, cols=150, length_m=150, width_m=100, max_water_level=1.0)
road_row = field.rows // 2
field.randomize_field(0, 0.35)
field.set_road(road_row)




# Поливалка с параметрами
water_machine = WateringMachine(speed_mps=1, water_per_sec=0.1, watering_coeff = 1, rad_x_m=1, rad_y_m=50, max_water_level=1.0, field=field)
time_intervals, analys = water_machine.water_field(road_row, visualize=True, anim_speed = 10, METRIC=Metrics.WHEAT)

# Визуализируем состояние поля до и после полива
pprint.pprint(analys[f"Harvest Data"])
pprint.pprint(analys[f"Watering Data"])