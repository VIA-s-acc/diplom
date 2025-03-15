#include "GDOptimizer.h"
#include <numeric>  
#include <algorithm>


Vector2D GDOptimizer::GD_step(int x_cur, double w, double v, double t_k, double Mr_Deltat)
{	

	std::vector<Vector4D> steps_progress{ Vector4D(v, w, 0, 0) };
	double start_v = v;
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
				steps_progress.push_back(Vector4D(v, w, w1, w2));
				std::cout<<"GD3"<<std::endl;
				std::any_cast<std::map<double, std::vector<Vector4D>>>(GDOptimizer::info["Optimization"])[t_k] = steps_progress;
			}
			return Vector2D(w, v);

		}
		else
		{
			w = w_new;
			v = v_new;

			if (GDOptimizer::savef())
			{
				steps_progress.push_back(Vector4D(v, w, w1, w2));
			}
		}
	}
	if (GDOptimizer::savef())
	{
		std::cout<<"GD4"<<std::endl;
		std::any_cast<std::map<double, std::vector<Vector4D>>>(GDOptimizer::info["Optimization"])[t_k] = steps_progress;
	}
	return Vector2D(w, v);
}

void GDOptimizer::GD_Max(int x)
{
	std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>>(GDOptimizer::info["Time"])["Start"] = std::chrono::system_clock::now();
	double x_met   = 0;
	int	   counter = 0;

	std::vector<Vector5D> progress{};

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
			std::vector<std::vector<double>> destination(cols, std::vector<double>(rows));
			auto& source = GDOptimizer::field.getFieldMap2D();
			for (int i = 0; i < rows; ++i) {
				// Copy the row from source to destination using memcpy
				std::memcpy(destination[i].data(), source[i].data(), cols * sizeof(double));
			}

			Vector5D resV5 = Vector5D(w, v, x, x_met, destination);
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
		std::cout<<"8" << std::endl;
		std::any_cast<std::map<double, std::vector<Vector5D>>>(GDOptimizer::info["Optimization"])[t_k] = progress;
	}
	std::any_cast<std::map<std::string, std::chrono::time_point<std::chrono::system_clock>>>(GDOptimizer::info["Time"])["End"] = std::chrono::system_clock::now();
	
	GDOptimizer::info["Water"] = Water;
	double start = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(GDOptimizer::info["Base"])["Start"]);
	double end = GDOptimizer::field.calc_base();
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["Base"])["End"] = end;
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["Base"])["Diff"] = start - end;
	start = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(GDOptimizer::info["AVG"])["Start"]);
	end = GDOptimizer::field.avgerageField();
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["AVG"])["End"] = end;
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["AVG"])["Diff"] = end - start;
	start = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MAX"])["Start"]);
	end = GDOptimizer::field.maxField();
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MAX"])["End"] = end;
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MAX"])["Diff"] = end - start;
	start = std::any_cast<double>(std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MIN"])["Start"]);
	end = GDOptimizer::field.minField();
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MIN"])["End"] = end;
	std::any_cast<std::map<std::string, double>>(GDOptimizer::info["MIN"])["Diff"] = end - start;


	std::cout << "\nres " << std::endl;
	std::cout << GDOptimizer::field.avgerageField() << std::endl;
	std::cout << GDOptimizer::field.maxField() << std::endl;
	std::cout << GDOptimizer::field.minField() << std::endl;
		
}


