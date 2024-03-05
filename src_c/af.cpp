#include "af.h"


void EncodedAF::addArgument(Argument a) {
    _a.push_back(a);
}

void EncodedAF::addArguments(const std::vector<Argument> & a) {
    for (int i = 0; i < a.size(); ++i) {
        _a.push_back(a[i]);
    }
    initAttackRelation();
}

void EncodedAF::initAttackRelation() {
    _r.clear();
    for (int i = 0; i < _a.size(); ++i) {
        std::vector<int> row;
        for (int j = 0; j < _a.size(); ++j) {
            if (i == j) {  // impossible reflexive attack
                row.push_back(-1);
            } else {
                row.push_back(0);
            }
        }
        _r.push_back(row);
    }
}

AF::AF() {
    _a = std::vector<Argument>();
    _r = std::vector<Attack>();
}

AF::~AF() {
    _a.clear();
    _r.clear();
}