#pragma once
#include <map>
#include <string>
#include <any>

using Section = std::map<std::string, std::any>;

struct Config
{
	std::map<std::string, Section> sections;
};


class ConfigLoader
{
public:
    /*
        ConfigLoader::load() loads a configuration file and returns it as a Config object.
        @param filename The path to the configuration file.
        @return A Config object containing the configuration data.
    */
    bool load(const std::string& filename, Config& config);

private:
    /*
        ConfigLoader::trim() trims leading and trailing whitespace from a string.
	    @param s The string to trim.
	    @return The trimmed string.
    */
    std::string trim(const std::string& s);
};