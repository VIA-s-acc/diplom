#pragma once
#include "Optimizer.h"
#include "ModelParams.h"

struct Matrix
{
    double data[2][2] = { {1, 0}, {0, 1} };
    
    Matrix() {};
    Matrix(double a, double b, double c, double d) { data[0][0] = a; data[0][1] = b; data[1][0] = c; data[1][1] = d; };
    Matrix(const Matrix& other) {
        data[0][0] = other.data[0][0];
        data[0][1] = other.data[0][1];
        data[1][0] = other.data[1][0];
        data[1][1] = other.data[1][1];
    }
    Matrix(Matrix&& other) noexcept {
        data[0][0] = other.data[0][0];
        data[0][1] = other.data[0][1];
        data[1][0] = other.data[1][0];
        data[1][1] = other.data[1][1];
    }
    double& operator()(int i, int j) { if (i < 2 && j < 2) { return data[i][j]; } else { throw std::out_of_range("Out of range"); } };
    const double& operator()(int i, int j) const { if (i < 2 && j < 2) {return data[i][j]; } else { throw std::out_of_range("Out of range"); } };
};

class NOptimizer :
    public Optimizer
{
    double regularization = 0;
    int max_iter_n = 0;

public:
    NOptimizer(ModelParams params, Field field, bool save = false, bool log = false, int max_iter_n = 0, double regularization = 0) : Optimizer(params, field, save, log), max_iter_n(max_iter_n), regularization(regularization){};
    
    Vector2D N_step(int x_cur, double w, double v, double t_k, double Mr_Deltat);
    void N_Max(int x);
    double FindAlpha(Vector2D grad, int x_cur, double t_k, double w, double v, double a = -1, double b = 1, double tol = 1e-6);
    double f(double alpha, int x_cur, double t_k, double w, double v, Vector2D grad);

};





