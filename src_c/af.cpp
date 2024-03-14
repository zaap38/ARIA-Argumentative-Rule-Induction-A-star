#include "af.h"


EncodedAF::EncodedAF() {
    _a = std::vector<Argument>();
    _r = std::vector<std::vector<int>>();
}

EncodedAF::EncodedAF(const EncodedAF & af) {
    _a = af.getArguments();
    _r = af.getAttacks();
}

EncodedAF::EncodedAF(const std::vector<Argument> & arguments) {
    _a = arguments;
    initAttackRelation();
}

EncodedAF::~EncodedAF() {
    _a.clear();
    _r.clear();
}

void EncodedAF::printMatrix() const {
    for (int i = 0; i < _a.size(); ++i) {
        std::cout << _a[i].getName() << " ";
    }
    std::cout << std::endl;
    for (int i = 0; i < _r.size(); ++i) {
        for (int j = 0; j < _r[i].size(); ++j) {
            char value = _r[i][j] == 1? '1' : _r[i][j] == -1? 'x' : '0';
            std::cout << value << " ";
        }
        std::cout << std::endl;
    }
}

AF * EncodedAF::convertToAF() const {
    AF * af = new AF();
    std::vector<Argument> args;
    for (int i = 0; i < _a.size(); ++i) {
        if (isInAttack(_a[i])) {
            args.push_back(_a[i]);
        }
    }
    af->setArguments(args);
    for (int i = 0; i < _r.size(); ++i) {
        for (int j = 0; j < _r[i].size(); ++j) {
            if (_r[i][j] == 1) {
                af->addAttack(_a[i], _a[j]);
            }
        }
    }
    
    return af;
}

Argument * AF::getArgumentByName(const std::string & name) {
    for (int i = 0; i < _a.size(); ++i) {
        if (_a[i].getName() == name) {
            return &_a[i];
        }
    }
    return nullptr;
}

bool EncodedAF::isInAttack(const Argument & a) const {
    int index = -1;
    for (int i = 0; i < _a.size(); ++i) {
        if (_a[i] == a) {
            index = i;
            break;
        }
    }
    for (int i = 0; i < _r.size(); ++i) {
        if (_r[index][i] == 1 || _r[i][index] == 1) {
            return true;
        }
    }
    return false;
}

std::vector<Argument> EncodedAF::getArguments() const {
    return _a;
}

std::vector<std::vector<int>> EncodedAF::getAttacks() const {
    return _r;
}

int EncodedAF::getAttackSize() const {
    int count = 0;
    for (int i = 0; i < _r.size(); ++i) {
        for (int j = 0; j < _r[i].size(); ++j) {
            if (_r[i][j] == 1) {
                ++count;
            }
        }
    }
    return count;
}

std::string EncodedAF::getHash() const {
    std::string hash = "";
    int cpt = 0;
    int sum = 0;
    for (int i = 0; i < _r.size(); ++i) {
        for (int j = 0; j < _r[i].size(); ++j) {
            //hash += std::to_string(_r[i][j]);
            sum += pow(std::max(_r[i][j], 0) * 2, cpt++);
            if (cpt > 7) {
                hash += std::to_string(sum - 1);
                sum = 0;
                cpt = 0;
            
            }
        }
    }
    return hash;
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
    std::tuple<int, int> indexes = getAttackIndex(r);
    int i = std::get<0>(indexes);
    int j = std::get<1>(indexes);
    if (i != -1 && j != -1) {
        _r[i][j] = 1;
        _r[j][i] = -1;
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
    std::tuple<int, int> indexes = getAttackIndex(r);
    int i = std::get<0>(indexes);
    int j = std::get<1>(indexes);
    if (i != -1 && j != -1) {
        _r[i][j] = 0;
        _r[j][i] = 0;
    }
}

std::vector<std::tuple<Argument, Argument>> EncodedAF::getPossibleAddons() const {
    std::vector<Attack> possibleAddons;
    for (int i = 0; i < _a.size(); ++i) {
        for (int j = 0; j < _a.size(); ++j) {
            /*
            Attack not already present, not reflexive, and not already attacked by someone else.
            Attacked node is already attacking something, or is the label.
            Attacker and Attacked do not share the same attribute name.
            */
            if (i != j && _r[i][j] == 0 && (j == 0 || intIn(_r[j], 1))
                    && _a[i].getAttribute() != _a[j].getAttribute()) {
                possibleAddons.push_back(std::make_tuple(_a[i], _a[j]));
            }
        }
    }
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
            if (i == j || i == 0 || _a[i].getAttribute() == _a[j].getAttribute()) {  // attack impossible if reflexive or from label
                row.push_back(-1);
            } else {
                row.push_back(0);
            }
        }
        _r.push_back(row);
    }
    // printMatrix();
}

void EncodedAF::print() const {
    AF * af = convertToAF();
    std::vector<AttackPtr> attacks = af->getAttacks();
    for (int i = 0; i < attacks.size(); ++i) {
        std::cout << std::get<0>(attacks[i])->getName() << " " << std::get<1>(attacks[i])->getName() << std::endl;
    }
    std::cout << "A size: " << af->getArguments().size() << " | R size: " << af->getAttacks().size() << std::endl;
    delete af;
}

AF::AF() {
    _a = std::vector<Argument>();
    _r = std::vector<AttackPtr>();
}

AF::~AF() {
    _a.clear();
    _r.clear();
}

void AF::setArguments(const std::vector<Argument> & a) {
    _a = a;
}

Argument * AF::getArgument(int i) {
    return &_a[i];
}

std::vector<Argument> AF::getArguments() const {
    return _a;
}

std::vector<AttackPtr> AF::getAttacks() const {
    return _r;
}

std::vector<Argument*> AF::getInAttackers(const Argument & a) {
    std::vector<Argument*> inAttacks;
    for (int i = 0; i < _r.size(); ++i) {
        if (*std::get<1>(_r[i]) == a) {
            inAttacks.push_back(std::get<0>(_r[i]));
        }
    }
    return inAttacks;
}

std::vector<Argument*> AF::getOutAttackers(const Argument & a) {
    std::vector<Argument*> outAttacks;
    for (int i = 0; i < _r.size(); ++i) {
        if (*std::get<0>(_r[i]) == a) {
            outAttacks.push_back(std::get<1>(_r[i]));
        }
    }
    return outAttacks;
}

void AF::addArgument(const Argument & a) {
    _a.push_back(a);
}

void AF::addAttack(const AttackPtr & r) {
    _r.push_back(r);
}

void AF::addAttack(const std::string & name1, const std::string & name2) {
    Argument * a1 = getArgumentByName(name1);
    Argument * a2 = getArgumentByName(name2);
    if (a1 != nullptr && a2 != nullptr) {
        addAttack(std::make_tuple(a1, a2));
    }
}

void AF::addAttack(const Argument & a1, const Argument & a2) {
    Argument * a1Ptr = getArgumentByName(a1.getName());
    Argument * a2Ptr = getArgumentByName(a2.getName());
    if (a1Ptr != nullptr && a2Ptr != nullptr) {
        addAttack(std::make_tuple(a1Ptr, a2Ptr));
    }
}

void AF::updateAliveness(const std::vector<Fact> & facts) {
    /*
    Set all arguments to undec if in facts, out otherwise.
    */
    for (int i = 0; i < _a.size(); ++i) {
        _a[i].setOut();
        if (_a[i].isLabel()) {
            _a[i].setUndec();
        } else {
            for (int j = 0; j < facts.size(); ++j) {
                if (_a[i].getName() == facts[j]) {
                    _a[i].setUndec();
                    break;
                }
            }
        }
    }
}

bool AF::predict(const std::vector<Fact> & facts, const std::string & target) {
    updateAliveness(facts);
    computeExtension();
    return targetAlive(target);
}

bool AF::targetAlive(const std::string & target) const {
    for (int i = 0; i < _a.size(); ++i) {
        if (_a[i].getAttribute() == target) {
            return _a[i].in();
        }
    }
    return false;
}

void AF::printArguments() const {
    std::vector<std::string> argNames;
    for (int i = 0; i < _a.size(); ++i) {
        argNames.push_back(_a[i].getName());
    }
    printVector(argNames);
}

void AF::printAttacks() const {
    for (int i = 0; i < _r.size(); ++i) {
        std::cout << std::get<0>(_r[i])->getName() << " " << std::get<1>(_r[i])->getName() << std::endl;
    }
}

void AF::computeExtension(const Fact & target) {
    // if target is not "", break when target is computed
    Argument * root = getRootArgument();
    std::vector<Argument> extension;
    bool doBreak = false;
    while (root != nullptr) {
        root->setIn();
        extension.push_back(*root);
        if (root->getName() == target) doBreak = true;
        std::vector<Argument*> attacked = getOutAttackers(*root);
        for (int i = 0; i < attacked.size(); ++i) {
            attacked[i]->setOut();
            if (attacked[i]->getAttribute() == target) doBreak = true;
        }
        if (doBreak) break;
        root = getRootArgument();
    }
}

Argument * AF::getRootArgument() {
    for (int i = 0; i < _a.size(); ++i) {
        if (isRoot(_a[i])) {
            return &_a[i];
        }
    }
    return nullptr;
}

bool AF::isRoot(const Argument & a) {
    /*
    Is a root if all attackers are dead and node _status is 0 (i.e., TBD).
    */
    std::vector<Argument*> inAttacks = getInAttackers(a);
    if (!a.undec()) return false;
    for (int i = 0; i < inAttacks.size(); ++i) {
        if (!inAttacks[i]->out()) {
            return false;
        }
    }
    return true;
}