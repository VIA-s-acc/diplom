#include "Func.h"
#include "Field.h"



Res Func::DGkDw(int x_cur, double w, double v, double t_k)
{
   
   
    int start_col = MAX(0, x_cur - Func::rx_cells);
    int end_col = MIN(cols, x_cur + Func::rx_cells + 1);

    //std::cout << "start_col: " << start_col << " end_col: " << end_col << std::endl;
    //std::cout << "X_cur: " << x_cur <<" w: " << floor(w * 100000) / 100000 << " v: " << v << " t_k: " << t_k << std::endl;
    double Base  = 0;
    double Water = 4 * Func::eta * Func::Wm * Func::Deltat * exp(-Func::delta * v) * Func::rx * Func::ry;
    double exp_alpha_v = exp(-Func::alpha*v);
    
    if (start_col == end_col)
    {
        start_col -= Func::rx_cells;
    }

    int row_start = MAX(0, Func::line - Func::ry_cells);
    int row_end   = MIN(Func::rows, Func::line + Func::ry_cells + 1);
    for (int i = row_start; i < row_end; i++) {
		for (int j = start_col; j < end_col; j++) {
		    if (Func::F(i, j) == -1.0) continue;
            double d_ij = sqrt(pow(i - Func::line, 2) + pow(j - x_cur, 2));
            double term = ((Func::Wm * Func::Deltat) / (pow( (pow(d_ij, 2) + 1), Func::beta))) * exp_alpha_v;
            Base += -2 * Func::a * (Func::F(i,j) + (w * term) - Func::b) * term;
            //std::cout << "i: " << i << " j: " << j << " d_ij: " << d_ij << " term: " << term << " Base: " << Base << " W: " << w << " Water: " << Water << " F: " << Func::F(i, j) << "\n";
        }
	}



    return Res(Base-Water, Water);
}

Res Func::DGkDv(int x_cur, double w, double v, double t_k)
{
    int start_col = MAX(0, x_cur - Func::rx_cells);
    int end_col = MIN(cols, x_cur + Func::rx_cells + 1);

    double Base = 0;
    double Time = -Func::gamma * Func::lambda * t_k * exp(-Func::gamma * v);
    double Water = -Func::delta * 4 * Func::eta * Func::rx * Func::ry * w * Func::Wm * Func::Deltat * exp(-Func::delta * v);

    double exp_alpha_v = exp(-Func::alpha * v);

    if (start_col == end_col) start_col -= Func::rx_cells;

    int row_start = MAX(0, Func::line - Func::ry_cells);
    int row_end = MIN(Func::rows, Func::line + Func::ry_cells + 1);

    for (int i = row_start; i < row_end; i++) {
        for (int j = start_col; j < end_col; j++) {
            if (Func::F(i, j) == -1.0) continue;
            double d_rc = sqrt(pow(i - Func::line, 2) + pow(j - x_cur, 2));
            Base += -2 * Func::a * (Func::F(i, j) + w * ((Func::Wm * Func::Deltat) / pow((pow(d_rc, 2) + 1), Func::beta)) * exp_alpha_v - Func::b) * (-Func::alpha * Func::Deltat * w * Func::Wm * exp_alpha_v / pow((pow(d_rc, 2) + 1), Func::beta));  
        }
    }

    return Res(Base - Time - Water, Water);
}


