#include "CGDOptimizer.h"
#include <numeric>  
#include <algorithm>
#include <Windows.h>
#include <nlohmann/json.hpp>
#include <fstream> 

Vector2D CGDOptimizer::CGD_step(int x_cur, double w, double v, double t_k, double Mr_Deltat)
{
	double G = CGDOptimizer::func.Gk(x_cur, w, v, t_k);
	std::vector<Vector5D> steps_progress{ Vector5D(w, v, 0, 0, G)};
	double start_v = v;
	int n_dim = 2;
	int max_iter = std::any_cast<int>(CGDOptimizer::getOparams()["max_iter"]);
	double eps = std::any_cast<double>(CGDOptimizer::getOparams()["eps"]);
	double l_r = std::any_cast<double>(CGDOptimizer::getOparams()["l_r"]);
	double Ms = std::any_cast<double>(CGDOptimizer::getMparams()["Ms"]);
	double Mr = std::any_cast<double>(CGDOptimizer::getMparams()["Mr"]);
	double w_k = w;
	double v_k = v;
	double w1 = 0;
	double w2 = 0;
	double dgkdw = 0;
	double dgkdv = 0;
	double step = 0;
	double beta = 0;



	Res dgkdw_r, dgkdv_r;
	dgkdw_r = CGDOptimizer::func.DGkDw(x_cur, w, v, t_k);
	dgkdv_r = CGDOptimizer::func.DGkDv(x_cur, w, v, t_k);

	Vector2D g_k{ dgkdw_r.res, dgkdv_r.res };


	w1 = dgkdw_r.water;
	w2 = dgkdv_r.water;
	Vector2D g_new { 0, 0 };
	Vector2D d_new { 0, 0 };
	Vector2D d_k { g_k.w, g_k.v };
	Vector2D w_v_old{ 0, 0 };

	int k = 0;

	while (k < max_iter && (g_k.norm() > eps))
	{

		double alpha = CGDOptimizer::FindAlpha(d_k, x_cur, t_k, w_k, v_k, -1, 1, 1e-8);
		
		w_v_old.w = w_k;
		w_v_old.v = v_k;
		w_k += alpha * d_k.w;
		v_k += alpha * d_k.v;

		w_k = MAX(0, MIN(1, w_k));
		v_k = MAX(0, MIN(Ms, v_k));



		if (abs(v_k - start_v) > Mr_Deltat) {
			if (v_k > start_v) v_k = start_v + Mr_Deltat;
			else v_k = start_v - Mr_Deltat;
		}

		dgkdw_r = CGDOptimizer::func.DGkDw(x_cur, w_k, v_k, t_k);
		dgkdv_r = CGDOptimizer::func.DGkDv(x_cur, w_k, v_k, t_k);

		g_new = Vector2D(dgkdw_r.res, dgkdv_r.res);
		w1 = dgkdw_r.water;
		w2 = dgkdv_r.water;
		
		if (CGDOptimizer::savef())
		{
			G = CGDOptimizer::func.Gk(x_cur, w_k, v_k, t_k);
			steps_progress.push_back(Vector5D(w_k, v_k, w1, w2, G));
		}

		if (g_new.norm() < eps or (abs(w_v_old.w - w_k) < eps && abs(w_v_old.v - v_k) < eps))
		{
			break;
		}
		
		if (k % n_dim == 0)
		{
			beta = 0;
		}
		else
		{
			beta = pow(g_new.norm(), 2) / pow(g_k.norm(), 2);
		}

		d_new.w = g_new.w + beta * d_k.w;
		d_new.v = g_new.v + beta * d_k.v;

		double dot_prod = d_new.w * g_new.w + d_new.v * g_new.v;
		if (dot_prod <= 0)
		{
			d_new.w = g_new.w;
			d_new.v = g_new.v;
		}

		g_k.w = g_new.w * 1;
		g_k.v = g_new.v * 1;
		d_k.w = d_new.w * 1;
		d_k.v = d_new.v * 1;
		k++;
		
	}
	if (CGDOptimizer::savef())
	{
		auto& optimization_info = std::any_cast<std::map<double, std::vector<Vector5D>>&>(CGDOptimizer::info["Optimization"]);
		optimization_info[t_k] = steps_progress;
	}


	return Vector2D(w_k, v_k);
}

void CGDOptimizer::CGD_Max(int x)
{
	auto& time_info = std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>&>(CGDOptimizer::info["Time"]);
	time_info["Start"] = std::chrono::system_clock::now();

	double avg = CGDOptimizer::field.avgerageField();
	double max = CGDOptimizer::field.maxField();
	double min = CGDOptimizer::field.minField();
	auto& avg_info = std::any_cast<std::map<std::string, double>&>(CGDOptimizer::info["AVG"]);
	avg_info["Start"] = avg;
	auto& max_info = std::any_cast<std::map<std::string, double>&>(CGDOptimizer::info["MAX"]);
	max_info["Start"] = max;
	auto& min_info = std::any_cast<std::map<std::string, double>&>(CGDOptimizer::info["MIN"]);
	min_info["Start"] = min;
	std::any_cast<std::map<double, std::vector<Vector5D>>>(CGDOptimizer::info["Optimization"]).clear();
	std::any_cast<std::map<double, std::vector<Vector6D>>>(CGDOptimizer::info["Optimization_Detailed"]).clear();


	double x_met = 0;
	int	   counter = 0;

	std::vector<Vector6D> progress{};

	std::map<std::string, std::any> FieldMap = CGDOptimizer::field.getFieldMap();

	int rx_cells = std::any_cast<double>(FieldMap["rx_cells"]);
	int ry_cells = std::any_cast<double>(FieldMap["ry_cells"]);

	int cols = std::any_cast<int>(FieldMap["cols"]);
	int rows = std::any_cast<int>(FieldMap["rows"]);

	double cell_length = std::any_cast<double>(FieldMap["cell_length_m"]);
	double lenght_m = std::any_cast<double>(CGDOptimizer::getFparams()["length_m"]);


	double w = std::any_cast<double>(CGDOptimizer::getMparams()["w"]);
	double v = std::any_cast<double>(CGDOptimizer::getMparams()["v"]);

	double Deltat = std::any_cast<double>(CGDOptimizer::getMparams()["Deltat"]);
	double Mr = std::any_cast<double>(CGDOptimizer::getMparams()["Mr"]);

	double Water = 0;

	double t_k = 0;
	double MR_Deltat = Mr * Deltat;



	while (x <= cols + rx_cells)
	{
		Vector2D res = CGDOptimizer::CGD_step(x, w, v, t_k, MR_Deltat);
		w = res.w;
		v = res.v;
		
		int start_col = MAX(0, x - rx_cells); // + 1
		int end_col = MIN(cols, x + 1);

		if (start_col == end_col) start_col -= rx_cells;
		std::vector<double> res_ = CGDOptimizer::field.update_field(x, w, v, CGDOptimizer::func);
		//CGDOptimizer::func.setField(CGDOptimizer::field);
		/*	for (auto el : res_) {
			std::cout << el << " ";
		}
		break;*/
		auto result = std::reduce(res_.begin(), res_.end());
		Water += result;


		if (CGDOptimizer::savef())
		{
			std::vector<std::vector<double>> destination(rows, std::vector<double>(cols));
			auto& source = CGDOptimizer::field.getFieldMap2D();
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

		if (CGDOptimizer::logf())
		{
			if ((int)(t_k) % 25 == 0 || (lenght_m - x_met) < 10) std::cout << "t_k: " << t_k << "  x: " << x << "  w: " << w << "  v: " << v << "  x_met: " << x_met << std::endl;
		}
		x = (int)(round(x_met / cell_length));
		t_k += Deltat;


	}
	if (CGDOptimizer::savef())
	{
		auto& optimization_info_p = std::any_cast<std::map<double, std::vector<Vector6D>>&>(CGDOptimizer::info["Optimization_Detailed"]);
		optimization_info_p[t_k] = progress;
	}
	std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>>(CGDOptimizer::info["Time"])["End"] = std::chrono::system_clock::now();

	CGDOptimizer::info["Water"] = Water;
	double start = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["Base"])["Start"]);
	double end = CGDOptimizer::field.calc_base();
	auto& base = std::any_cast<std::map<std::string, double>&>(CGDOptimizer::info["Base"]);
	base["Diff"] = end - start;
	base["End"] = end;
	double start_avg = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["AVG"])["Start"]);
	double end_avg = CGDOptimizer::field.avgerageField();
	std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["AVG"])["End"] = end_avg;
	std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["AVG"])["Diff"] = end_avg - start_avg;
	double start_max = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["MAX"])["Start"]);
	double end_max = CGDOptimizer::field.maxField();
	std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["MAX"])["End"] = end_max;
	std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["MAX"])["Diff"] = end_max - start_max;
	double start_min = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["MIN"])["Start"]);
	double end_min = CGDOptimizer::field.minField();
	std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["MIN"])["End"] = end_min;
	std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["MIN"])["Diff"] = end_min - start_min;

	auto start_time = std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>>(CGDOptimizer::info["Time"])["Start"];
	auto end_time = std::chrono::system_clock::now();
	std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>>(CGDOptimizer::info["Time"])["End"] = end_time;
	//auto time_diff = end_time - start_time;
	//std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["Time"])["Diff"] = std::chrono::duration_cast<std::chrono::milliseconds>(time_diff).count();
	//
	//std::any_cast<std::map<std::string, double>>(CGDOptimizer::info["Time"])["Diff"] = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();



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
	if (CGDOptimizer::savef())
	{
		if (CGDOptimizer::logf())
		{

			auto time = start_time;
			std::string folderName = "logs";

			std::wstring wideFolderName = std::wstring(folderName.begin(), folderName.end());
			LPCWSTR wfolderName = wideFolderName.c_str();
			CreateDirectory(wfolderName, NULL);

			std::string folderName2 = "logs/log_CGD" + std::to_string(time.time_since_epoch().count());

			std::wstring wideFolderName2 = std::wstring(folderName2.begin(), folderName2.end());
			LPCWSTR wfolderName2 = wideFolderName2.c_str();
			CreateDirectory(wfolderName2, NULL);

			std::string fs_name = folderName2 + "/log_s.txt";
			std::string fs_name2 = folderName2 + "/log_p.txt";
			std::string fs_name3 = folderName2 + "/log_res.txt";

			FILE* file_step = fopen(fs_name.c_str(), "w");
			using json = nlohmann::json;


			auto progress_ = std::any_cast<std::map<double, std::vector<Vector6D>>>(CGDOptimizer::info["Optimization_Detailed"]);
			auto step_progress = std::any_cast<std::map<double, std::vector<Vector5D>>>(CGDOptimizer::info["Optimization"]);
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

			FILE* file_res = fopen(fs_name3.c_str(), "w");
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


			std::ofstream resultFile(fs_name3j);  // ��� �����������
			if (resultFile.is_open()) {
				resultFile << std::setw(4) << resultJson << std::endl;
				resultFile.close();
			}
			else {
				std::cerr << "������ �������� ����� ��� ������: " << fs_name3 << std::endl;
			}
		}
	}
}



double CGDOptimizer::f(double alpha, int x_cur, double t_k, double w, double v, Vector2D grad)
{
	return CGDOptimizer::func.Gk(x_cur, w+alpha*grad.w, v+alpha*grad.v, t_k);
}

double CGDOptimizer::FindAlpha(Vector2D grad, int x_cur, double t_k, double w, double v, double a, double b, double tol)
{
    double gr = (sqrt(5) - 1) / 2;
	double c = b - gr * (b - a);
	double d = a + gr * (b - a);

	int max_iter = 1000;  // ������������ ���������� ��������
	int iter = 0;
	while (abs(c - d) > tol) {
		if (f(c, x_cur, t_k, w, v, grad) > f(d, x_cur, t_k, w, v, grad)) {
			b = d;
		}
		else {
			a = c;
		}

		c = b - gr * (b - a);
		d = a + gr * (b - a);
		iter++;
		if (iter == max_iter) {
			std::cout << "Warning: Maximum iterations (1000) reached in FindAlpha" << std::endl;
			break;
		}
	}
	return (a + b) / 2;
}
