#include "ModelParams.h"
#include <vector>
ModelParams::ModelParams()
{
	InitParametrs();
}

ModelParams::~ModelParams()
{
	for (auto& element : ModelParamsMap)
	{
		element.second.clear();
	}
	ModelParamsMap.clear();
	
}

void ModelParams::LoadModelSectionParams(std::string KeyWord, std::map<std::string, std::any> params)
{
	if (ModelParamsMap.find(KeyWord) == ModelParamsMap.end()) // Если ключа нет в словаре
	{
		throw std::invalid_argument("KeyWord not found in ModelParamsMap."); // Выбрасвыаем исключение неверного аргумента
	}
	else {
		ModelParamsMap[KeyWord] = params;
	}
	
}

void ModelParams::LoadModelParams(std::map<std::string, std::any> paramsM, std::map<std::string, std::any> paramsO, std::map<std::string, std::any> paramsF)
{
	std::vector<std::map<std::string, std::any>> ParamsVec{paramsM, paramsO, paramsF};
	std::vector<std::string> LabelsVec{"M", "O", "F"};
	for (size_t i = 0; i < 3; ++i)
	{
		std::map<std::string, std::any> param = ParamsVec[i];
		auto& label = LabelsVec[i];

		ModelParamsMap[label] = param;
	}
}

void ModelParams::LoadModelFromFile(std::string filename)
{
	Config config;
	ConfigLoader loader;

	if (loader.load(filename, config))
	{
		std::map<std::string, Section> Params = config.sections;
		ModelParams::LoadModelParams(Params["Model"], Params["Optimization"], Params["Field"]);
	}
	else throw std::invalid_argument("Check config file");
}

std::any ModelParams::getParam(std::string KeyWord, std::string ParamName)
{
	auto& element = ModelParams::ModelParamsMap[KeyWord][ParamName];
	if (element.type() == typeid(int)) return std::any_cast<int>(element);
	if (element.type() == typeid(double)) return std::any_cast<double>(element);
	else throw std::invalid_argument("Unsupported type");
}

void ModelParams::InitParametrs()
{	
	
	std::map<std::string, std::any> ModeLParamsMMap
	{
		// all double
		{"a", 2.0}, {"b", 0.3412}, {"c", 3.0}, {"w", 0.0},
		{"Wp", 0.0}, {"v", 0.0}, {"Ms", 10.0},
		{"Mr", 1.0}, {"Wm", 50.0}, {"alpha", 0.25},
		{"beta", 0.01}, {"lambda", 0.5}, {"eta", 0.01},
		{"gamma", 0.3}, {"delta", 0.1}, {"Deltat", 0.05	}
	};

	std::map<std::string, std::any> ModelParamsOMap
	{
		{"l_r", 0.1}, {"eps", 1e-3}, {"max_iter", 500}
	};
	std::map<std::string, std::any> ModelParamsFMap
	{
		// length_m, width_m, rx, ry - doubles
		// other int
		{"length_m", 1000.0}, {"width_m", 100.0}, {"rows", 100}, 
		{"cols", 1000}, {"rx", 0.1}, {"ry", 50.0}, {"line", 50}
	};

	ModelParamsMap["M"] = ModeLParamsMMap;
	ModelParamsMap["O"] = ModelParamsOMap;
	ModelParamsMap["F"] = ModelParamsFMap;

}


std::map<std::string, std::any>  ModelParams::getModelParams(std::string KeyWord)  {
	if (ModelParamsMap.find(KeyWord) == ModelParamsMap.end()) // Если ключа нет в словаре
	{
		throw std::invalid_argument("KeyWord not found in ModelParamsMap."); // Выбрасвыаем исключение неверного аргумента
	}
	else // иначче возвращаем словарь
	{
		return ModelParamsMap[KeyWord]; 
	}	
}
