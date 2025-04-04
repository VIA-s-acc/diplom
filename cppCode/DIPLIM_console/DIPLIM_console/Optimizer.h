#pragma once
#include "ModelParams.h"
#include "Func.h"
#include <chrono>

struct Vector5D
{
	double w;
	double v;
	double w1;
	double w2;
	double G;
};

struct Vector6D
{
	double t_k;
	double w;
	double v;
	int	   x;
	double x_m;
	double G;
	std::vector<std::vector<double>> FieldMap2D;
};

struct Vector2D {
	double w;
	double v;

	double norm() const { return sqrt(w * w + v * v); };
};


class Optimizer
{

	void initializeInfo();
	bool saveF = false;
	bool logF = false;
	std::map<std::string, std::any> Mparams;
	std::map<std::string, std::any> Oparams;
	std::map<std::string, std::any> Fparams;
	

public:
	Func func;
	Field field;
	std::map<std::string, std::any> info;

	Optimizer(ModelParams Params, Field field_, bool saveF = false, bool logF = false) : field(field_), Mparams(Params.getModelParams("M")), Oparams(Params.getModelParams("O")), Fparams(Params.getModelParams("F")), func(Params, field_), saveF(saveF), logF(logF) {
		initializeInfo();
	};
	~Optimizer() {};

	bool savef() const { return saveF; };
	bool logf()  const { return logF;  };
	std::map<std::string, std::any> getMparams() { return Mparams; };
	std::map<std::string, std::any> getOparams() { return Oparams; };
	std::map<std::string, std::any> getFparams() { return Fparams; };
};

