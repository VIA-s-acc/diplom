// DIPLIM_console.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
#define _CRT_SECURE_NO_DEPRECATE

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

void print_help(const char* program_name) {
	std::cout << "Usage: " << program_name << " <config_file_path> [-f <config_file_path>] [-Oi <n>] [-h]" << std::endl;
	std::cout << std::endl;
	std::cout << "Options:" << std::endl;
	std::cout << "  -h, --help          Show this help message and exit." << std::endl;
	std::cout << "  -f, --file <path>   Load the model from a specified configuration file." << std::endl;
	std::cout << "  -Oi, --optimization-iterations <n>  Run optimization for n iterations (default is 1)." << std::endl;
	std::cout << "  -sf, --save-flag <1/0>   Enable or disable save flag (1 = true, 0 = false)." << std::endl;
	std::cout << "  -lf, --log-flag <1/0>    Enable or disable log flag (1 = true, 0 = false)." << std::endl;
	std::cout << std::endl;
	std::cout << "Examples:" << std::endl;
	std::cout << "  " << program_name << " config.ini              Load the model from config.json and run optimization." << std::endl;
	std::cout << "  " << program_name << " -f config.ini -Oi 10    Load the model from config.json and run optimization for 10 iterations." << std::endl;
	std::cout << "  " << program_name << " -sf 1 -lf 1               Enable save flag and log flag." << std::endl;
	std::cout << "  " << program_name << " -h                       Show help message." << std::endl;
}

struct Argument
{
	std::string name;
	std::string value;
};

int main(int argc, char* argv[])
{

	if (argc == 2 && (std::string(argv[1]) == "-h" || std::string(argv[1]) == "--help")) {
		print_help(argv[0]);
		return 0;
	}

	ModelParams Params;
	std::map <std::string, std::string> ParamLabels{
				{"M", "[Model]"}, {"O", "[Optimizer]"}, {"F", "[Field]"}
	};
	if (argc < 2) {
		std::cout << "Usage: " << argv[0] << " <config_file_path>" << std::endl;
		std::cout << "Config file not specified." << std::endl;
		std::cout << "Will used default config" << std::endl;
		std::map<std::string, std::map<std::string, std::any>> ParamsMap = Params.getParms();
		debug_print(ParamsMap, argv, ParamLabels);
	}

	int RunOptimizationITimes = 1;
	bool save_flag = false;
	bool log_flag  = false;

	if (argc >= 2) {

		std::vector<Argument> arguments;
		for (int i = 1; i < argc-1; i++) {
			{ arguments.push_back(Argument{ argv[i], argv[i + 1] }); };
		}
		bool Fflag = false;
		for (Argument args : arguments) {

			if (args.name == "-f" or args.name == "--file") {
				std::string file_path = args.value;
				Params.LoadModelFromFile(file_path);
				std::map<std::string, std::map<std::string, std::any>> ParamsMap = Params.getParms();
				debug_print(ParamsMap, argv, ParamLabels);
				Fflag = true;
			}
			if (args.name == "-Oi" or args.name == "--optimization-iterations")
			{
				try {
					RunOptimizationITimes = std::stoi(args.value);
				}
				catch (const std::exception& e) {
					throw std::runtime_error("RunOptimizationITimes is not integer.");
				}
			}
			if (args.name == "-sf" or args.name == "--save-flag")
			{
				try {
					save_flag = (std::stoi(args.value) == 1) ? true : false;
				}
				
				catch (const std::exception& e) {
					throw std::runtime_error("RunOptimizationITimes is not integer.");
				}
			}

			if (args.name == "-lf" or args.name == "--log-flag")
			{
				try {
					log_flag = (std::stoi(args.value) == 1) ? true : false;
				}

				catch (const std::exception& e) {
					throw std::runtime_error("RunOptimizationITimes is not integer.");
				}
			}

		}

		if (!Fflag) {
			throw std::runtime_error("Config file not specified.");
		};

	}
	Field field(Params);

	field.randomizeField(0.0, 0.0);
	std::cout << save_flag << " " << log_flag << std::endl;
	GDOptimizer GD(Params, field, save_flag, log_flag);
	for (int i = 1; i < RunOptimizationITimes+1; i++) {
		std::cout<< "\t\t\t--------- iteration " << i << " ---------\t\t\t" << std::endl;
		GD.GD_Max(0);
		std::cout << "\t\t\t--------- iteration " << i << " ---------\t\t\t" << std::endl << std::endl << std::endl;
	}
	//GD.GD_Max(0);
	//GD.GD_Max(0);
	//GD.GD_Max(0);
	//GD.GD_Max(0);


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
