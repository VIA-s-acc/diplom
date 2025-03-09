from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import numpy as np

##
# @file Field.py
# @brief This file contains the Field class, which is used to represent a field with a grid of cells.
# @version v1a
# @date 15.02.2025
# @package Field
# @brief Class for representing a field with a grid of cells
#

class Field:
    
    """!
    Field class.
    
    @brief Class for representing a field with a grid of cells.
    """
    def __init__(self, length_m, width_m, rows, cols, rx, ry, alpha, beta, Wm, Deltat, line = None, field=None):
        
        """!
        
        Constructor for Field class.
        
        @param length_m Length of the field in meters.
        @param width_m Width of the field in meters.
        @param rows Number of rows in the field.
        @param cols Number of columns in the field.
        @param rx Radius of watering in meters.
        @param ry Radius of watering in meters.
        @param alpha Coefficient for watering.
        @param beta Coefficient for watering.
        @param Wm Maximum watering in meters.
        @param Deltat Time step.
        @param line Line index of watering machine.
        @param field 2D np.array, optional
        @details Initializes the field with the given parameters and sets the moisture level of each cell to a random value between 0 and 1.
        
        """
        
        # Initializing the field
        self.rows = rows
        self.cols = cols
        self.rx = rx
        self.ry = ry
        self.alpha = alpha
        self.beta = beta
        self.Wm = Wm
        self.Deltat = Deltat
        self.line = line if line is not None else self.rows // 2  # Линия расположения машины
        self.field = field if field is not None else self.randomize_field()
        self.length_m = length_m
        self.width_m = width_m
        self.cell_length_m = length_m / cols  
        self.cell_width_m = width_m / rows  
        self.rx_cells = int(self.rx / self.cell_length_m)
        self.ry_cells = int(self.ry / self.cell_width_m)


    
    def calc_base(self, func, a = 2, b = 0.3, c = 3):
        """!
        Calculate the base value of the field.

        @param func Function to calculate the base value.
        @param a Parameter a.
        @param b Parameter b.
        @param c Parameter c.
        """
        
        return func(self, a=a, b=b, c=c)


    def __getitem__(self, index):
        if isinstance(index, int):
            return self.field[index]
        row, col = index
        return self.field[row][col]
    
    def __setitem__(self, index, value):
        if isinstance(index, int):
            self.field[index] = value
        else:
            row, col = index
            self.field[row][col] = value
    
    def __str__(self):
        base = f"Field with {self.rows} rows and {self.cols} columns\n" + f"Cell length: {self.cell_length_m} m, Cell width: {self.cell_width_m} m\n" + \
            f"Rx: {self.rx} m, Ry: {self.ry} m\n" + f"rx_cells: {self.rx_cells}, ry_cells: {self.ry_cells}\n"
        for row in self.field:
            base += str(row) + "\n"
        return base

    def randomize_field(self, MAX_V = 0.4123, MIN_V = 0.0):
        """!
        Randomize the field.

        @param MAX_V Maximum water level.
        @param MIN_V Minimum water level.
        """

        field = np.random.uniform(MIN_V, MAX_V, (self.rows, self.cols))
        field[self.line] = [-1 for _ in range(self.cols)]
        self.field = field
    
    
    def avg_field(self, field = None):
        """!
        
        Calculate the average water level in the field

        @param field 2D np.array, optional
        @details Calculates the average water level in the field.

        @return float
        """
        if field is None:
            field = self.field
        valid_cells = field[field != -1]  
        return np.mean(valid_cells)
    
    def update_cell(self, r, c, x, w, v):
        """!
        
        Update the moisture level of a cell in the field

        @param r Row index of the cell.
        @param c Column index of the cell.
        @param x Current position of watering machine.
        @param w Watering intensity.
        @param v Water level.

        @return float
        @details Updates the moisture level of a cell in the field based on the current position of the watering machine, the watering intensity, and the water level.
        
        """
        if self.field[r][c] == -1:
            return 0
        d_rc = ((r - self.line) ** 2 + (c - x) ** 2) ** 0.5
        term = w * (self.Wm * self.Deltat / (d_rc**2 + 1)**self.beta) * np.exp(-self.alpha * v)
        self.field[r][c] += term
        return term

    def parallel_update_field(self, x, w, v):
        """
        @param x Current position of watering machine.
        @param w Watering intensity.
        @param v Water level.
        @return List of changes in the field.
        @details Updates the moisture level of cells in the field based on the current position of the watering machine, the watering intensity, and the water level.
        
        """
        start_col = max(0, x - self.rx_cells)
        end_col = min(self.cols, x + 1)
        if start_col == end_col:
            start_col -= self.rx_cells

        max_workers = multiprocessing.cpu_count()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.update_cell, r, c, x, w, v)
                for r in range(max(0, self.line - self.ry_cells), min(self.rows, self.line + self.ry_cells + 1))
                for c in range(start_col, end_col)
            ]
            results = [future.result() for future in futures]

        return results  # Возвращает список изменений для анализа


