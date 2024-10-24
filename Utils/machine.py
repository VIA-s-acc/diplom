import matplotlib.pyplot as plt
from .metrics import Metrics
import concurrent.futures
from copy import deepcopy
class WateringMachine:
    def __init__(self, max_speed_mps, water_per_sec, watering_coeff, rad_x_m, rad_y_m, field, max_water_level=1.0, optimal_water_level=0.5, METRIC = Metrics.WHEAT, delta_t = 0.1):
        """

        Args:
            max_speed_mps (float): max speed in mps
            water_per_sec (float): water per second
            watering_coeff (float): watering coefficient
            rad_x_m (float): horizontal radius in meters
            rad_y_m (float): vertical radius in meters
            field (Field): field to water
            max_water_level (float): maximum water level
            delta_t (float): time step
            METRIC (Metrics): metric to optimize
            optimal_water_level (float): optimal water level
        """
        self.max_speed_mps = max_speed_mps  # speed in mps
        self.water_per_sec = water_per_sec  # water per second
        self.watering_coeff = watering_coeff  # watering coefficient
        self.rad_x_m = rad_x_m  # horizontal radius in meters
        self.rad_y_m = rad_y_m  # vertical radius in meters
        self.max_water_level = max_water_level
        self.field = field  # field to water
        self.optimal_water_level = optimal_water_level
        self.delta_t = delta_t
        self.METRIC = METRIC

        
        self.rad_x_cells = int(self.rad_x_m / self.field.cell_length_m)
        self.rad_y_cells = int(self.rad_y_m / self.field.cell_width_m)

        # speed from mps to cells/sec
        self.speed_cells_per_sec = self.max_speed_mps / self.field.cell_length_m
        
        
    
    def calculate_profit(self, current_level, water_added, target_level=0.5):
        """
            Calculate profit after adding water to field
            
            Args:
                current_level (float) : current water level
                water_added (float) : water added
                target_level (float) : target water level
                metric_func (function) : metric function
                
            Returns:
                float : profit
        """
        metric_func = self.METRIC
        new_level = min(current_level + water_added, self.max_water_level)
        profit_before = metric_func(current_level)
        profit_after = metric_func(new_level)
        # print(profit_after - profit_before)
        # print("profit_a", profit_after)
        # print("profit_b", profit_before)
        return profit_after - profit_before

    def calculate_water_deficit(self, current_level):
        """
        Calculate water deficit for a cell.
        
        Args:
            current_level (float): Current water level in the cell.
            
        Returns:
            float: Water deficit.
        """
        return max(0, self.optimal_water_level - current_level)

    
    @staticmethod
    def calculate_HC(field, METRIC = Metrics.WHEAT):
        """
            Calculate harvest coefficient
            
            Args:
                METRIC (function) : metric function
                
            Returns:
                float : harvest coefficient
        """
        grid = field.get_grid()
        total = 0
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == -1:
                    continue
                else:
                    total += METRIC(grid[r][c])
        
        return total

    @staticmethod
    def calculate_HR(field, METRIC = Metrics.WHEAT):
        """
        Calculate harvest IN TON

        Args:
            field (Field): field_
            METRIC (function) : metric function

        Returns:
            float : harvest in TON
        """
        
        grid = field.get_grid()
        total = 0
        cell_area = field.cell_length_m * field.cell_width_m
        cell_area_HA = cell_area / 10000
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == -1:
                    continue
                else:
                    total += METRIC(grid[r][c]) * cell_area_HA

        return total
        

    def t_iteration(self, t, delta_t, ax, fig, road_row, visualize=False, anim_speed=1, place_time={}, analys_table={}, tt=[], total_profit=[0]):
        """
        t iter of watering
        
        Args:
            t (float): current time
            delta_t (float): delta time
            ax (Axes): axis
            fig (Figure): figure
            road_row (int): road row
            visualize (bool, optional): visualize. Defaults to False.
            anim_speed (int, optional): animation speed. Defaults to 1.
            place_time (dict): place time
            analys_table (dict): analys table
            tt (list): time table
        """
        current_col = int(t * self.speed_cells_per_sec)
        start_col = max(0, current_col - self.rad_x_cells)
        end_col = min(self.field.cols, current_col + self.rad_x_cells + 1)
        
        potential_profit = 0
        prev_profit = 0
        time_delay = 0  

        water_per_delta_t = self.water_per_sec * delta_t * self.watering_coeff

        while potential_profit >= prev_profit:
            prev_profit = potential_profit
            for r in range(max(0, self.field.rows // 2 - self.rad_y_cells), min(self.field.rows, self.field.rows // 2 + self.rad_y_cells + 1)):
                for c in range(start_col, end_col):
                    current_level = self.field.get_water_level(r, c)
                    if current_level == -1:
                        continue
                    if current_level < self.max_water_level:
                        potential_profit += self.calculate_profit(current_level, water_per_delta_t)

            # Если прибыль увеличивается, задерживаем машину для дополнительного полива
            if potential_profit > 0 and potential_profit >= prev_profit:
                time_delay += delta_t
                if str(t) not in place_time.keys():
                    place_time[f"{t}"] = {1: [t, current_col, delta_t, potential_profit, (t+time_delay) * self.max_speed_mps + 1 - 0.5]}
                else:
                    place_time[f"{t}"][max(place_time[f"{t}"].keys()) + 1 ] = ([t, current_col, delta_t, potential_profit, (t+time_delay) * self.max_speed_mps + 1 - 0.5])
       
            
                # Обновляем уровень воды для всех клеток в радиусе
                for r in range(max(0, self.field.rows // 2 - self.rad_y_cells), min(self.field.rows, self.field.rows // 2 + self.rad_y_cells + 1)):
                    for c in range(start_col, end_col):
                        current_level = self.field.get_water_level(r, c)
                        if current_level == -1:
                            continue
                        if current_level < self.max_water_level:
                            new_level = min(current_level + water_per_delta_t, self.max_water_level)
                            self.field.set_water_level(r, c, new_level)

                # Визуализируем, если требуется
                if visualize:
                    ax.clear()
                    im = ax.imshow(self.field.get_grid(), cmap='YlGnBu', vmin=0, vmax=1)
                    ax.scatter(current_col, road_row, color='red', label='WaterMachine')
                    ax.axhline(y=road_row, color='gray', linestyle='--', linewidth=2, label='Machine Path')
                    for col in range(start_col, end_col):
                        label = 'irrigation nozzles' if col == start_col else None
                        ax.axvline(x=col, ymin=max(0, self.field.rows // 2 - self.rad_y_cells), ymax=min(self.field.rows, self.field.rows // 2 + self.rad_y_cells + 1), color='green', linestyle='--', linewidth=2, label=label)
                    ax.legend(loc='upper right', fontsize=8, frameon=True)
                    ax.set_title(f"Location = {(t+1) * self.max_speed_mps} m | Stayed at = {time_delay} s")
                    plt.draw()
                    plt.pause(1 / anim_speed)

            # Если прибыль не растет, прекращаем задержку и продолжаем движение
            if potential_profit < prev_profit:
                total_profit[0] += prev_profit
                tt[0] += time_delay
                PT_global = {
                    "T": (place_time[f"{t}"][1][0], place_time[f"{t}"][max(place_time[f"{t}"].keys())][0]),
                    "C": (place_time[f"{t}"][1][1], place_time[f"{t}"][max(place_time[f"{t}"].keys())][1]),
                    "P": prev_profit,
                    "D": (place_time[f"{t}"][1][4], place_time[f"{t}"][max(place_time[f"{t}"].keys())][4]),
                }
                place_time[f"{t}"]["Global"] = PT_global
                break

        tt[0] += delta_t
        analys_table[f"Watering Data"][f"I(n)"][f"I{t}"] = [potential_profit, True if potential_profit > 0 else False]
        return deepcopy(self.field) if visualize else None


    def water_field(self, road_row, visualize=False, anim_speed=1):
        """
        Water the field

        Args:
            road_row (int): row of the road
            visualize (bool, optional): if True, the field will be visualized. Defaults to False.
            anim_speed (int, optional): speed of the animation. Defaults to 1.
            
        """
        METRIC = self.METRIC
        total_time = int(self.field.cols / self.speed_cells_per_sec)  # Общее время полива
        place_time = {}
        analys_table = {"Harvest Data": {}, "Watering Data": {"I(n)": {}}}
        total_profit = [0]
        tt = [0]
        start_coeff = self.calculate_HC(self.field, METRIC)
        start_HR = self.calculate_HR(self.field, METRIC)
        avg_water_start = self.field.get_avg_water_level()

        if visualize:
            plt.ion()  # Включаем интерактивный режим
            fig, ax = plt.subplots()
            im = ax.imshow(self.field.get_grid(), cmap='YlGnBu', vmin=0, vmax=1)
            cbar = plt.colorbar(im, ax=ax)


        for t in range(0, total_time):
            if visualize:
                self.t_iteration(t=t, delta_t=self.delta_t, ax=ax, fig=fig, road_row=road_row, visualize=visualize, anim_speed=anim_speed, place_time=place_time, tt=tt, analys_table=analys_table, total_profit=total_profit)
            else:
                self.t_iteration(t=t, delta_t=self.delta_t, ax=None, fig=None, road_row=road_row, visualize=visualize, anim_speed=anim_speed, place_time=place_time, tt=tt, analys_table=analys_table, total_profit=total_profit)

        end_coeff = self.calculate_HC(self.field, METRIC)
        end_HR = self.calculate_HR(self.field, METRIC)
        avg_water_end = self.field.get_avg_water_level()

        if visualize:
            ax.clear()
            im = ax.imshow(self.field.get_grid(), cmap='YlGnBu', vmin=0, vmax=1)
            ax.set_title(f"Time = {tt[0]} с\nStart HC = {start_coeff} | End HC = {end_coeff}\nHC Boost = {end_coeff - start_coeff}\nHR Boost = {end_HR - start_HR}")
            plt.draw()
            plt.pause(1 / anim_speed)

        if visualize:
            plt.ioff()
            plt.show()

        analys_table[f"Watering Data"][f"Watering info"] = place_time
        analys_table[f"Harvest Data"][f"HC PLUS"] = total_profit[0]
        analys_table[f"Harvest Data"][f"HC"] = {"Start": start_coeff, "End": end_coeff}
        analys_table[f"Harvest Data"][f"Prognosed HR"] = {"Start": f"{start_HR} Ton", "End": f"{end_HR} Ton"}
        analys_table[f"Harvest Data"][f"BOOST"] = {"HC": end_coeff - start_coeff, "HR": end_HR - start_HR, "HC %": abs((end_coeff - start_coeff) / start_coeff) * 100, "HR %": abs((end_HR - start_HR) / start_HR) * 100}
        analys_table[f"Harvest Data"][f"Total time"] = tt[0] + total_time
        analys_table[f"Harvest Data"][f"AVG moisture"] = {"Start": avg_water_start, "End": avg_water_end}

        return place_time, analys_table
