/*==========================================================
BASE HEADER TEMPLATE
==========================================================*/
#ifndef FUNCS_H
#define FUNCS_H

/*
\file
\brief header file for basic functions (G_k, G_K_dw, etc.)
\author Georgii
\version 1.0a

*/

int basic_function();

/*!
Exponential step function 
\param[in] l_0 initial value
\param[in] step number of step
\param[in] lmbda decay constant
\return value of exponential step function
*/
double c_exp_step(double l_0, int step, double lmbda);


/*!
Polynomial step function 
\param[in] l_0 initial value
\param[in] step number of step
\param[in] alpha decay constant
\param[in] beta decay constant
\return value of polynomial step function
*/
double c_poly_step(double l_0, int step, double alpha, double beta);

/*!
Base function
\param[in] Field array of values
\param[in] rows number of rows
\param[in] cols number of columns
\param[in] a parameter
\param[in] b parameter
\param[in] c parameter
\return value of base function
*/
double c_base(double* Field, int rows, int cols, double a, double b, double c);


/*!
G_k function
\param[in] Field array of values
\param[in] x_cur current position
\param[in] w parameter
\param[in] v parameter
\param[in] t_k parameter
\param[in] eta parameter
\param[in] Wm parameter
\param[in] Deltat parameter
\param[in] delta parameter
\param[in] rx parameter
\param[in] ry parameter
\param[in] rx_cells parameter
\param[in] ry_cells parameter
\param[in] line parameter
\param[in] a parameter
\param[in] b parameter
\param[in] c parameter
\param[in] alpha parameter
\param[in] beta parameter
\param[in] gamma parameter
\param[in] lmbda parameter
\return value of G_k function
*/
double c_Gk(double* field, int rows, int cols, int x_cur, double w, double v, double t_k, double eta, double Wm, double Deltat, double delta, double rx, double ry, int rx_cells, int ry_cells, int line, double a, double b, double c, double alpha, double beta, double gamma, double lmbda);



#endif // FUNCS_H
