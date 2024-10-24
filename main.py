from Utils.field import Field
from Utils.machine import WateringMachine
from Utils.metrics import Metrics
from Utils.data_convert import dict_to_csv, dict_to_excel, dict_to_json
import pprint


field = Field(rows=100, cols=100, length_m=100, width_m=100, max_water_level=1.0)
road_row = field.rows // 2
field.randomize_field(0.2,0.1)
field.set_road(road_row)




water_machine = WateringMachine(max_speed_mps=1, water_per_sec=0.01, watering_coeff = 1, rad_x_m=0.5, rad_y_m=50, max_water_level=1.0, field=field, METRIC=Metrics.SOYBEAN, delta_t=0.1)
time_intervals, analys = water_machine.water_field(road_row, visualize=False, anim_speed = 10)

# pprint.pprint(analys[f"Watering Data"])
pprint.pprint(analys[f"Harvest Data"])

dict_to_csv(analys, "data/analys.csv")
dict_to_excel(analys, "data/analys.xlsx")
dict_to_json(analys, "data/analys.json")
