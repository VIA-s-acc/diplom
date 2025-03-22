#pragma once
#include "Optimizer.h"

class CGDOptimizer :
    public Optimizer
{
public:
    CGDOptimizer(ModelParams params, Field field, bool save = false, bool log = false) : Optimizer(params, field, save, log) {};

    Vector2D CGD_step(int x_cur, double w, double v, double t_k, double Mr_Deltat);
	void CGD_Max(int x);
    double FindAlpha(Vector2D grad, int x_cur, double t_k, double w, double v, double a = -1, double b = 1, double tol = 1e-6);
    double f(double alpha, int x_cur, double t_k, double w, double v, Vector2D grad);

};

