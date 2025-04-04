// DIPLIM_console.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//
#define _CRT_SECURE_NO_DEPRECATE

#include "Field.h"
#include "ModelParams.h"
#include "ConfigLoader.h"
#include "Optimizer.h">
#include "GDOptimizer.h"
#include "CGDOptimizer.h"
#include "NOptimizerDFP.h"
#include "random"
#include <iostream>


constexpr bool DEBUG = true;


struct Argument
{
	std::string name;
	std::string value;
};
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
	std::cout << "Usage: " << program_name << " [-f <config_file_path>] [-Oi <n>] [-h] [-m <1/2>] [-sf <1/0>] [-lf <1/0>]" << std::endl;
	std::cout << std::endl;
	std::cout << "Options:" << std::endl;
	std::cout << "  -h, --help          Show this help message and exit." << std::endl;
	std::cout << "  -f, --file <path>   Load the model from a specified configuration file." << std::endl;
	std::cout << "  -Oi, --optimization-iterations <n>  Run optimization for n iterations (default is 1)." << std::endl;
	std::cout << "  -sf, --save-flag <1/0>   Enable or disable save flag (1 = true, 0 = false)." << std::endl;
	std::cout << "  -lf, --log-flag <1/0>    Enable or disable log flag (1 = true, 0 = false)." << std::endl;
	std::cout << "  -m,  --method   <1/2/3>    Optimization method (1 = CGD, 2 = GD, 3 = NDFP)." << std::endl;
	std::cout << "  -r,  --regularization   <f>   Use Regularization with lambda = f" << std::endl;
	std::cout << "  -d   --diagnostic  <1/0> Find optimal parametrs for selected method (1 = true, 0 = false), need -m param." << std::endl;
	std::cout << std::endl;
	std::cout << "Examples:" << std::endl;
	std::cout << "  " << program_name << " config.ini              Load the model from config.json and run optimization." << std::endl;
	std::cout << "  " << program_name << " -f config.ini -Oi 10    Load the model from config.json and run optimization for 10 iterations." << std::endl;
	std::cout << "  " << program_name << " -sf 1 -lf 1               Enable save flag and log flag." << std::endl;
	std::cout << "  " << program_name << " -h                       Show help message." << std::endl;
}



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
	bool RunDiagnostic = false;
	int RunOptimizationMethod = 2;
	double RunNewtonRegularizationParam = 0;
	int RunNewtonMaxIterParam = 0;
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

		
			if (args.name == "-m" or args.name == "--method")
			{
				try {
					RunOptimizationMethod = std::stoi(args.value);
				}
				catch ( const std::exception& e) {
					throw std::runtime_error("RunOptimizationMethod is not integer. (1 = CGD, 2 = GD)");
				}
			}
			if (args.name == "-r" or args.name == "--regularization")
			{
				try {
					RunNewtonRegularizationParam = std::stod(args.value);
				}
				catch (const std::exception& e) {
					throw std::runtime_error("RunNewtonRegularizationParam is not double.");
				}
			}
			if (args.name == "-d" or args.name == "--diagnostic")
			{
				RunNewtonMaxIterParam = std::any_cast<int>(Params.getParam("O", "max_iter"));
				RunDiagnostic = true;
			}
		}


		if (RunDiagnostic)
		{
			switch (RunOptimizationMethod)
			{
			case 3: {
					int step = 1;
					int RunDiagMaxIterNum = 25;
					std::vector<std::vector<double>> diag_vector;
					bool diagnostic_flag = true;
					double end_avg = 0;
					double end_min = 0;
					double max = 0;
					int index = 0;
					double end_max = 0;
					double end_max_new = 0;
					double end_min_new = 0;
					double end_avg_new = 0;
					int prev = RunNewtonMaxIterParam;
					double optimal_ = std::any_cast<double>(Params.getParam("M", "b"));
					Field Dfield(Params);
					Dfield.randomizeField(0, 0.14);
					std::vector<std::vector<double>> fieldMap2D = Dfield.getFieldMap2D();
					
					std::cout << "RunNewtonMaxIterParam set to " << RunNewtonMaxIterParam << "\tFrom Config File" << std::endl;
					while (diagnostic_flag)
					{
						std::cout << "\n\n\n-----Diagnostic Step: " << step << "-----" << std::endl;
						std::cout << "RunNewtonRegularizationParam: " << RunNewtonRegularizationParam << std::endl;
						std::cout << "RunNewtonMaxIterParam: " << RunNewtonMaxIterParam << std::endl;

						Dfield.setField2D(fieldMap2D);

						NOptimizerDFP DiagnosticN(Params, Dfield, save_flag, log_flag, RunNewtonMaxIterParam, RunNewtonRegularizationParam);

						try
						{

							DiagnosticN.N_Max(0);
							end_avg_new = DiagnosticN.field.avgerageField();
							end_min_new = DiagnosticN.field.minField();
							end_max_new = DiagnosticN.field.maxField();
							auto& base_info = std::any_cast<std::map<std::string, double>&>(DiagnosticN.info["Base"]);
							double base = base_info["End"];
							prev = RunNewtonMaxIterParam;
							if (end_max_new > optimal_ * 1.75 && RunNewtonRegularizationParam < 1e-5)
							{
								RunNewtonRegularizationParam += 1e-8;

							}

							if (abs(end_avg_new - end_avg) < 0.00000001 && abs(end_min_new - end_min) < 0.00000001 && abs(end_max_new - end_max) < 0.00000001)
							{
								RunNewtonMaxIterParam--;
								diagnostic_flag = false;
								break;
							}

							if (end_max_new > end_max && step > 1)
							{
								RunNewtonMaxIterParam--;
							}
							else
							{
								RunNewtonMaxIterParam++;
							}

							if (prev != RunNewtonMaxIterParam)
							{
								if (prev == RunNewtonMaxIterParam + 1 && end_max_new < optimal_ * 1.75 && step > 1 && RunNewtonRegularizationParam < 1e-5)
								{
									std::vector<double> temp = { base, static_cast<double>(RunNewtonMaxIterParam), RunNewtonRegularizationParam };
									diag_vector.push_back(temp);
									diagnostic_flag = false;
									for (int i = 0; i < diag_vector.size(); i++)
									{
										if (diag_vector[i][0] > max)
										{
											max = diag_vector[i][0];
											index = i;
										}
									}
									diagnostic_flag = false;
									break;
								}
							}

							end_avg = end_avg_new;
							end_min = end_min_new;
							end_max = end_max_new;
							
			

							std::vector<double> temp = { base, static_cast<double>(RunNewtonMaxIterParam), RunNewtonRegularizationParam };
							diag_vector.push_back(temp);
							if (step > RunDiagMaxIterNum - 2)
							{
								for (int i = 0; i < diag_vector.size(); i++)
								{
									if (diag_vector[i][0] > max)
									{
										max = diag_vector[i][0];
										index = i;
									}
								}
								diagnostic_flag = false;
								break;
							}
							
							
							
							step++;
						}

						catch (const NewtonException& e) {
							std::cout << e.what() << std::endl;
							step++;
							int IterNum = e.getValue();
							if (RunNewtonMaxIterParam > IterNum && IterNum != 0)
							{
								RunNewtonMaxIterParam = IterNum - 1;
							}
							else {
								RunNewtonMaxIterParam--;
							}
						}
					}
					RunNewtonRegularizationParam = diag_vector[index][2];
					RunNewtonMaxIterParam = static_cast<int>(diag_vector[index][1]) - 1;
					Dfield.setField2D(fieldMap2D);
					std::cout << "\n\n\n\t\t\t -----Diagnostic completed. Steps: " << step << "-----" << std::endl;
					std::cout << "RunNewtonRegularizationParam: " << RunNewtonRegularizationParam << std::endl;
					std::cout << "RunNewtonMaxIterParam: " << RunNewtonMaxIterParam << std::endl;
					std::cout << "\t\t\t-----Diagnostic completed. Steps: " << step << "-----" << std::endl;
					NOptimizerDFP DiagnosticN(Params, Dfield, save_flag, log_flag, RunNewtonMaxIterParam, RunNewtonRegularizationParam);
					DiagnosticN.N_Max(0);
					
					return 0;
				}
			default:
				std::cerr<<"Diagnostic not available for selected method. Closing..."<<std::endl;
				return 0;
			}
		}
	}
	Field field(Params);
	field.randomizeField(0.0, 0.14);
	CGDOptimizer CGD(Params, field, save_flag, log_flag);
	GDOptimizer GD(Params, field, save_flag, log_flag);
	NOptimizerDFP NO(Params, field, save_flag, log_flag, RunNewtonMaxIterParam, RunNewtonRegularizationParam);
	for (int i = 1; i < RunOptimizationITimes+1; i++) {
		switch (RunOptimizationMethod)
		{
		case 1:
			CGD.CGD_Max(0);
			break;
		case 2:
			GD.GD_Max(0);
			break;
		case 3:
			NO.N_Max(0);
			break;
		default:
			throw std::runtime_error("Method not found. Available methods: 1: cgd, 2: gd, 3: ndfp.");
		}
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
