#define _CRT_SECURE_NO_DEPRECATE
#include "GDOptimizer.h"
#include <numeric>  
#include <algorithm>
#include <Windows.h>
#include <nlohmann/json.hpp>
#include <fstream> 

Vector2D GDOptimizer::GD_step(int x_cur, double w, double v, double t_k, double Mr_Deltat)
{	

	double G = GDOptimizer::func.Gk(x_cur, w, v, t_k);
	std::vector<Vector5D> steps_progress{ Vector5D(w, v, 0, 0, G) };	double start_v = v;
	int max_iter = std::any_cast<int>(GDOptimizer::getOparams()["max_iter"]);
	double eps	 = std::any_cast<double>(GDOptimizer::getOparams()["eps"]);
	double l_r   = std::any_cast<double>(GDOptimizer::getOparams()["l_r"]);
	double Ms    = std:: any_cast<double>(GDOptimizer::getMparams()["Ms"]);
	double Mr    = std:: any_cast<double>(GDOptimizer::getMparams()["Mr"]);
	double w_new = 0;
	double v_new = 0;
	double w1 = 0;
	double w2 = 0;
	double dgkdw = 0;
	double dgkdv = 0;
	double step  = 0;

	

	for (int i = 0; i < max_iter; i++)
	{
		
		Res dgkdw_r = GDOptimizer::func.DGkDw(x_cur, w, v, t_k);
		Res dgkdv_r = GDOptimizer::func.DGkDv(x_cur, w, v, t_k);



		dgkdw = dgkdw_r.res;
		dgkdv = dgkdv_r.res;


		w1 = dgkdw_r.water;
		w2 = dgkdv_r.water;


		step = GDOptimizer::func.exp_step(l_r, i);

		w_new = w + dgkdw * step;
		v_new = v + dgkdv * step;

			

		w_new = MAX(0, MIN(1, w_new));
		v_new = MAX(0, MIN(Ms, v_new));

			

		if (abs(v_new - start_v) > Mr_Deltat) {
			if (v_new > start_v) v_new = start_v + Mr_Deltat;
			else v_new = start_v - Mr_Deltat;
		}

			

		//std::cout<<"abs(w_new - w): "<<abs(w_new - w)<<" abs(v_new - v): "<<abs(v_new - v)<<" i: "<<i<<std::endl;
		if (abs(w_new - w) < eps && abs(v_new - v) < eps && i != 0)
		{
			w = w_new;
			v = v_new;
			//std::cout<<"GD2"<<std::endl;
			if (GDOptimizer::savef())
			{
				G = GDOptimizer::func.Gk(x_cur, w, v, t_k);
				steps_progress.push_back(Vector5D(w, v, w1, w2, G));
				auto& optimization_info = std::any_cast<std::map<double, std::vector<Vector5D>>&>(GDOptimizer::info["Optimization"]);
				optimization_info[t_k] = steps_progress;
			}
			return Vector2D(w, v);

		}
		else
		{
			w = w_new;
			v = v_new;

			if (GDOptimizer::savef())
			{
				G = GDOptimizer::func.Gk(x_cur, w, v, t_k);
				steps_progress.push_back(Vector5D(w, v, w1, w2, G));
			}
		}
	}
	if (GDOptimizer::savef())
	{
		auto& optimization_info = std::any_cast<std::map<double, std::vector<Vector5D>>&>(GDOptimizer::info["Optimization"]);
		optimization_info[t_k] = steps_progress;
	}
	
	return Vector2D(w, v);
}

void GDOptimizer::GD_Max(int x)
{
	auto& time_info = std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>&>(GDOptimizer::info["Time"]);
	time_info["Start"] = std::chrono::system_clock::now();
	
	double avg = GDOptimizer::field.avgerageField();
	double max = GDOptimizer::field.maxField();
	double min = GDOptimizer::field.minField();
	auto& avg_info = std::any_cast<std::map<std::string, double>&>(GDOptimizer::info["AVG"]);
	avg_info["Start"] = avg;
	auto& max_info = std::any_cast<std::map<std::string, double>&>(GDOptimizer::info["MAX"]);
	max_info["Start"] = max;
	auto& min_info = std::any_cast<std::map<std::string, double>&>(GDOptimizer::info["MIN"]);
	min_info["Start"] = min;
	std::any_cast<std::map<double, std::vector<Vector5D>>>(GDOptimizer::info["Optimization"]).clear();
	std::any_cast<std::map<double, std::vector<Vector6D>>>(GDOptimizer::info["Optimization_Detailed"]).clear();


	double x_met   = 0;
	int	   counter = 0;

	std::vector<Vector6D> progress{};

	std::map<std::string, std::any> FieldMap = GDOptimizer::field.getFieldMap();

	int rx_cells = std::any_cast<double>(FieldMap["rx_cells"]);
	int ry_cells = std::any_cast<double>(FieldMap["ry_cells"]);

	int cols     = std::any_cast<int>(FieldMap["cols"]);
	int rows     = std::any_cast<int>(FieldMap["rows"]);

	double cell_length = std::any_cast<double>(FieldMap["cell_length_m"]);
	double lenght_m	   = std::any_cast<double>(GDOptimizer::getFparams()["length_m"]);

	
	double w     = std::any_cast<double>(GDOptimizer::getMparams()["w"]);
	double v     = std::any_cast<double>(GDOptimizer::getMparams()["v"]);

	double Deltat = std::any_cast<double>(GDOptimizer::getMparams()["Deltat"]);
	double Mr	  = std::any_cast<double>(GDOptimizer::getMparams()["Mr"]);

	double Water = 0;

	double t_k = 0;
	double MR_Deltat = Mr * Deltat;
	


	while (x <= cols + rx_cells)
	{
		Vector2D res = GDOptimizer::GD_step(x, w, v, t_k, MR_Deltat);
		w = res.w;
		v = res.v;

		int start_col = MAX(0, x - rx_cells); // + 1
		int end_col = MIN(cols, x + 1);

		if (start_col == end_col) start_col -= rx_cells;
		std::vector<double> res_ = GDOptimizer::field.update_field(x, w, v, GDOptimizer::func);
		//GDOptimizer::func.setField(GDOptimizer::field);
		/*	for (auto el : res_) {
			std::cout << el << " ";
		}
		break;*/
		auto result = std::reduce(res_.begin(), res_.end());
		Water += result;


		if (GDOptimizer::savef())
		{
			std::vector<std::vector<double>> destination(rows, std::vector<double>(cols));
			auto& source = GDOptimizer::field.getFieldMap2D();
			if (source.size() != rows || source[0].size() != cols) {
				std::cout << "Error: source and destination matrices have different sizes." << std::endl;
			}
			for (int i = 0; i < rows; ++i) {
				std::memcpy(destination[i].data(), source[i].data(), cols * sizeof(double));
			}

			double G_val = func.Gk(x, w, v, t_k);
			Vector6D resV5 = Vector6D(t_k, w, v, x, x_met, G_val, destination);
			progress.push_back(resV5);
		}

		double change = v * Deltat;
		if (change <= 1e-8)
		{
			counter += 1;
			if (counter == 3)
			{
				v += Mr;
			}
		}
		else counter = 0;
		x_met += change;
		
		if (GDOptimizer::logf())
		{
			if ((int)(t_k) % 25 == 0 || (lenght_m-x_met) < 10) std::cout << "t_k: " << t_k << "  x: " << x << "  w: " << w << "  v: " << v << "  x_met: " << x_met << std::endl;
		}
		x = (int)(round(x_met / cell_length));
		t_k += Deltat;
		
			
	}
	if (GDOptimizer::savef())
	{
		auto& optimization_info_p = std::any_cast<std::map<double, std::vector<Vector6D>>&>(GDOptimizer::info["Optimization_Detailed"]);
		optimization_info_p[t_k] = progress;
	}
	std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>>(GDOptimizer::info["Time"])["End"] = std::chrono::system_clock::now();
	
	GDOptimizer::info["Water"] = Water;
	double start = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(GDOptimizer::info["Base"])["Start"]);
	double end = GDOptimizer::field.calc_base();
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["Base"])["End"] = end;
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["Base"])["Diff"] = start - end;
	double start_avg = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(GDOptimizer::info["AVG"])["Start"]);
	double end_avg = GDOptimizer::field.avgerageField();
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["AVG"])["End"] = end_avg;
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["AVG"])["Diff"] = end_avg - start_avg;
	double start_max = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MAX"])["Start"]);
	double end_max = GDOptimizer::field.maxField();
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MAX"])["End"] = end_max;
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MAX"])["Diff"] = end_max - start_max;
	double start_min = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MIN"])["Start"]);
	double end_min = GDOptimizer::field.minField();
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MIN"])["End"] = end_min;
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MIN"])["Diff"] = end_min - start_min;

	auto start_time = std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>>(GDOptimizer::info["Time"])["Start"];
	auto end_time = std::chrono::system_clock::now();
	std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>>(GDOptimizer::info["Time"])["End"] = end_time;
	//auto time_diff = end_time - start_time;
	//std::any_cast<std::map<std::string, double>>(GDOptimizer::info["Time"])["Diff"] = std::chrono::duration_cast<std::chrono::milliseconds>(time_diff).count();
	//
	//std::any_cast<std::map<std::string, double>>(GDOptimizer::info["Time"])["Diff"] = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();



	std::cout << "\n\t\t\t------ res ------\t\t\t" << std::endl;
	std::cout << "Start AVG: " << start_avg << " End AVG: " << end_avg << " Diff AVG: " << end_avg - start_avg << std::endl;
	std::cout << "Start MAX: " << start_max << " End MAX: " << end_max << " Diff MAX: " << end_max - start_max << std::endl;
	std::cout << "Start MIN: " << start_min << " End MIN: " << end_min << " Diff MIN: " << end_min - start_min << std::endl;
	std::cout << "Start BASE: " << start << " End BASE: " << end << " Diff BASE: " << end - start << std::endl;
	std::cout << "Water: " << Water << std::endl;
	std::cout << "Start_Time: " << start_time << " End_Time: " << end_time << std::endl << "Duration: ";
	
	auto duration = end_time - start_time;
	auto hours = std::chrono::duration_cast<std::chrono::hours>(duration).count();
	auto minutes = std::chrono::duration_cast<std::chrono::minutes>(duration % std::chrono::hours(1)).count();
	auto seconds = std::chrono::duration_cast<std::chrono::seconds>(duration % std::chrono::minutes(1)).count();
	auto milliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(duration % std::chrono::seconds(1)).count();

	std::string dur_string = std::to_string(hours) + " H " + std::to_string(minutes) + " M " + std::to_string(seconds) + " S " + std::to_string(milliseconds) + " MS";
	std::string start_time_string = std::to_string(start_time.time_since_epoch().count());
	std::string end_time_string = std::to_string(end_time.time_since_epoch().count());
	std::cout << dur_string << std::endl;
	if (GDOptimizer::savef())
	{
		if (GDOptimizer::logf())
		{

			auto time = start_time;
			std::string folderName = "logs";

			std::wstring wideFolderName = std::wstring(folderName.begin(), folderName.end());
			LPCWSTR wfolderName = wideFolderName.c_str();
			CreateDirectory(wfolderName, NULL);

			std::string folderName2 = "logs/log_GD" + std::to_string(time.time_since_epoch().count());

			std::wstring wideFolderName2 = std::wstring(folderName2.begin(), folderName2.end());
			LPCWSTR wfolderName2 = wideFolderName2.c_str();
			CreateDirectory(wfolderName2, NULL); 

			std::string fs_name = folderName2 + "/log_s.txt";
			std::string fs_name2 = folderName2 + "/log_p.txt";
			std::string fs_name3 = folderName2 + "/log_res.txt"; 

			FILE* file_step = fopen(fs_name.c_str(), "w");
			using json = nlohmann::json;
			

			auto progress_ = std::any_cast<std::map<double, std::vector<Vector6D>>>(GDOptimizer::info["Optimization_Detailed"]);
			auto step_progress = std::any_cast<std::map<double, std::vector<Vector5D>>>(GDOptimizer::info["Optimization"]);
			//std::cout << "\n\t\t\t------ step_progress ------\t\t\t" << std::endl;
			fprintf(file_step, "\n\t\t\t------ step_progress ------\t\t\t\n");
			for (auto& el : step_progress) {
				//std::cout << "\t\t\t-------- T_k: " << el.first << " ------- \t\t\t" << std::endl;
				fprintf(file_step, "\t\t\t-------- T_k: %f ------- \t\t\t\n", el.first);
				for (auto& el2 : el.second) {
					fprintf(file_step, "\t\t w: %f v: %f w1: %f w2: %f \t\t\t\n", el2.w, el2.v, el2.w1, el2.w2);
					//std::cout << "\t\t w: " << el2.w << " v: " << el2.v << " w1: " << el2.w1 << " w2: " << el2.w2 << " \t\t\t" << std::endl;
				
				}
				fprintf(file_step, "\n\n");
				//std::cout << std::endl << std::endl;
			}
			fclose(file_step);
			FILE* file_prog = fopen(fs_name2.c_str(), "w");
			//std::cout << "\n\t\t\t------ progress_ ------\t\t\t" << std::endl;
			fprintf(file_prog, "\n\t\t\t------ progress_ ------\t\t\t\n");
			for (auto& el : progress_) {
				//std::cout << "\t\t\t-------- T_k: " << el.first << " ------- \t\t\t" << std::endl;
				fprintf(file_prog, "\t\t\t-------- T_k: %f ------- \t\t\t\n", el.first);
				for (auto& el2 : el.second) {
					fprintf(file_prog, "\t\tt_k: %f w: %f v: %f x: %d w_met: %f \t\t\t\n", el2.t_k, el2.w, el2.v, el2.x, el2.x_m);
					//std::cout << "\t\t w: " << el2.w << " v: " << el2.v << " x: " << el2.x << " w_met: " << el2.x_m << " \t\t\t" << std::endl;
				}
				fprintf(file_prog, "\n\n");
				//std::cout << std::endl << std::endl;
			}

			fclose(file_prog);
			
			FILE *file_res = fopen(fs_name3.c_str(), "w");
			//std::cout << "\n\t\t\t------ result_ ------\t\t\t" << std::endl;

			
			std::string fs_namej = folderName2 + "/log_s.json";
			std::string fs_name2j = folderName2 + "/log_p.json";
			std::string fs_name3j = folderName2 + "/log_res.json";
			FILE* file_res3 = fopen(fs_name3.c_str(), "w");
			fprintf(file_res3, "\n\t\t\t------ res ------\t\t\t\n");
			fprintf(file_res3, "Start AVG: %f End AVG: %f Diff AVG: %f\n", start_avg, end_avg, end_avg - start_avg);
			fprintf(file_res3, "Start MAX: %f End MAX: %f Diff MAX: %f\n", start_max, end_max, end_max - start_max);
			fprintf(file_res3, "Start MIN: %f End MIN: %f Diff MIN: %f\n", start_min, end_min, end_min - start_min);
			fprintf(file_res3, "Start BASE: %f End BASE: %f Diff BASE: %f\n", start, end, end - start);
			fprintf(file_res3, "Water: %f\n", Water);
			fprintf(file_res3, "Start_Time: %s End_Time: %s\n", start_time_string.c_str(), end_time_string.c_str());
			fprintf(file_res3, "Duration: %s\n", dur_string.c_str());
			fclose(file_res3);
			

			json stepProgressJson;
			json progressJson;
			json resultJson; 

			for (auto& el : step_progress) {
				json stepEntry;
				stepEntry["T_k"] = el.first;

				std::vector<json> details;
				for (auto& el2 : el.second) {
					json detail;
					detail["w"] = el2.w;
					detail["v"] = el2.v;
					detail["w1"] = el2.w1;
					detail["w2"] = el2.w2;
					detail["G"] = el2.G;

					details.push_back(detail);
				}
				stepEntry["details"] = details;
				stepProgressJson.push_back(stepEntry);
			}

			for (auto& el : progress_) {
				json progressEntry;
				progressEntry["T"] = el.first;

				std::vector<json> details;
				for (auto& el2 : el.second) {
					json detail;
					detail["t_k"] = el2.t_k;
					detail["w"] = el2.w;
					detail["v"] = el2.v;
					detail["x"] = el2.x;
					detail["w_met"] = el2.x_m;
					detail["G"] = el2.G;

					details.push_back(detail);
				}
				progressEntry["details"] = details;
				progressJson.push_back(progressEntry);
			}

			std::ofstream stepFile(fs_namej);
			stepFile << std::setw(4) << stepProgressJson << std::endl;
			stepFile.close();

			std::ofstream progressFile(fs_name2j);
			progressFile << std::setw(4) << progressJson << std::endl;
			progressFile.close();

			resultJson["Start AVG"] = start_avg;
			resultJson["End AVG"] = end_avg;
			resultJson["Diff AVG"] = end_avg - start_avg;

			resultJson["Start MAX"] = start_max;
			resultJson["End MAX"] = end_max;
			resultJson["Diff MAX"] = end_max - start_max;

			resultJson["Start MIN"] = start_min;
			resultJson["End MIN"] = end_min;
			resultJson["Diff MIN"] = end_min - start_min;

			resultJson["Start BASE"] = start;
			resultJson["End BASE"] = end;
			resultJson["Diff BASE"] = end - start;

			resultJson["Water"] = Water;

			resultJson["Start Time"] = start_time_string;
			resultJson["End Time"] = end_time_string;
			resultJson["Duration"] = dur_string;


			std::ofstream resultFile(fs_name3j);  // Для результатов
			if (resultFile.is_open()) {
				resultFile << std::setw(4) << resultJson << std::endl;
				resultFile.close();
			}
			else {
				std::cerr << "Ошибка открытия файла для записи: " << fs_name3 << std::endl;
			}
		}
	}
}


