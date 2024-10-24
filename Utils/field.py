import random
from copy import deepcopy
class Field:
    def __init__ (self, rows, cols, length_m, width_m, max_water_level = 1.0, grid = None ):
        self.max_water_level = max_water_level
        self.length_m = length_m
        self.width_m = width_m
        
        if grid is None:
            self.rows = rows
            self.cols = cols
            self.cell_length_m = length_m / cols  # длина одной ячейки в метрах
            self.cell_width_m = width_m / rows  # ширина одной ячейки в метрах
            self.grid = self.grid = [[0.5 for _ in range(cols)] for _ in range(rows)]
            
        else:
            self.grid = grid
            self.rows = len(grid)
            self.cols = len(grid[0])
            self.cell_length_m = length_m / cols  
            self.cell_width_m = width_m / rows 
            
    
    def __getitem__(self, index):
        return self.grid[index]
    
    def set_road(self, road_row):
        for col in range(self.cols):
            self.set_water_level(road_row, col, -1)
     
    def randomize_field(self, min_v, max_v, random_function = random.uniform):
        for row in range(self.rows):
            for col in range(self.cols):
                self.set_water_level(row, col, random_function(min_v, max_v))
            
    def get_avg_water_level(self):
        """
            Get average water level in field
            
            Returns:
                float : average water level
        """
        return sum(sum(row) for row in self.grid if row[0] != -1) / (self.rows * self.cols)
        # return sum(sum(row) for row in self.grid) / (self.rows * self.cols)
            
    def set_water_level(self, row, col, level):
        """
            Set water level in field
            
            Args:
                row (int) : row index
                col (int) : col index
                level (float) : water level
        """
        # if level > self.max_water_level:
        #     raise ValueError(f"Water level can't be bigger than {self.max_water_level}")
        # if level < 0:
        #     raise ValueError("Water level can't be negative")
        
        self.grid[row][col] = min(level, self.max_water_level)

    def get_water_level(self, row, col):
        """
            Get water level in field
            
            Args:
                row (int) : row index
                col (int) : col index

            Returns:
                float : water level
        """
        return self.grid[row][col]

    def display(self, road_row = None):
        """
            Display field
        """
        print("Field:")
        
        for index in range(len(self.grid)):
            if road_row is not None and index == road_row:
                print("".join(f"{cell:<2}" for cell in "->" * (len(self.grid[index])+3)))
            else:
                print(" ".join(f"{cell:.2f}" for cell in self.grid[index]))
            
        print()
    
    def get_grid(self):
        return self.grid
    
    @staticmethod
    def empty():
        return Field(1, 1, 1, 1)
        
    @staticmethod
    def copy_from(field):
        new = deepcopy(field)
        return new


