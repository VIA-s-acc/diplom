from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import numpy as np

class Field:
    def __init__(self, length_m, width_m, rows, cols, rx, ry, alpha, beta, Wm, Deltat, line = None, field=None):
        
        """
        Constructor for Field class

        Parameters
        ----------
        length_m : float
            Length of the field in meters
        width_m : float
            Width of the field in meters
        rows : int
            Number of rows in the field
        cols : int
            Number of columns in the field
        rx : float
            radius of watering in meters
        ry : float
            radius of watering in meters
        alpha : float
            coefficient for watering
        beta : float
            coefficient for watering
        Wm : float
            maximum watering in meters
        Deltat : float
            time step
        line : int, optional
            line index of watering machine
        field : 2D np.array, optional
            preinitialized field

        Returns
        -------
        Field
            A Field object
        """
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

    def __str__(self):
        base = f"Field with {self.rows} rows and {self.cols} columns\n" + f"Cell length: {self.cell_length_m} m, Cell width: {self.cell_width_m} m\n" + \
            f"Rx: {self.rx} m, Ry: {self.ry} m\n" + f"rx_cells: {self.rx_cells}, ry_cells: {self.ry_cells}\n"
        for row in self.field:
            base += str(row) + "\n"
        return base

    def randomize_field(self, MAX_V = 0.4123, MIN_V = 0.0):
        """
        Randomize the field values

        Returns
        -------
        2D array of floats
            The randomized field
        """

        field = np.random.uniform(MIN_V, MAX_V, (self.rows, self.cols))
        field[self.line] = [-1 for _ in range(self.cols)]
        return field
    
    
    def avg_field(self, field = None):
        """
        Calculate the average water level in the field

        Returns
        -------
        float
            The average water level
        """
        if field is None:
            field = self.field
        valid_cells = field[field != -1]  
        return np.mean(valid_cells)
    
    def update_cell(self, r, c, x, w, v):
        """
        Update the cell at the specified row and column

        Parameters
        ----------
        r : int
            Row index
        c : int
            Column index
        x : int
            Current position of watering machine
        w : float
            Watering intensity
        v : float
            Water level

        Returns
        -------
        float
            The updated water level of the cell
        """
        if self.field[r][c] == -1:
            return 0
        d_rc = ((r - self.line) ** 2 + (c - x) ** 2) ** 0.5
        term = w * (self.Wm * self.Deltat / (d_rc**2 + 1)**self.beta) * np.exp(-self.alpha * v)
        self.field[r][c] += term
        return term

    def parallel_update_field(self, x, w, v):
        """
        Update the field in parallel

        Parameters
        ----------
        x : int
            Current position of watering machine
        w : float
            Watering intensity
        v : float
            Water level

        Returns
        -------
        list
            The list of changes of water level of the cells
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


