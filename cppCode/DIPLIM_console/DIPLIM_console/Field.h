#pragma once
#include "ModelParams.h"
#include <any>
#include <map>
#include <vector>

class Func;

#define MAX(x,y) ((double)(x) > (double)(y)) ? x : y
#define MIN(x,y) ((double)(x) < (double)(y)) ? x : y

class Field
{
private:
	ModelParams FieldParams;
	std::map<std::string, std::any> FieldMap;
	std::vector<std::vector<double>> FieldMap2D;
public:
	Field(ModelParams& Mparams);
	
	void setField2D(const std::vector<std::vector<double>>& FieldMap2D) { this->FieldMap2D = FieldMap2D; };
	~Field();

	/*         
		Field::calc_base - used to Calculate the base value of the field.

	@param func - The function to be used to calculate the base value.
		- func() --- argument in func Model::a Model::b Model::c and Field
	*/
	double calc_base();
	
	/*
		Field::getFieldMap - used to Get the field map
	*/
	const std::map<std::string, std::any>& getFieldMap() const { return FieldMap; };
	/*
		Field::getFieldMap2D - used to Get the field map
	*/
	const std::map<std::string, std::map<std::string, std::any>>& getParamsMap() const { return FieldParams.getParms(); };
	std::vector<std::vector<double>>& getFieldMap2D() { return FieldMap2D; }; 

	//	Operators for Field
	double& operator()(int i, int j) { return FieldMap2D[i][j]; };
	const double& operator()(int i, int j) const { return FieldMap2D[i][j]; };

	/*
		Field::randomizeField - used to Randomize the field
		@param min_value - The minimum value of the field.
		@param max_value - The maximum value of the field.
	*/
	void randomizeField(double min_value, double max_value);
	/*
		Field::avgerageField - used to Calculate the average value of the field
		@return - The average value of the field
	*/
	double avgerageField();
	/*
		Field::minField - used to Calculate the minimum value of the field
		@return - The minimum value of the field
	*/
	double minField();
	/*
	Field::maxField - used to Calculate the maximum value of the field
	@return - The maximum value of the field
	*/
	double maxField();
	
	/*
		Field::DataField - used to Get the data of the field
		@return - The data of the field (avg, min, max)
	*/
	std::vector<double> DataField();

	/*
		Field::update_cell - used to Update the cell of the field
		@param i - The row of the cell.
		@param j - The column of the cell.
		@param x - The x coordinate of the machine
		@param w - The preasure of water
		@param v - The speed of machine

		@return term - The value by which the cell is updated
	*/
	double update_cell(int i, int j, int x, double w, double v, Func& f);

	/*
	* Field::update_field - used to Update the field
	* @param x - The x coordinate of the machine
	* @param w - The preasure of water
	* @param v - The speed of machine
	* @return vector - The updated cells term values ( in whic they are updated)
	* */
	std::vector<double> update_field(int x, double w, double v, Func& f);

	void setField2D_ij(int i, int j, double value) {FieldMap2D[i][j] = value;};
	
	// Operators
	friend std::ostream& operator<<(std::ostream& os, const Field& field);

};


