#include "ConfigLoader.h"
#include "ConfigLoader.h"
#include <fstream>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <iostream>
#include <regex>

/**
 * Checks if a given string represents an integer.
 *
 * @param str the input string to be checked
 *
 * @return true if the string is an integer, false otherwise
 */
bool isInteger(const std::string& str) {
    static const std::regex intRegex(R"(^-?\d+$)");
    return std::regex_match(str, intRegex);
}
/**
 * Checks if a given string represents an integer.
 *
 * @param str the input string to be checked
 *
 * @return true if the string is an integer, false otherwise
 */
bool isDouble(const std::string& str) {
    static const std::regex doubleRegex(R"(^-?\d+\.\d+$)");
    return std::regex_match(str, doubleRegex);
}


std::string ConfigLoader::trim(const std::string& s) {
    // Remove leading spaces
    auto start = std::find_if_not(s.begin(), s.end(), [](unsigned char ch) {
        return std::isspace(ch);
    });
    // Remove trailing spaces
    auto end = std::find_if_not(s.rbegin(), s.rend(), [](unsigned char ch) {
        return std::isspace(ch);
    }).base();
    return (start < end ? std::string(start, end) : std::string());
}




bool ConfigLoader::load(const std::string& filename, Config& config) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Cannot open file " << filename << std::endl;
        return false;
    }

    std::string line;
    std::string currentSection;
    while (std::getline(file, line)) {
        line = trim(line);
        // Skip empty lines and lines starting with '#' or ';' (comments)
        if (line.empty() || line[0] == '#' || line[0] == ';')
            continue;

        // If the line defines a section, update currentSection
        if (line.front() == '[' && line.back() == ']') {
            currentSection = trim(line.substr(1, line.size() - 2));
            // Create the section if it doesn't exist
            if (config.sections.find(currentSection) == config.sections.end()) {
                config.sections[currentSection] = Section();
            }
        } else {
            // Otherwise, the line should contain a key=value pair.
            size_t pos = line.find('=');
            if (pos == std::string::npos) {
                // Malformed line; skip or handle error as needed.
                continue;
            }
            std::string key = trim(line.substr(0, pos));
            std::string value = trim(line.substr(pos + 1));
            if (!currentSection.empty()) {
                // Store the value as a string wrapped in std::any.
                if (isInteger(value)) {
                    config.sections[currentSection][key] = std::stoi(value);
                }
                else if (isDouble(value)) {
                    config.sections[currentSection][key] = std::stod(value);
                }
                else {
                    config.sections[currentSection][key] = value; // Сохраняем как строку
                }
            }
        }
    }
    return true;
}
