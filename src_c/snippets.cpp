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