#pragma once
#include "ModelParams.h"
#include "Func.h"
#include <chrono>

struct Vector4D
{
	double w;
	double v;
	double w1;
	double w2;
};

struct Vector5D
{
	double w;
	double v;
	int	   x;
	double x_m;
	std::vector<std::vector<double>> FieldMap2D;
};

struct Vector2D {
	double w;
	double v;
};


class Optimizer
{


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
		info["O"] = getOparams();
		info["F"] = getFparams();
		info["M"] = getMparams();
		double avg = field.avgerageField();
		if (!saveF) info["Details"] = NULL;
		info["Time"] = std::map<std::string, std::chrono::time_point<std::chrono::system_clock> >{
			{"Start", std::chrono::system_clock::now()},
			{"End", std::chrono::system_clock::now()},
			{"Total", std::chrono::system_clock::now()}
		};
		info["Base"] = std::map<std::string, double>{
			{"Start", this->field.calc_base()},
			{"End", 0},
			{"Diff", 0}
		};
		info["AVG"] = std::map<std::string, double>{
			{"Start", avg},
			{"End", 0},
			{"Diff", 0}
		};
		double max = field.maxField();
		info["MAX"] = std::map<std::string, double>{
			{"Start", max},
			{"End", 0},
			{"Diff", 0}
		};
		double min = field.minField();
		info["MIN"] = std::map<std::string, double>{
			{"Start", min},
			{"End", 0},
			{"Diff", 0}
		};
		info["Optimization"] = std::map<double, std::vector<Vector4D>>{};
		info["Optimization_Detailed"] = std::map<double, std::vector<Vector5D>>{};

		
	};
	~Optimizer() {};

	bool savef() const { return saveF; };
	bool logf()  const { return logF;  };
	std::map<std::string, std::any> getMparams() { return Mparams; };
	std::map<std::string, std::any> getOparams() { return Oparams; };
	std::map<std::string, std::any> getFparams() { return Fparams; };
};

