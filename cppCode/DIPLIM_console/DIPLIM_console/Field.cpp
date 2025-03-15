#include "Field.h"
#include "ModelParams.h"
#include <cmath>
#include <thread>
#include <future>
#include <algorithm>
#include "Func.h"


Field::Field(ModelParams& Mparams)
{
	Field::FieldParams = Mparams;
	Field::FieldMap = Mparams.getModelParams("F");

	
	double cell_length_m = std::any_cast<double>(Field::FieldMap["length_m"]) / std::any_cast<int>(Field::FieldMap["cols"]);
	double cell_width_m = std::any_cast<double>(Field::FieldMap["width_m"]) / std::any_cast<int>(Field::FieldMap["rows"]);
	
	
	double rx_cells = (int)(std::any_cast<double>(Field::FieldMap["rx"]) / cell_length_m);
	double ry_cells = (int)(std::any_cast<double>(Field::FieldMap["ry"]) / cell_width_m);

	
	Field::FieldMap["rx_cells"] = rx_cells;
	Field::FieldMap["ry_cells"] = ry_cells;
	Field::FieldMap["cell_length_m"] = cell_length_m;
	Field::FieldMap["cell_width_m"] = cell_width_m;
	int line = std::any_cast<int>(Field::FieldMap["line"]);
	Field::FieldMap["line"] = line;
	Field::FieldMap2D = std::vector<std::vector<double>>(std::any_cast<int>(Field::FieldMap["rows"]), std::vector<double>(std::any_cast<int>(Field::FieldMap["cols"]), 0.0));
	FieldMap2D[line] = std::vector<double>(std::any_cast<int>(Field::FieldMap["cols"]), -1);
}

Field::~Field()
{
	Field::FieldMap.clear();
}

double Field::calc_base()
{
	double res = 0;
	int rows = std::any_cast<int>(Field::FieldMap["rows"]);
	int cols = std::any_cast<int>(Field::FieldMap["cols"]);
	double a = std::any_cast<double>(Field::FieldParams.getParam("M", "a"));
	double b = std::any_cast<double>(Field::FieldParams.getParam("M", "b"));
	double c = std::any_cast<double>(Field::FieldParams.getParam("M", "c"));
	for (int i = 0; i < rows; i++)
	{
		for (int j = 0; j < cols; j++)
		{
			if ((*this)(i, j) == -1) continue;
			res += -a * pow(((*this)(i, j) - b), 2) + c;
		}
	}
	return res;
}

void Field::randomizeField(double min_value, double max_value)
{
	int rows = std::any_cast<int>(Field::FieldMap["rows"]);
	int cols = std::any_cast<int>(Field::FieldMap["cols"]);

	for ( int i = 0; i < rows; i++) {
		for (int j = 0; j < cols; j++) {
			if ((*this)(i, j) == -1) continue;
			double value = min_value + static_cast<double>(rand()) / (static_cast<double>(RAND_MAX) / (max_value - min_value));
			(*this)(i, j) = value;
		}
	}
}

double Field::avgerageField()
{
	int rows = std::any_cast<int>(Field::FieldMap["rows"]);
	int cols = std::any_cast<int>(Field::FieldMap["cols"]);
	double res = 0;
	for (int i = 0; i < rows; i++) {
		for (int j = 0; j < cols; j++) {
			double el = (*this)(i, j);
			if (el >= 0.0) res += el;
		}
	}
	return res / (rows * cols);
}

double Field::minField()
{
	double min = 0;
	int rows = std::any_cast<int>(Field::FieldMap["rows"]);
	int cols = std::any_cast<int>(Field::FieldMap["cols"]);
	for (int i = 0; i < rows; i++) {
		for (int j = 0; j < cols; j++) {
			double el = (*this)(i, j);
			if (el < min) min = el;
		}
	}
	return min;
}

double Field::maxField()
{
double max = 0;
	int rows = std::any_cast<int>(Field::FieldMap["rows"]);
	int cols = std::any_cast<int>(Field::FieldMap["cols"]);
	for (int i = 0; i < rows; i++) {
		for (int j = 0; j < cols; j++) {
			double el = (*this)(i, j);
			if (el > max) max = el;
		}
	}
	return max;
}

std::vector<double> Field::DataField()
{
	double avg = avgerageField();
	double min = minField();
	double max = maxField();
	std::vector<double> res = { avg, min, max };
	return res;
}

double Field::update_cell(int i, int j, int x, double w, double v)
{
	if ((*this)(i, j) == -1.0) return 0.0;
	double Wm = std::any_cast<double>(Field::FieldParams.getParam("M", "Wm"));
	double Dt = std::any_cast<double>(Field::FieldParams.getParam("M", "Deltat"));
	double beta = std::any_cast<double>(Field::FieldParams.getParam("M", "beta"));
	double alpha = std::any_cast<double>(Field::FieldParams.getParam("M", "alpha"));

	double d_ij = pow(pow(i - std::any_cast<int>(Field::FieldMap["line"]), 2) + pow((j - x), 2), 0.5);
	double term = w * (Wm * Dt / pow((pow(d_ij, 2) + 1), beta)) * exp(-alpha * v);

	(*this)(i, j) += term;

	return term;
}
std::vector<double> Field::update_field(int x, double w, double v)
{
	int rows = std::any_cast<int>(Field::FieldMap["rows"]);
	int cols = std::any_cast<int>(Field::FieldMap["cols"]);
	int rx_cells = std::any_cast<double>(Field::FieldMap["rx_cells"]);
	int ry_cells = std::any_cast<double>(Field::FieldMap["ry_cells"]);
	int line = std::any_cast<int>(Field::FieldMap["line"]);


	// start col, end col
	int start_row = std::max(0, line - ry_cells);
	int end_row = std::min(rows, line + ry_cells + 1);
	
	int start_col = MAX(0, x - rx_cells);
	int end_col = MIN(cols, x + rx_cells + 1);

	if (start_col == end_col) {
		start_col -= rx_cells;
	}

	std::vector<std::future<double>> futures;
	std::vector<double> results;

	// parallel update
	for (int i = start_row; i < end_row; i++) {
		for (int j = start_col; j < end_col; j++) {
			futures.push_back(std::async(std::launch::async, &Field::update_cell, this, i, j, x, w, v));
		}
	}

	// collect results
	for (auto& future : futures)
	{
		results.push_back(future.get());
	}
	
	return results;
}

std::ostream& operator<<(std::ostream& os, const Field& field)
{
	std::map<std::string, std::any> fieldMap = field.getFieldMap();

	// Преобразуем данные в строку с правильным форматированием
	std::string s = "Rows: " + std::to_string(std::any_cast<int>(fieldMap["rows"])) +
		" Columns: " + std::to_string(std::any_cast<int>(fieldMap["columns"])) + "\n";
	s += "Length: " + std::to_string(std::any_cast<double>(fieldMap["length_m"])) +
		" Width: " + std::to_string(std::any_cast<double>(fieldMap["width_m"])) + "\n";
	s += "Rx: " + std::to_string(std::any_cast<double>(fieldMap["rx"])) +
		" Ry: " + std::to_string(std::any_cast<double>(fieldMap["ry"])) +
		s += "Rx (cells): " + std::to_string(std::any_cast<double>(fieldMap["rx_cells"])) +
		" Ry (cells): " + std::to_string(std::any_cast<double>(fieldMap["ry_cells"])) + "\n";  // Исправлено Rz

	return os << s;
}

