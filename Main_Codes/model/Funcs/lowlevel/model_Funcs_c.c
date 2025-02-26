/*==========================================================
BASE C TEMPLATE
==========================================================*/
#include "model_Funcs_c.h"
#include <math.h>

int basic_function() {
    return 1;
}

double c_exp_step(double l_0, int step, double lmbda)
{
    return l_0 * exp(-lmbda * step);
}

double c_poly_step(double l_0, int step, double alpha, double beta)
{
    return l_0 * pow(beta*step+1, -alpha);
}

double c_base(double* Field, int rows, int cols, double a, double b, double c)
{
    double res = 0;
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            if (Field[i*cols+j] == -1)
            {
                continue;
            }
            else 
            {
                res += -a * pow((Field[i*cols+j] - b), 2) + c;
            }
        }
    }
    return res;
}

double c_Gk(double* field, int rows, int cols, int x_cur, double w, double v, double t_k, double eta, double Wm, double Deltat, double delta, double rx, double ry, int rx_cells, int ry_cells, int line, double a, double b, double c, double alpha, double beta, double gamma, double lmbda)
{
    int start_col = fmax(0, x_cur);
    int end_col = fmin(cols, x_cur + rx_cells + 1);

    double Base = 0;
    double Time = -gamma * t_k * exp(-gamma * v);
    double Water = 4*eta*rx*ry*w*Wm*Deltat*exp(-delta*v);

    double exp_alpha_v = exp(-alpha*v);

    if (start_col == end_col)
    {
        start_col = rx_cells;
    }

    int range_min = fmax(0, line - ry_cells);
    int range_max = fmin(rows, line + ry_cells + 1);

    for (int r = range_min; r < range_max; r++)
    {
        for (int c_ = start_col; c_ < end_col; c_++)
        {
            if (field[r*cols+c_] == -1)
            {
                continue;
            }
            else
            {
                double d_rc = pow(pow(r-line, 2) + pow(c_ - x_cur, 2), 0.5);
                double term = (Wm * Deltat)/pow((pow(d_rc, 2) + 1), beta) * exp_alpha_v;
                Base += -a * pow((field[r*cols+c_] + w*term - b), 2) + c;
            }
        }
    }
    return Base - Time - Water;
}