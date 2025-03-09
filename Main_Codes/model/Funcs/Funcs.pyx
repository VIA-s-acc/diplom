#==========================================================
# BASE PYX TEMPLATE
#==========================================================

from libc.stdlib cimport malloc, free
from libc.string cimport memcpy

cdef extern from "lowlevel/model_Funcs_c.h" nogil:
    int basic_function()
    double c_exp_step(double l_0, int step, double lmbda)
    double c_poly_step(double l_0, int step, double alpha, double beta)

    double c_base(double* Field, int rows, int cols, double a, double b, double c)
    # GK
    double c_Gk(double* field, int rows, int cols, int x_cur, double w, double v, double t_k, double eta, double Wm, double Deltat, double delta, double rx, double ry, int rx_cells, int ry_cells, int line, double a, double b, double c, double alpha, double beta, double gamma, double lmbda)
    # DGkDw
    double c_dGkdw(double* field, int rows, int cols, int x_cur, double w, double v, double t_k, double eta, double Wm, double Deltat, double delta, double rx, double ry, int rx_cells, int ry_cells, int line, double a, double b, double c, double alpha, double beta, double gamma, double lmbda)
    # DGkDv
    double c_dGkdv(double* field, int rows, int cols, int x_cur, double w, double v, double t_k, double eta, double Wm, double Deltat, double delta, double rx, double ry, int rx_cells, int ry_cells, int line, double a, double b, double c, double alpha, double beta, double gamma, double lmbda)

def call_basic_function():
    return basic_function()

def exp_step(l_0, step, lmbda = 0.05):
    return c_exp_step(l_0, step, lmbda)

def poly_step(l_0, step, alpha=0.5, beta=1):
    return c_poly_step(l_0, step, alpha, beta)

def base(field, a, b, c):
    cdef int c_rows = int(len(field))
    cdef int c_cols = int(len(field[0]))

    cdef double c_a = a
    cdef double c_b = b
    cdef double c_c = c

    cdef int c_size = c_rows * c_cols 
    cdef double* c_field = <double*>malloc(c_size * sizeof(double))

    if c_field == NULL:
        raise MemoryError("model.Funcs.base.c_field::alloc_error\nFailed to allocate memory")
    
    cdef double[:] row_buffer

    cdef int i
    for i in range(c_rows):
        row_buffer = field[i]  # CBUFF
        memcpy(&c_field[i * c_cols], &row_buffer[0], c_cols * sizeof(double))

    cdef double result = 0

    with nogil:
        result = c_base(c_field, c_rows, c_cols, c_a, c_b, c_c)

    free(c_field)

    return result


def Gk(field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, rx_cells, ry_cells, line, a, b, c, alpha, beta, gamma, lmbda):
    cdef int c_rows = int(len(field))
    cdef int c_cols = int(len(field[0]))

    cdef int c_size = c_rows * c_cols 
    cdef double* c_field = <double*>malloc(c_size * sizeof(double))

    if c_field == NULL:
        raise MemoryError("model.Funcs.base.c_field::alloc_error\nFailed to allocate memory")
    
    cdef double[:] row_buffer

    cdef int i
    for i in range(c_rows):
        row_buffer = field[i]  # CBUFF
        memcpy(&c_field[i * c_cols], &row_buffer[0], c_cols * sizeof(double))

    cdef double result = 0

    cdef int c_x_cur = x_cur
    cdef double c_w = w
    cdef double c_v = v
    cdef double c_t_k = t_k
    cdef double c_eta = eta
    cdef double c_Wm = Wm
    cdef double c_Deltat = Deltat
    cdef double c_delta = delta
    cdef double c_rx = rx
    cdef double c_ry = ry
    cdef int c_rx_cells = rx_cells
    cdef int c_ry_cells = ry_cells
    cdef int c_line = line
    cdef double c_a = a
    cdef double c_b = b
    cdef double c_c = c
    cdef double c_alpha = alpha
    cdef double c_beta = beta
    cdef double c_gamma = gamma
    cdef double c_lmbda = lmbda

    with nogil:
        result = c_Gk(c_field, c_rows, c_cols, c_x_cur, c_w, c_v, c_t_k, c_eta, c_Wm, c_Deltat, c_delta, c_rx, c_ry, c_rx_cells, c_ry_cells, c_line, c_a, c_b, c_c, c_alpha, c_beta, c_gamma, c_lmbda)

    free(c_field)

    return result

def dGkdw(field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, rx_cells, ry_cells, line, a, b, c, alpha, beta, gamma, lmbda):
    cdef int c_rows = int(len(field))
    cdef int c_cols = int(len(field[0]))

    cdef int c_size = c_rows * c_cols 
    cdef double* c_field = <double*>malloc(c_size * sizeof(double))

    if c_field == NULL:
        raise MemoryError("model.Funcs.base.c_field::alloc_error\nFailed to allocate memory")
    
    cdef double[:] row_buffer

    cdef int i
    for i in range(c_rows):
        row_buffer = field[i]  # CBUFF
        memcpy(&c_field[i * c_cols], &row_buffer[0], c_cols * sizeof(double))

    cdef double result = 0

    cdef int c_x_cur = x_cur
    cdef double c_w = w
    cdef double c_v = v
    cdef double c_t_k = t_k
    cdef double c_eta = eta
    cdef double c_Wm = Wm
    cdef double c_Deltat = Deltat
    cdef double c_delta = delta
    cdef double c_rx = rx
    cdef double c_ry = ry
    cdef int c_rx_cells = rx_cells
    cdef int c_ry_cells = ry_cells
    cdef int c_line = line
    cdef double c_a = a
    cdef double c_b = b
    cdef double c_c = c
    cdef double c_alpha = alpha
    cdef double c_beta = beta
    cdef double c_gamma = gamma
    cdef double c_lmbda = lmbda

    with nogil:
        result = c_dGkdw(c_field, c_rows, c_cols, c_x_cur, c_w, c_v, c_t_k, c_eta, c_Wm, c_Deltat, c_delta, c_rx, c_ry, c_rx_cells, c_ry_cells, c_line, c_a, c_b, c_c, c_alpha, c_beta, c_gamma, c_lmbda)

    free(c_field)

    return result


def dGkdv(field, x_cur, w, v, t_k, eta, Wm, Deltat, delta, rx, ry, rx_cells, ry_cells, line, a, b, c, alpha, beta, gamma, lmbda):
    cdef int c_rows = int(len(field))
    cdef int c_cols = int(len(field[0]))

    cdef int c_size = c_rows * c_cols 
    cdef double* c_field = <double*>malloc(c_size * sizeof(double))

    if c_field == NULL:
        raise MemoryError("model.Funcs.base.c_field::alloc_error\nFailed to allocate memory")
    
    cdef double[:] row_buffer

    cdef int i
    for i in range(c_rows):
        row_buffer = field[i]  # CBUFF
        memcpy(&c_field[i * c_cols], &row_buffer[0], c_cols * sizeof(double))

    cdef double result = 0

    cdef int c_x_cur = x_cur
    cdef double c_w = w
    cdef double c_v = v
    cdef double c_t_k = t_k
    cdef double c_eta = eta
    cdef double c_Wm = Wm
    cdef double c_Deltat = Deltat
    cdef double c_delta = delta
    cdef double c_rx = rx
    cdef double c_ry = ry
    cdef int c_rx_cells = rx_cells
    cdef int c_ry_cells = ry_cells
    cdef int c_line = line
    cdef double c_a = a
    cdef double c_b = b
    cdef double c_c = c
    cdef double c_alpha = alpha
    cdef double c_beta = beta
    cdef double c_gamma = gamma
    cdef double c_lmbda = lmbda

    with nogil:
        result = c_dGkdv(c_field, c_rows, c_cols, c_x_cur, c_w, c_v, c_t_k, c_eta, c_Wm, c_Deltat, c_delta, c_rx, c_ry, c_rx_cells, c_ry_cells, c_line, c_a, c_b, c_c, c_alpha, c_beta, c_gamma, c_lmbda)

    free(c_field)

    return result