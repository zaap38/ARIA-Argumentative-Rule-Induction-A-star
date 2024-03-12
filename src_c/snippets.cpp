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