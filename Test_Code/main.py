from .Classes.Field import Field
from math import e


def Gk(Field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, ry_cells, Line, a, b, c_, alpha, beta, gamma, lmbda, Water = 0):
    """
    The function Gk calculates a component of the gradient of the goal function.
    
    Parameters
    ----------
    Field : Field
        The field object
    x_cur : int
        The current x-coordinate of the machine
    w : float
        The watering intensity
    v : float
        The machine speed
    t_k : float
        The time step
    eta : float
        The water price coefficient
    Wm : float
        The water supply coefficient
    Deltat : float
        The time step
    delta : float
        The water price intensity coefficient
    rx : float
        The horizontal radius of watering in meters
    ry : float
        The vertical radius of watering in meters
    ry_cells : int
        The number of rows in the vertical radius of watering
    Line : int
        The line number of the machine
    a : float
        The watering intensity coefficient
    b : float
        The desired moisture level
    c_ : float
        The constant term in the goal function
    alpha : float
        The watering range coefficient
    beta : float
        The watering intensity coefficient
    gamma : float
        The time intensity coefficient
    lmbda : float
        The time penalty coefficient
    Water : float, optional
        The water usage at the previous time step
    
    Returns
    -------
    float
        The value of the Gk component of the gradient
    """

    start_col = max(0, x_cur) #+1
    end_col = min(Field.cols, x_cur + Field.rx_cells + 1) 
    Base = 0
    Time = -gamma*t_k*e**(-gamma * v)
    Water += 4*eta*rx*ry*w*Wm*Deltat*e**(-delta*v)
    
    exp_alpha_v = e**(-alpha*v)
    if start_col == end_col: 
        start_col -= Field.rx_cells  

    for r in range(max(0, Line - ry_cells), min(Field.rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field[r, c] == -1:
                continue
            else:
                d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
                term = Wm*Deltat/(d_rc**2+1)**beta * exp_alpha_v
                Base += -a*(Field[r, c] + w*term - b) ** 2 + c_
    
    return Base - Time - Water


def dGkdw(Field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, ry_cells, Line, a, b, alpha, beta, Water = 0):
    start_col = max(0, x_cur) #+1
    end_col = min(Field.cols, x_cur + Field.rx_cells + 1) 
    Base = 0
    Time = 0
    Water += 4*eta*Wm*Deltat*e**(-delta*v) *rx*ry
    
    exp_alpha_v = e**(-alpha*v)
    if start_col == end_col: 
        start_col -= Field.rx_cells  

    for r in range(max(0, Line - ry_cells), min(Field.rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field[r, c] == -1:
                continue
            else:
                d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
                term = Wm*Deltat/(d_rc**2+1)**beta * exp_alpha_v
                Base += -2*a*(Field[r, c] + w*term - b) * term
    
    return Base - Water, Water

def dGkdv(Field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, ry_cells, Line, a, b, alpha, beta, gamma, lmbda, Water = 0):
    start_col = max(0, x_cur - Field.rx_cells) #+1
    end_col = min(Field.cols, x_cur + 1) 
    if start_col == end_col: 
        start_col -= Field.rx_cells  
    Base = 0
    Time = -gamma * lmbda * t_k * e**(-gamma*v) 
    
    Water += -delta * 4 * eta * rx * ry * w * Wm * Deltat * e**(-delta*v)
    
    exp_alpha_v = e**(-alpha*v)
    for r in range(max(0, Line - ry_cells), min(Field.rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field[r, c] == -1:
                continue
            else:
                d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
                Base += -2*a*(Field[r, c] + w * ((Wm * Deltat)/(d_rc**2+1)**beta) * exp_alpha_v - b) * (-alpha*Deltat*w*Wm*exp_alpha_v/(d_rc**2+1)**beta)
    return Base - Time - Water, Water
    