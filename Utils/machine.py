import matplotlib.pyplot as plt
from .metrics import Metrics
class WateringMachine:
    def __init__(self, speed_mps, water_per_sec, watering_coeff, rad_x_m, rad_y_m, field, max_water_level=1.0):
        """

        Args:
            speed_mps (float): speed in mps
            water_per_sec (float): water per second
            watering_coeff (float): watering coefficient
            rad_x_m (float): horizontal radius in meters
            rad_y_m (float): vertical radius in meters
            field (Field): field to water
            max_water_level (float): maximum water level

        """
        self.speed_mps = speed_mps  # speed in mps
        self.water_per_sec = water_per_sec  # water per second
        self.watering_coeff = watering_coeff  # watering coefficient
        self.rad_x_m = rad_x_m  # horizontal radius in meters
        self.rad_y_m = rad_y_m  # vertical radius in meters
        self.max_water_level = max_water_level
        self.field = field  # field to water

        
        self.rad_x_cells = int(self.rad_x_m / self.field.cell_length_m)
        self.rad_y_cells = int(self.rad_y_m / self.field.cell_width_m)

        # speed from mps to cells/sec
        self.speed_cells_per_sec = self.speed_mps / self.field.cell_length_m
        
        
    
    def calculate_profit(self, current_level, water_added, target_level=0.5, metric_func = Metrics.WHEAT):
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
        new_level = min(current_level + water_added, self.max_water_level)
        profit_before = metric_func(current_level)
        profit_after = metric_func(new_level)
        # print(profit_after - profit_before)
        # print("profit_a", profit_after)
        # print("profit_b", profit_before)
        return profit_after - profit_before

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
    def calculate_HR(field, METRIC = Metrics.WHEAT, METRIC_PARAMS = None):
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
        

    def water_field(self, road_row, METRIC=Metrics.WHEAT, visualize=False, anim_speed = 1):
        """
            Water field
            
            Args:
                road_row (int) : row index of road
                METRIC (function) : metric function
                visualize (bool) : visualize field
                anim_speed (int) : animation speed
                
            Returns:
                time_intervals (list) : time intervals
                analys_table (dict) : analysis table
        """
        field = self.field
        total_time = int(self.field.cols / self.speed_cells_per_sec)
        place_time = {}
        analys_table = {}
        total_profit = 0
        analys_table[f"Harvest Data"] = {}
        analys_table[f"Watering Data"] = {}
        analys_table[f"Watering Data"][f"T(t)"] = {}
        tt = 0
        start_coeff = self.calculate_HC(field, METRIC)
        start_HR = self.calculate_HR(field, METRIC)
        avg_water_start = field.get_avg_water_level()
        if visualize:
            plt.ion()  # interactive mode on
            fig, ax = plt.subplots()
            im = ax.imshow(self.field.get_grid(), cmap='YlGnBu', vmin=0, vmax=1)
            cbar = plt.colorbar(im, ax=ax)  # 
            

            
        for t in range(total_time):
            current_col = int(t * self.speed_cells_per_sec) # current_col = t * self.speed position of WaterMachine in field in cells in t Moment
            start_col = max(0, current_col - self.rad_x_cells)
            end_col = min(self.field.cols, current_col + self.rad_x_cells + 1)
            potential_profit = 0
            prev_profit = 0
            time_delay = 0
            
            # profit 
            while potential_profit >= prev_profit:
                prev_profit = potential_profit
                for r in range(max(0, self.field.rows // 2 - self.rad_y_cells), min(self.field.rows, self.field.rows // 2 + self.rad_y_cells + 1)):
                    for c in range(start_col, end_col):
                        current_level = self.field.get_water_level(r, c)
                        if current_level == -1:
                            continue
                        if current_level < self.max_water_level:
                            potential_profit += self.calculate_profit(current_level, self.water_per_sec * self.watering_coeff, metric_func=METRIC)
                
                if potential_profit > 0 and potential_profit >= prev_profit:
                    time_delay+=1
                    place_time[f"{t}"] = [t, current_col, time_delay, potential_profit, (t+1) * self.speed_mps]
                    # Update water level
                    for r in range(max(0, self.field.rows // 2 - self.rad_y_cells), min(self.field.rows, self.field.rows // 2 + self.rad_y_cells + 1)):
                        for c in range(start_col, end_col):
                            current_level = self.field.get_water_level(r, c)
                            if current_level == -1:
                                continue
                            if current_level < self.max_water_level:
                                new_level = current_level + self.water_per_sec * self.watering_coeff
                                self.field.set_water_level(r, c, new_level)    
                                
                    # field.display()         
                    if visualize:
                        ax.clear()
                        im = ax.imshow(self.field.get_grid(), cmap='YlGnBu', vmin=0, vmax=1)
                        ax.scatter(current_col, road_row, color='red', label='WaterMachine')
                        ax.axhline(y = road_row, color='gray', linestyle='--', linewidth=2, label='Machine Path')
                        for col in range(start_col, end_col):
                            label = 'irrigation nozzles' if col == start_col else None
                            ax.axvline(x = col, ymin=max(0, self.field.rows // 2 - self.rad_y_cells), ymax=min(self.field.rows, self.field.rows // 2 + self.rad_y_cells + 1), color='green', linestyle='--', linewidth=2, label = label)
                        ax.legend(loc='upper right', fontsize=8, frameon=True)
                        ax.set_title(f"Location = {(t+1) * self.speed_mps} m | Stayed at = {time_delay} s")
                        plt.draw()
                        plt.pause(1 / anim_speed)  
                        
                
                if potential_profit < prev_profit:
                        total_profit += prev_profit
                        potential_profit = prev_profit
                        tt += time_delay
                        break 
                

                      
             
            tt += 1
            analys_table[f"Watering Data"][f"T(t)"][f"T{t}"] = [potential_profit, True if potential_profit > 0 else False]
        
        end_coeff = self.calculate_HC(field, METRIC)
        end_HR = self.calculate_HR(field, METRIC)
        avg_water_end = field.get_avg_water_level()
        
        if visualize:
            ax.clear()
            im = ax.imshow(self.field.get_grid(), cmap='YlGnBu', vmin=0, vmax=1)
            ax.set_title(f"Passed | Total Time = {tt} s\nStart HC = {start_coeff} | End HC = {end_coeff}\nStart HR = {start_HR} | End HR = {end_HR}\nHC boost = {end_coeff - start_coeff} or {((end_coeff - start_coeff) / start_coeff) * 100} %\nHR boost = {end_HR - start_HR} or {((end_HR - start_HR) / start_HR) * 100} %")
            plt.draw()
            plt.pause(1 / anim_speed)  
            
        if visualize:
            plt.ioff()  
            plt.show()   
            
        analys_table[f"Watering Data"][f"Watering info"] = place_time
        analys_table[f"Harvest Data"][f"HC PLUS"] = [total_profit, (end_coeff - start_coeff / start_coeff) * 100]
        analys_table[f"Harvest Data"][f"HC"] = {"Start": start_coeff, "End": end_coeff}
        analys_table[f"Harvest Data"][f"Prognosed HR"] = {"Start": str(start_HR)+(" Ton"), "End": str(end_HR)+(" Ton")}
        analys_table[f"Harvest Data"][f"BOOST"] = {"HC": end_coeff - start_coeff, "HR": end_HR - start_HR, "HC %": (end_coeff - start_coeff) / start_coeff * 100, "HR %": end_HR / start_HR * 100}
        analys_table[f"Harvest Data"][f"Total time"] = tt
        analys_table[f"Harvest Data"][f"AVG moisture"] = {"Start": avg_water_start, "End": avg_water_end}
    
        
        #[t, current_col, time_delay, potential_profit, (t+1) * self.speed_mps]
        #[T_1 moment, Col, DELAY IN T_1, POTENTIAL_PROFIT, LOC OF MACHINE]
        return place_time, analys_table