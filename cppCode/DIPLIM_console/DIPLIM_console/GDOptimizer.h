#pragma once
#include "Field.h"
#include "ModelParams.h"
#include "Optimizer.h"
#include "time.h"




class GDOptimizer :
    public Optimizer
{
public:
	GDOptimizer(ModelParams params, Field field, bool save = false, bool log = false) : Optimizer(params, field, save, log){};
	Vector2D GD_step(int x_cur, double w, double v, double t_k);
	/*
		void GD_Max(int x); used to optimize Gk function in Field;

		@param x - index of current cell, in which machine is located;
	*/
	void GD_Max(int x);

};

