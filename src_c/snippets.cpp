#include "snippets.h"


std::vector<std::string> splitStr(const std::string & s, char delim) {
    int index = 0;
    std::vector<std::string> result;
    std::string current = "";
    while (index < s.size()) {
        if (s[index] == delim) {
            result.push_back(current);
            current = "";
        } else {
            current += s[index];
        }
        ++index;
    }
    result.push_back(current);
    return result;
}

bool strIn(const std::vector<std::string> & v, const std::string & e) {
    for (int i = 0; i < v.size(); ++i) {
        if (v[i] == e) {
            return true;
        }
    }
    return false;
}

bool intIn(const std::vector<int> & v, int e) {
    for (int i = 0; i < v.size(); ++i) {
        if (v[i] == e) {
            return true;
        }
    }
    return false;
}

void printVector(const std::vector<std::string> & v) {
    std::cout << '[';
    for (int i = 0; i < v.size(); ++i) {
        std::string sep = ", ";
        if (i == v.size() - 1) sep = "";
        std::cout << v[i] << sep;
    }
    std::cout << ']' << std::endl;
}

double round(double value, int precision) {
    return std::round(value * std::pow(10, precision)) / std::pow(10, precision);
}

std::string trim(const std::string & str) {
    // Find the position of the decimal point
    size_t dotPosition = str.find('.');
    if (dotPosition == std::string::npos) {
        return str; // No decimal point found, return the original string
    }

    // Find the position of the last non-zero digit
    size_t lastNonZeroDigit = str.find_last_not_of('0');
    if (lastNonZeroDigit == std::string::npos) {
        // All digits after the decimal point are zeros
        return str.substr(0, dotPosition);
    } else if (lastNonZeroDigit == dotPosition) {
        // All digits after the decimal point are zeros, except for the last one
        return str.substr(0, lastNonZeroDigit + 2); // Include the decimal point
    } else {
        // Remove trailing zeros after the last non-zero digit
        return str.substr(0, lastNonZeroDigit + 1);
    }
}