from Utils.field import Field
from Utils.machine import WateringMachine
from Utils.metrics import Metrics
import pprint


field = Field(rows=10000, cols=15000, length_m=15000, width_m=10000, max_water_level=1.0)
road_row = field.rows // 2
field.randomize_field(0, 0.4)
field.set_road(road_row)




# Поливалка с параметрами
water_machine = WateringMachine(speed_mps=1, water_per_sec=0.1, watering_coeff = 1, rad_x_m=1, rad_y_m=500, max_water_level=1.0, field=field)
time_intervals, analys = water_machine.water_field(road_row, visualize=False, anim_speed = 10, METRIC=Metrics.SOYBEAN)

# Визуализируем состояние поля до и после полива
pprint.pprint(analys[f"Harvest Data"])
# pprint.pprint(analys[f"Watering Data"])