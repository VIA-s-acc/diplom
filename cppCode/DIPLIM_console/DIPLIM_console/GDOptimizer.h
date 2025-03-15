#pragma once
#include "Field.h"
#include "ModelParams.h"
#include "Optimizer.h"
#include "time.h"




class GDOptimizer :
    public Optimizer
{
public:
	/*
	* Constructs a GDOptimizer object with the given parameters.
	*
	* @param params Model parameters for the optimizer.
	* @param field Field object associated with the optimizer.
	* @param save Flag to enable saving of optimization results.
	* @param log Flag to enable logging of optimization process.
	*/
	GDOptimizer(ModelParams params, Field field, bool save = false, bool log = false) : Optimizer(params, field, save, log){};
	
	/**
	 * Performs a gradient descent step for the given parameters.
	 *
	 * @param x_cur the current x index
	 * @param w the current w value
	 * @param v the current v value
	 * @param t_k the current time step
	 * @param Mr_Deltat the maximum allowed change in v
	 *
	 * @return a Vector2D containing the new w and v values
	 */
	Vector2D GD_step(int x_cur, double w, double v, double t_k, double Mr_Deltat);
	
	
	/*
		void GD_Max(int x); used to optimize Gk function in Field;

		@param x - index of current cell, in which machine is located;
	*/
	void GD_Max(int x);

};

