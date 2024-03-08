#include "af.h"


EncodedAF::EncodedAF() {
    _a = std::vector<Argument>();
    _r = std::vector<std::vector<int>>();
}

EncodedAF::EncodedAF(const EncodedAF & af) {
    _a = af.getArguments();
    _r = af.getAttacks();
}

EncodedAF::~EncodedAF() {
    _a.clear();
    _r.clear();
}

AF * EncodedAF::convertToAF() const {
    AF * af = new AF();
    for (int i = 0; i < _r.size(); ++i) {
        af->addArgument(_a[i]);
        for (int j = 0; j < _r[i].size(); ++j) {
            if (_r[i][j] == 1) {
                af->addAttack(std::make_tuple(_a[i], _a[j]));
            }
        }
    }
    return af;
}

std::vector<Argument> EncodedAF::getArguments() const {
    return _a;
}

std::vector<std::vector<int>> EncodedAF::getAttacks() const {
    return _r;
}

std::vector<Attack> EncodedAF::getAttackTuples() const {
    std::vector<Attack> attackTuples;
    for (int i = 0; i < _r.size(); ++i) {
        for (int j = 0; j < _r[i].size(); ++j) {
            if (_r[i][j] == 1) {
                attackTuples.push_back(std::make_tuple(_a[i], _a[j]));
            }
        }
    }
    return attackTuples;
}

void EncodedAF::addAttack(const Attack & r) {
    Argument a1 = std::get<0>(r);
    Argument a2 = std::get<1>(r);
    std::tuple<int, int> indexes = getAttackIndex(r);
    int i = std::get<0>(indexes);
    int j = std::get<1>(indexes);
    if (i != -1 && j != -1) {
        _r[i][j] = 1;
    }
}

std::tuple<int, int> EncodedAF::getAttackIndex(const Attack & r) const {
    Argument a1 = std::get<0>(r);
    Argument a2 = std::get<1>(r);
    int i = -1;
    int j = -1;
    for (int k = 0; k < _a.size(); ++k) {
        if (_a[k] == a1) {
            i = k;
        }
        if (_a[k] == a2) {
            j = k;
        }
        if (i != -1 && j != -1) {
            break;
        }
    }
    return std::make_tuple(i, j);
}

void EncodedAF::removeAttack(const Attack & r) {
    Argument a1 = std::get<0>(r);
    Argument a2 = std::get<1>(r);
    std::tuple<int, int> indexes = getAttackIndex(r);
    int i = std::get<0>(indexes);
    int j = std::get<1>(indexes);
    if (i != -1 && j != -1) {
        _r[i][j] = 0;
    }
}

std::vector<Attack> EncodedAF::getPossibleAddons() const {
    std::vector<Attack> possibleAddons;
    // TODO: return the attacks which can be added to the current AF
    return possibleAddons;
}

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

std::vector<Argument> AF::getArguments() const {
    return _a;
}

std::vector<Attack> AF::getAttacks() const {
    return _r;
}

std::vector<Argument> AF::getInAttacks(const Argument & a) const {
    std::vector<Argument> inAttacks;
    for (int i = 0; i < _r.size(); ++i) {
        if (std::get<1>(_r[i]) == a) {
            inAttacks.push_back(std::get<0>(_r[i]));
        }
    }
    return inAttacks;
}

std::vector<Argument> AF::getOutAttacks(const Argument & a) const {
    std::vector<Argument> outAttacks;
    for (int i = 0; i < _r.size(); ++i) {
        if (std::get<0>(_r[i]) == a) {
            outAttacks.push_back(std::get<1>(_r[i]));
        }
    }
    return outAttacks;
}

void AF::addArgument(const Argument & a) {
    _a.push_back(a);
}

void AF::addAttack(const Attack & r) {
    _r.push_back(r);
}

void AF::updateAliveness(const std::vector<Fact> & facts) {
    for (int i = 0; i < _a.size(); ++i) {
        _a[i].setStatus(false);
        for (int j = 0; j < facts.size(); ++j) {
            if (_a[i].getName() == facts[j]) {
                _a[i].setStatus(true);
                break;
            }
        }
    }
}

bool AF::predict(const std::vector<Fact> & facts, const Fact & target) {
    updateAliveness(facts);
    computeExtension();
    return targetAlive(target);
}

bool AF::targetAlive(const Fact & target) const {
    for (int i = 0; i < _a.size(); ++i) {
        if (_a[i].getName() == target) {
            return _a[i].getStatus();
        }
    }
    return false;
}

void AF::computeExtension() {
    // TODO: grounded extension
}