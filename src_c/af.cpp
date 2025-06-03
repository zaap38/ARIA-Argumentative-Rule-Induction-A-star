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
            char value = _r[i][j] >= 1? '0' + _r[i][j] : _r[i][j] == -1? 'x' : '0';
            std::cout << value << " ";
        }
        std::cout << std::endl;
    }
}

AF * EncodedAF::convertToAF() const {
    AF * af = new AF();
    std::vector<Argument> args;
    for (int i = 0; i < _a.size(); ++i) {
        if (isInAttackOrSupport(_a[i])) {
            args.push_back(_a[i]);
        }
    }
    af->setArguments(args);
    for (int i = 0; i < _r.size(); ++i) {
        for (int j = 0; j < _r[i].size(); ++j) {
            if (_r[i][j] == 1) {
                af->addAttack(_a[i], _a[j]);
            } else if (_r[i][j] == 2) {
                af->addSupport(_a[i], _a[j]);
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

bool EncodedAF::isInSupport(const Argument & a) const {
    int index = -1;
    for (int i = 0; i < _a.size(); ++i) {
        if (_a[i] == a) {
            index = i;
            break;
        }
    }
    for (int i = 0; i < _r.size(); ++i) {
        if (_r[index][i] == 2 || _r[i][index] == 2) {
            return true;
        }
    }
    return false;
}

bool EncodedAF::isInAttackOrSupport(const Argument & a) const {
    int index = -1;
    for (int i = 0; i < _a.size(); ++i) {
        if (_a[i] == a) {
            index = i;
            break;
        }
    }
    for (int i = 0; i < _r.size(); ++i) {
        if (_r[index][i] >= 1 || _r[i][index] >= 1) {
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
            if (_r[i][j] >= 1) {  // include supports
                ++count;
            }
        }
    }
    return count;
}

std::string EncodedAF::getHash(const std::string & callFrom) const {
    //if (callFrom != "") std::cout << "getHash() called from " << callFrom << std::endl;
    std::string hash = "";
    int cpt = 0;
    int wordSize = 32;
    uint64_t maxValue = 0;
    uint64_t sum = 0;
    for (int i = 0; i < wordSize; ++i) {
        maxValue += pow(2, i);
    }
    int paddingLength = std::to_string(maxValue).size();
    //std::cout << maxValue << "=========>" << paddingLength << std::endl;
    for (int i = 0; i < _r.size(); ++i) {
        for (int j = 0; j < _r[i].size(); ++j) {
            //hash += std::to_string(_r[i][j]);
            sum += std::max(_r[i][j], 0) * pow(2, cpt++);
            if (cpt > wordSize || (i == _r.size() - 1 && j == _r[i].size() - 1)) {
                std::string tmp = std::to_string(sum);
                while (tmp.size() < paddingLength) tmp = "0" + tmp;
                //std::cout << tmp.size() << " " << paddingLength << std::endl;
                //std::cout << " ----> " << sum << " == " << tmp << std::endl;
                hash += tmp;
                sum = 0;
                cpt = 0;
            }
        }
    }
    //std::cout << "hash " << hash << std::endl;
    //this->print();
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

void EncodedAF::addAttack(const Attack & r, int type) {
    std::tuple<int, int> indexes = getAttackIndex(r);
    int i = std::get<0>(indexes);
    int j = std::get<1>(indexes);
    if (i != -1 && j != -1) {
        _r[i][j] = type;
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
            if (i != j && _r[i][j] == 0 && (j == 0 || intIn(_r[j], 1))  // not reflexive/forbidden/symmetric + connected
                    && _a[i].getAttribute() != _a[j].getAttribute()  // arguments of the same attribute cannot attack each other
                    //&& !intIn(_r[i], 1)  // limit to one attack per argument
                    && (_r[i][0] == 0)  // an argument attacking the target cannot attack something else
                    ) {
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
            if (i == j || i == 0 || i == 1 ||
                    _a[i].getAttribute() == _a[j].getAttribute()) {  // attack impossible if reflexive or from label or negation
                if (i == 1 && j == 0) {
                    row.push_back(0);
                } else {
                    row.push_back(-1);
                }
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
    // std::vector<AttackPtr> attacks = af->getAttacks();
    // for (int i = 0; i < attacks.size(); ++i) {
    //     std::cout << std::get<0>(attacks[i])->getName() << " " << std::get<1>(attacks[i])->getName() << std::endl;
    // }
    // std::cout << "A size: " << af->getArguments().size() << " | R size: " << af->getAttacks().size() << std::endl;
    af->printAttacks();
    delete af;
}

AF::AF() {
    _a = std::vector<Argument>();
    _r = std::vector<AttackPtr>();
    _s = std::vector<AttackPtr>();
}

AF::~AF() {
    _a.clear();
    _r.clear();
    _s.clear();
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

std::vector<AttackPtr> AF::getSupports() const {
    return _s;
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

std::vector<Argument*> AF::getInSupporters(const Argument & a) {
    std::vector<Argument*> inSupports;
    for (int i = 0; i < _s.size(); ++i) {
        if (*std::get<1>(_s[i]) == a) {
            inSupports.push_back(std::get<0>(_s[i]));
        }
    }
    return inSupports;
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

std::vector<Argument*> AF::getOutSupporters(const Argument & a) {
    std::vector<Argument*> outSupports;
    for (int i = 0; i < _s.size(); ++i) {
        if (*std::get<0>(_s[i]) == a) {
            outSupports.push_back(std::get<1>(_s[i]));
        }
    }
    return outSupports;
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

void AF::addSupport(const AttackPtr & r) {
    _s.push_back(r);
}

void AF::addSupport(const Argument & a1, const Argument & a2) {
    Argument * a1Ptr = getArgumentByName(a1.getName());
    Argument * a2Ptr = getArgumentByName(a2.getName());
    if (a1Ptr != nullptr && a2Ptr != nullptr) {
        addSupport(std::make_tuple(a1Ptr, a2Ptr));
    }
}

void AF::addSupport(const std::string & name1, const std::string & name2) {
    Argument * a1 = getArgumentByName(name1);
    Argument * a2 = getArgumentByName(name2);
    if (a1 != nullptr && a2 != nullptr) {
        addSupport(std::make_tuple(a1, a2));
    }
}

void AF::updateAliveness(const std::vector<Fact> & facts) {
    for (int i = 0; i < _a.size(); ++i) {
        if (_a[i].isLabel() || _a[i].isNegation()) {
            _a[i].setUndec();
        } else {
            _a[i].setOut();
            if (_a[i].getName()[0] == '!') {
                _a[i].setUndec();
            }
            for (int j = 0; j < facts.size(); ++j) {
                std::string name = _a[i].getName();
                if (name[0] == '!') name = name.substr(1, name.size() - 1);
                if (name == facts[j]) {
                    _a[i].setUndec();
                    if (_a[i].getName()[0] == '!') {
                        _a[i].setOut();
                    }
                    break;
                }
            }
        }
    }
}

bool AF::predict(const std::vector<Fact> & facts, const std::string & target) {
    using namespace std::chrono;
    high_resolution_clock::time_point timepoint = high_resolution_clock::now();
    updateAliveness(facts);
    //std::cout << "updateAliveness() = " << duration_cast<nanoseconds>(high_resolution_clock::now() - timepoint).count() / 1000.0 << std::endl;
    timepoint = high_resolution_clock::now();
    //computeExtension();
    computeBipolarExtension();
    //std::cout << "computeExtension() = " << duration_cast<nanoseconds>(high_resolution_clock::now() - timepoint).count() / 1000.0 << std::endl;
    timepoint = high_resolution_clock::now();
    bool result = targetAlive(target);
    //std::cout << "targetAlive() = " << duration_cast<nanoseconds>(high_resolution_clock::now() - timepoint).count() / 1000.0 << std::endl;

    return result;
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
    if (_s.size() > 0) { // print supports if any
        for (int i = 0; i < _s.size(); ++i) {
            std::cout << std::get<0>(_s[i])->getName() << " " << std::get<1>(_s[i])->getName() << " +" << std::endl;
        }
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

void AF::computeBipolarExtension(const Fact & target) {
    
    Argument * root = getRootTempInSupArgument();
    std::vector<Argument> extension;

    while (root != nullptr) {

        if (root->tempInSup()) {
            root->setInSup();
        } else {
            root->setIn();
        }
        extension.push_back(*root);
        std::vector<Argument*> attacked = getOutAttackers(*root);
        for (int i = 0; i < attacked.size(); ++i) {
            if (!attacked[i]->inSup() && !attacked[i]->tempInSup()) {
                attacked[i]->setOut();
            }
        }
        std::vector<Argument*> supported = getOutSupporters(*root);
        for (int i = 0; i < supported.size(); ++i) {
            supported[i]->setTempInSup();
        }
        root = getRootArgument();
    }
    // convert all IN-SUP to IN
    for (int i = 0; i < _a.size(); ++i) {
        if (_a[i].inSup() || _a[i].tempInSup()) {
            _a[i].setIn();
        }
    }
}

void AF::printArgumentStatus() const {
    std::cout << "Argument status:" << std::endl;
    for (int i = 0; i < _a.size(); ++i) {
        std::cout << _a[i].getName() << ": ";
        if (_a[i].in()) {
            std::cout << "IN";
        } else if (_a[i].inSup()) {
            std::cout << "IN-SUP";
        } else if (_a[i].tempInSup()) {
            std::cout << "TEMP-IN-SUP";
        } else if (_a[i].out()) {
            std::cout << "OUT";
        } else if (_a[i].undec()) {
            std::cout << "UNDEC";
        }
        std::cout << std::endl;
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

Argument * AF::getRootTempInSupArgument() {
    for (int i = 0; i < _a.size(); ++i) {
        if (isTempInSupRoot(_a[i])) {
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

bool AF::isTempInSupRoot(const Argument & a) {
    /*
    Is a root if all attackers are dead and node _status is 4 (i.e., TEMP-IN-SUP).
    */
    std::vector<Argument*> inAttacks = getInAttackers(a);
    if (a.tempInSup()) return true;
    if (!a.undec()) return false;
    for (int i = 0; i < inAttacks.size(); ++i) {
        if (!inAttacks[i]->out()) {
            return false;
        }
    }
    return true;
}