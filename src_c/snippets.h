#pragma once
#include <vector>
#include <string>
#include <iostream>


std::vector<std::string> splitStr(const std::string & s, char delim);

bool strIn(const std::vector<std::string> & v, const std::string & e);
bool intIn(const std::vector<int> & v, int e);

void printVector(const std::vector<std::string> & v);