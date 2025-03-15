#pragma once
#include <iostream>
#include <map>
#include <any>
#include "ConfigLoader.h"



class ModelParams
{
    std::map<std::string, std::map<std::string, std::any>> ModelParamsMap;

public:
    // constructor
    ModelParams();
    // destructor
    ~ModelParams();

    /*
        Init ModelParamsMap
    */
    void InitParametrs();
    
    /*
        ModelParams::LoadModelSectionParams(KeyWord, params) used to set parameters in ModelParamsMap

        @param KeyWord(std::string) - key in ModelParamsMap. KeyWord can be "M", "O" or "F":

			M - model parameters,

			O - optimizer parameters,

			F - field parameters

		@param params(std::map<std::string, std::any>) - map of parameters
        @return void
    */
    void LoadModelSectionParams(std::string KeyWord, std::map<std::string, std::any> params);
    /*
        ModelParams::LoadModelParams(paramsM, paramsO, paramsF) used to set parameters in ModelParamsMap

		@param paramsM(std::map<std::string, std::any>) - map of model parameters
		@param paramsO(std::map<std::string, std::any>) - map of optimizer parameters
		@param paramsF(std::map<std::string, std::any>) - map of field parameters
		@return void
    
    */
    void LoadModelParams(std::map<std::string, std::any> paramsM, std::map<std::string, std::any> paramsO, std::map<std::string, std::any> paramsF);
    /*
        ModelParams::LoadModelFromFile(filename) used to set parameters in ModelParamsMap from file

		@param filename(std::string) - path to file
		@return void

    */
    void LoadModelFromFile(std::string filename);
    


    /*
        ModelParams::getParam(KeyWord, ParamName) used to get parameter from ModelParamsMap

		@param KeyWord(std::string) - key in ModelParamsMap. KeyWord can be "M", "O" or "F":
            M - model parameters,   

            O - optimizer parameters,

			F - field parameters

		@param ParamName(std::string) - name of parameter.
            Check cfg file
		@return std::any 
    */
    std::any getParam(std::string KeyWord, std::string ParamName);
    
    
    /*
    ModelParams::getModelParams(KeyWord) used to get parameters from ModelParamsMap

    @param KeyWord(std::string) - key in ModelParamsMap. KeyWord can be "M", "O" or "F":

        M - model parameters,

        O - optimizer parameters,

        F - field parameters

    @return std::map<std::string, std::any> - map of parameters
    */
	std::map<std::string, std::any>  getModelParams (std::string KeyWord) ;
    /*
        ModelParams::getParms() used to get ModelParamsMap
    */
    std::map<std::string, std::map<std::string, std::any>> const getParms() const { return ModelParamsMap;};
};


