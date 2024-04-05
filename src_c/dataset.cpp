#include "dataset.h"


Dataset::Dataset() {
    _delim = ',';
    std::random_device rd;
    _seed = rd();
    _negation = "!";  // default negation
}

Dataset::~Dataset() {

}

void Dataset::loadBalloons() {
    setAttributes({"color", "size", "act", "age", "inflated"});  // set attributes
    load("../src/datasets/balloons/yellow-small+adult-stretch.data.txt", "T");  // load data
}

void Dataset::loadCar() {
    setAttributes({"buying", "maint", "doors", "persons", "lug_boot", "safety", "acceptability"});  // set attributes
    load("../src/datasets/car/car.data.txt", "vgood");  // load data
}

void Dataset::loadMushroom() {
    setAttributes({"class", "cap-shape", "cap-surface", "cap-color", "bruises", "odor", "gill-attachment",
                    "gill-spacing", "gill-size", "gill-color", "stalk-shape", "stalk-root",
                    "stalk-surface-above-ring", "stalk-surface-below-ring", "stalk-color-above-ring",
                    "stalk-color-below-ring", "veil-type", "veil-color", "ring-number", "ring-type",
                    "spore-print-color", "population", "habitat"});  // set attributes
    load("../src/datasets/mushroom/agaricus-lepiota.data.txt", "e", 0);  // load data
}

void Dataset::loadBreastCancer() {
    setAttributes({"class", "age", "menopause", "tumor-size", "inv-nodes", "node-caps", "deg-malign",
                "breast", "breast-quad", "irradiat"});  // set attributes
    load("../src/datasets/breast-cancer/breast-cancer.data.txt", "recurrence-events", 0);  // load data
}

void Dataset::loadVoting() {
    setAttributes({"party", "handicapped-infants", "water-project-cost-sharing", "adoption-of-the-budget-resolution",
                    "physician-fee-freeze", "el-salvador-aid", "religious-groups-in-schools", "anti-satellite-test-ban",
                    "aid-to-nicaraguan-contras", "mx-missile", "immigration", "synfuels-corporation-cutback", "education-spending",
                    "superfund-right-to-sue", "crime", "duty-free-exports", "export-administration-act-south-africa"});  // set attributes
    load("../src/datasets/voting/house-votes-84.data.txt", "republican", 0);  // load data
}

void Dataset::loadHeartDisease() {
    setAttributes({"age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach",
                    "exang", "oldpeak", "slope", "ca", "thal", "class"});  // set attributes
    load("../src/datasets/heart-disease/processed.cleveland.data.txt", "0", -1, {}, true);  // load data
}

void Dataset::loadFake() {
    setAttributes({"a", "b", "c", "label"});  // set attributes
    load("../src/datasets/fake/fake.data.txt", "T");  // load data

}

void Dataset::load(const std::string & filename,
                   const std::string & labelValue,
                   int labelIndex,
                   const std::vector<int> & ignoredIndexes,
                   bool sampling) {

    std::ifstream file(filename);
    std::string line;

    _arguments.clear();
    _data.clear();
    std::vector<std::string> argumentNames;
    while (std::getline(file, line)) {
        std::vector<std::string> elements = splitStr(line, _delim);
        std::vector<std::string> facts;
        bool label;
        _labelIndex = labelIndex;
        if (_labelIndex == -1) {
            _labelIndex = elements.size() - 1;
        }
        _labelAttribute = _attributes[_labelIndex];

        for (size_t i = 0; i < elements.size(); ++i) {

            if (i == _labelIndex) {
                label = (elements[i] == labelValue)? true: false;
            }
            
            if (!intIn(_ignoredIndexes, i)) {

                std::string value = elements[i];
                std::string attribute = _attributes[i];
                std::string full = attribute + "=" + value;
                if (!strIn(argumentNames, full)) {  // incorrect type
                    Argument a;
                    a.setAttribute(attribute);  // to add based on index i
                    a.setValue(value);
                    if (i == _labelIndex) {
                        if (value == labelValue) {
                            a.setIsLabel(true);
                            _arguments.insert(_arguments.begin(), a);
                            argumentNames.push_back(full);
                            Argument neg;
                            neg.setAttribute(_negation);
                            neg.setValue(full);
                            neg.setIsNegation(true);
                            argumentNames.push_back(neg.getName());
                            _arguments.insert(_arguments.begin() + 1, neg);
                        }
                    } else if (value != "?") {
                        _arguments.push_back(a);
                        argumentNames.push_back(full);
                    }
                }
                if (i != _labelIndex) {
                    facts.push_back(full);
                }
            }
        }
        Data dataline;
        dataline.setFacts(facts);
        dataline.setLabel(label);
        _data.push_back(dataline);
    }
}

void Dataset::setLabelAttribute(const std::string & labelAttribute) {
    _labelAttribute = labelAttribute;
}

void Dataset::setAttributes(const std::vector<std::string> & attributes) {
    _attributes = attributes;
}

std::string Dataset::getLabelAttribute() const {
    return _labelAttribute;
}

void Dataset::setSeed(int seed) {
    _seed = seed;
}

void Dataset::randomizeSeed() {
    std::random_device rd;
    _seed = rd();
}

void Dataset::shuffle() {
    std::random_device rd;
    std::mt19937 g(_seed);
    std::shuffle(_data.begin(), _data.end(), g);
}

void Dataset::balance(float minRatio) {
    std::vector<Data> newData = _data;
    int positive = 0;
    int negative = 0;
    for (int i = 0; i < _data.size(); ++i) {
        if (_data[i].getLabel()) {
            ++positive;
        } else {
            ++negative;
        }
    }
    int total = positive + negative;
    while (positive < total * minRatio || negative < total * minRatio) {
        int randIndex = rand() % newData.size();
        if (positive < negative) {
            if (newData[randIndex].getLabel()) {
                newData.push_back(newData[randIndex]);
                ++positive;
            }
        } else if (negative < positive) {
            if (!newData[randIndex].getLabel()) {
                newData.push_back(newData[randIndex]);
                ++negative;
            }
        }
        total = positive + negative;
    }
    
    _data = newData;
}

std::tuple<Dataset, Dataset> Dataset::split(double ratio) {
    Dataset train;
    Dataset test;

    shuffle();

    train._arguments = _arguments;
    test._arguments = _arguments;

    int trainSize = _data.size() * ratio;

    for (int i = 0; i < trainSize; ++i) {
        train._data.push_back(_data[i]);
    }
    for (int i = trainSize; i < _data.size(); ++i) {
        test._data.push_back(_data[i]);
    }

    return std::make_tuple(train, test);
}

int Dataset::size() const {
    return _data.size();
}

Data & Dataset::operator[](int i) {
    return get(i);
}

Data & Dataset::get(int i) {
    return _data[i];
}

void Dataset::addAttribute(const std::string & attribute) {
    _attributes.push_back(attribute);
}

void Dataset::setLabelIndex(int index) {
    _labelIndex = index;
}

void Dataset::setDelim(char delim) {
    _delim = delim;
}

void Dataset::addIgnoredIndex(int index) {
    _ignoredIndexes.push_back(index);
}

Data::Data() {

}

Data::~Data() {

}

void Data::setFacts(const std::vector<std::string> & facts) {
    _facts = facts;
}

void Data::addFact(const std::string & fact) {
    _facts.push_back(fact);
}

void Data::setLabel(bool label) {
    _label = label;
}

const std::vector<std::string> & Data::getFacts() const {
    return _facts;
}

bool Data::getLabel() const {
    return _label;
}

std::vector<Argument> Dataset::getArguments() const {
    return _arguments;
}
