#pragma once
#include "ModelParams.h"
#include "Field.h"

struct Res
{
	double res;
	double water;
};

class Func 
{
	Field F;
	ModelParams MP;
	std::map<std::string, std::any> ParamsM;
	std::map<std::string, std::any> ParamsF;
	std::map<std::string, std::any> ParamsO;
	

public:
	int rows, cols, rx_cells, ry_cells, line;
	double eta, Wm, Deltat, rx, ry, a, b, c, alpha, beta, gamma, lambda, delta;

	void setField(Field F_) { F = F_; };
	void setFieldEl(int i, int j, double val) { F(i,j) = val; };

	double getFieldEl(int i, int j) { return Func::F(i, j); };

	Func(ModelParams MP_, Field F_) :
		MP(MP_), F(F_),
		ParamsM(MP.getModelParams("M")), ParamsF(MP.getModelParams("F")), ParamsO(MP.getModelParams("O")),
		rows(std::any_cast<int>(MP.getParam("F", "rows"))),
		cols(std::any_cast<int>(MP.getParam("F", "cols"))),
		rx_cells(std::any_cast<double>(F.getFieldMap().at("rx_cells"))),
		ry_cells(std::any_cast<double>(F.getFieldMap().at("ry_cells"))),
		line(std::any_cast<int>(F.getFieldMap().at("line"))),
		eta(std::any_cast<double>(MP.getParam("M", "eta"))),
		Wm(std::any_cast<double>(MP.getParam("M", "Wm"))),
		rx(std::any_cast<double>(MP.getParam("F", "rx"))),
		ry(std::any_cast<double>(MP.getParam("F", "ry"))),
		a(std::any_cast<double>(MP.getParam("M", "a"))),
		b(std::any_cast<double>(MP.getParam("M", "b"))),
		c(std::any_cast<double>(MP.getParam("M", "c"))),
		alpha(std::any_cast<double>(MP.getParam("M", "alpha"))),
		beta(std::any_cast<double>(MP.getParam("M", "beta"))),
		gamma(std::any_cast<double>(MP.getParam("M", "gamma"))),
		lambda(std::any_cast<double>(MP.getParam("M", "lambda"))),
		delta(std::any_cast<double>(MP.getParam("M", "delta"))),
		Deltat(std::any_cast<double>(MP.getParam("M", "Deltat")))
	{
	};
	

	Res DGkDw(int x_cur, double w, double v, double t_k);
	Res DGkDv(int x_cur, double w, double v, double t_k);
	double poly_step(double l_0, int step, double alpha = 0.5, double beta = 1) { return l_0 * pow((beta * step + 1), -alpha); };
	double exp_step(double l_0, int step, double lambda = 0.05) { return l_0 * exp(-lambda * step); };;
	

};

