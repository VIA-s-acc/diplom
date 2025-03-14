#include "ModelParams.h"

ModelParams::ModelParams()
{
	InitParametrs();
}

ModelParams::~ModelParams()
{
	for (auto it = ModelParams::ModelParamsMap.begin(); it != ModelParams::ModelParamsMap.end(); it++)
	{
		it = ModelParams::ModelParamsMap.erase(it);
	}
	ModelParams::ModelParamsMap.clear();
}

void ModelParams::setModelParams(std::string KeyWord, std::map<std::string, std::any> params)
{
	if (ModelParams::ModelParamsMap.find(KeyWord) == ModelParams::ModelParamsMap.end()) // Если ключа нет в словаре
	{
		throw std::invalid_argument("KeyWord not found in ModelParamsMap."); // Выбрасвыаем исключение неверного аргумента
	}
	else {
		ModelParams::ModelParamsMap[KeyWord] = params;
	}
	
}

void ModelParams::InitParametrs()
{
	std::map<std::string, std::any> ModeLParamsMMap
	{
		{"a", 2}, {"b", 0.3}, {"c", 3},
		{"Wp", 0}, {"v", 0}, {"Ms", 10},
		{"Mr", 0.1}, {"Wm", 10}, {"alpha", 0.25},
		{"beta", 0.01}, {"lmbda", 0.5}, {"eta", 0.01},
		{"gamma", 0.3}, {"delta", 0.1}, {"Deltat", 0.1}
	};

	std::map<std::string, std::any> ModelParamsOMap
	{
		{"l_r", 1e-1}, {"eps", 1e-3}, {"max_iter", 1000}
	};
	std::map<std::string, std::any> ModelParamsFMap
	{
		{"l_m", 1000}, {"w_m", 100}, {"rows", 400}, 
		{"cols", 1000}, {"rx", 0.1}, {"ry", 0.1}
	};

	ModelParams::ModelParamsMap["M"] = ModeLParamsMMap;
	ModelParams::ModelParamsMap["O"] = ModelParamsOMap;
	ModelParams::ModelParamsMap["F"] = ModelParamsFMap;

}


std::map<std::string, std::any> ModelParams::getModelParams(std::string KeyWord) 
{
	if (ModelParams::ModelParamsMap.find(KeyWord) == ModelParams::ModelParamsMap.end()) // Если ключа нет в словаре
	{
		throw std::invalid_argument("KeyWord not found in ModelParamsMap."); // Выбрасвыаем исключение неверного аргумента
	}
	else // иначче возвращаем словарь
	{
		return ModelParams::ModelParamsMap[KeyWord]; 
	}	
}
