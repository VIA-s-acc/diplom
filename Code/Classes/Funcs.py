from Field import Field
from math import e


def exp_step(l_0, step, lmbda=0.05):
    return l_0 * e**(-lmbda*step)


def poly_step(l_0, step, alpha=0.5, beta=1):
    return l_0 * (beta * step + 1)**(-alpha)
    

def base(Field, a, b, c):
    res = 0 
    for i in range(Field.rows):
        for j in range(Field.cols):
            if Field.field[i][j] == -1:
                continue
            else:
                
                res += -a*(Field.field[i][j] - b)**2 + c
    return res

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
    Water = 4*eta*rx*ry*w*Wm*Deltat*e**(-delta*v)
    
    exp_alpha_v = e**(-alpha*v)
    if start_col == end_col: 
        start_col -= Field.rx_cells  

    for r in range(max(0, Line - ry_cells), min(Field.rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field.field[r, c] == -1:
                continue
            else:
                d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
                term = Wm*Deltat/(d_rc**2+1)**beta * exp_alpha_v
                Base += -a*(Field.field[r, c] + w*term - b) ** 2 + c_
    
    return Base - Time - Water


def dGkdw(Field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, ry_cells, Line, a, b, alpha, beta, Water = 0):
    start_col = max(0, x_cur) #+1
    end_col = min(Field.cols, x_cur + Field.rx_cells + 1) 
    Base = 0
    Time = 0
    Water = 4*eta*Wm*Deltat*e**(-delta*v) *rx*ry
    
    exp_alpha_v = e**(-alpha*v)
    if start_col == end_col: 
        start_col -= Field.rx_cells  

    for r in range(max(0, Line - ry_cells), min(Field.rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field.field[r, c] == -1:
                continue
            else:
                d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
                term = Wm*Deltat/(d_rc**2+1)**beta * exp_alpha_v
                Base += -2*a*(Field.field[r, c] + w*term - b) * term
    
    return Base - Water, Water

def dGkdv(Field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, ry_cells, Line, a, b, alpha, beta, gamma, lmbda, Water = 0):
    start_col = max(0, x_cur - Field.rx_cells) #+1
    end_col = min(Field.cols, x_cur + 1) 
    if start_col == end_col: 
        start_col -= Field.rx_cells  
    Base = 0
    Time = -gamma * lmbda * t_k * e**(-gamma*v) 
    
    Water = -delta * 4 * eta * rx * ry * w * Wm * Deltat * e**(-delta*v)
    
    exp_alpha_v = e**(-alpha*v)
    for r in range(max(0, Line - ry_cells), min(Field.rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field.field[r, c] == -1:
                continue
            else:
                d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
                Base += -2*a*(Field.field[r, c] + w * ((Wm * Deltat)/(d_rc**2+1)**beta) * exp_alpha_v - b) * (-alpha*Deltat*w*Wm*exp_alpha_v/(d_rc**2+1)**beta)
    return Base - Time - Water, Water
    
import matplotlib.pyplot as plt
import numpy as np
def plot_Gk(Field, x_cur, t_k, eta, Wm, Deltat, delta, rx, ry, ry_cells, Line, a, b, c_, alpha, beta, gamma, lmbda, points = None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ws = np.linspace(0, 1, 100)
    vs = np.linspace(0, 10, 100)
    ws, vs = np.meshgrid(ws, vs)
    Gks = np.zeros(ws.shape)

        
    for i in range(ws.shape[0]):
        for j in range(ws.shape[1]):
            Gks[i, j] = Gk(Field, x_cur, ws[i, j], vs[i, j], t_k, eta, Wm, Deltat, delta, rx, ry, ry_cells, Line, a, b, c_, alpha, beta, gamma, lmbda)
    ax.plot_surface(ws, vs, Gks)
    
    if points is not None:
        for (w,v) in points:
            print(w,v)
            ax.scatter(w, v, Gk(Field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, ry_cells, Line, a, b, c_, alpha, beta, gamma, lmbda), color='red')
    
    ax.set_title('Gk')
    ax.set_xlabel('w')
    ax.set_ylabel('v')
    ax.set_zlabel('Gk')
    plt.show()
        

    
if __name__ == "__main__":
    from ConfigLoader import ConfigLoader
    from Field import Field
    Loader = ConfigLoader('../config.ini')   
    Loader.print_config() 
    a,b,c,wp,v,ms,mr,wm,alpha,beta,lmbda,eta,gamma,delta = Loader.getfloat("Model", "a"), Loader.getfloat("Model", "b"), Loader.getfloat("Model", "c"), Loader.getfloat("Model", "wp"), Loader.getfloat("Model", "v"), Loader.getfloat("Model", "ms"), Loader.getfloat("Model", "mr"), Loader.getfloat("Model", "wm"), Loader.getfloat("Model", "alpha"), Loader.getfloat("Model", "beta"), Loader.getfloat("Model", "lmbda"), Loader.getfloat("Model", "eta"), Loader.getfloat("Model", "gamma"), Loader.getfloat("Model", "delta"), 
    
    length_m, width_m, rows, cols, rx, ry = Loader.getfloat("Field", "length_m"), Loader.getfloat("Field", "width_m"), Loader.getint("Field", "rows"), Loader.getint("Field", "cols"), Loader.getfloat("Field", "rx"), Loader.getfloat("Field", "ry")

    Deltat = Loader.getfloat("Model", "deltat")
    

    field = Field(length_m=length_m, width_m=width_m, rows = rows, cols = cols, rx = rx, ry = ry, alpha = alpha, beta = beta, Wm = wm, Deltat = Deltat)
    
    field.randomize_field(0, 0)
    
    plot_Gk(field, 0, 0, eta, wm, Deltat, delta, rx, ry, field.ry_cells, field.line, a, b, c, alpha, beta, gamma, lmbda)
