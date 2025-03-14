#pragma once
#include <iostream>
#include <map>
#include <any>

class ModelParams
{
    std::map<std::string, std::map<std::string, std::any>> ModelParamsMap;

public:
    ModelParams();
    ~ModelParams();

    void InitParametrs();
    void setModelParams(std::string KeyWord, std::map<std::string, std::any> params);

    /*
    Function getModelParams(KeyWord) used to get parameters from ModelParamsMap

    @param KeyWord(std::string) - key in ModelParamsMap. KeyWord can be "M", "O" or "F":

        M - model parameters,

        O - optimizer parameters,

        F - field parameters

    @return std::map<std::string, std::any> - map of parameters
    */
	std::map<std::string, std::any> getModelParams(std::string KeyWord);
};


