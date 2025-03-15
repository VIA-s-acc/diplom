// DIPLIM_console.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
#include <iostream>
#include "Field.h"
#include "ModelParams.h"
#include "ConfigLoader.h"
#include "Optimizer.h">
#include "GDOptimizer.h"

constexpr bool DEBUG = true;

void debug_print(std::map<std::string, std::map<std::string, std::any>> ParamsMap, char* argv[], std::map <std::string, std::string> ParamLabels)
{
if (DEBUG) {
	for (const auto& Params : ParamsMap) {
		bool kf = false;
		for (const auto& [key, value] : Params.second)
		{
			if (!kf) {
				std::cout << ParamLabels[Params.first] << std::endl;
				kf = true;
			}
			if (value.type() == typeid(int))	std::cout << key << ": " << std::any_cast<int>(value) << std::endl;
			else if (value.type() == typeid(double))	std::cout << key << ": " << std::any_cast<double>(value) << std::endl;
		}
		std::cout << std::endl;
	}
}
}


int main(int argc, char* argv[])
{


	ModelParams Params;
	std::map <std::string, std::string> ParamLabels{
				{"M", "[Model]"}, {"O", "[Optimizer]"}, {"F", "[Field]"}
	};
	if (argc != 2) {
		std::cout << "Usage: " << argv[0] << " <config_file_path>" << std::endl;
		std::cout << "Config file not specified." << std::endl;
		std::cout << "Will used default config" << std::endl;
		std::map<std::string, std::map<std::string, std::any>> ParamsMap = Params.getParms();
		debug_print(ParamsMap, argv, ParamLabels);
	}

	if (argc == 2) {
		
		std::string file_path = argv[1];
		Params.LoadModelFromFile(file_path);
		std::map<std::string, std::map<std::string, std::any>> ParamsMap = Params.getParms();
		debug_print(ParamsMap, argv, ParamLabels);
	}
  
	Field field(Params);

	field.randomizeField(0.0, 0.0);

	GDOptimizer GD(Params, field, false, true);
	GD.GD_Max(0);
	GD.GD_Max(0);
	GD.GD_Max(0);
	GD.GD_Max(0);
	GD.GD_Max(0);


	return 0;
    //std::cout << "Config file path: " << file_path << std::endl;
    
}


// Запуск программы: CTRL+F5 или меню "Отладка" > "Запуск без отладки"
// Отладка программы: F5 или меню "Отладка" > "Запустить отладку"

// Советы по началу работы 
//   1. В окне обозревателя решений можно добавлять файлы и управлять ими.
//   2. В окне Team Explorer можно подключиться к системе управления версиями.
//   3. В окне "Выходные данные" можно просматривать выходные данные сборки и другие сообщения.
//   4. В окне "Список ошибок" можно просматривать ошибки.
//   5. Последовательно выберите пункты меню "Проект" > "Добавить новый элемент", чтобы создать файлы кода, или "Проект" > "Добавить существующий элемент", чтобы добавить в проект существующие файлы кода.
//   6. Чтобы снова открыть этот проект позже, выберите пункты меню "Файл" > "Открыть" > "Проект" и выберите SLN-файл.
