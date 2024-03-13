#include "dataset.h"


Dataset::Dataset() {
    _delim = ',';
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

void Dataset::load(const std::string & filename,
                   const std::string & labelValue,
                   int labelIndex,
                   const std::vector<int> & ignoredIndexes) {

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
            _labelAttribute = _attributes[_labelIndex];
        }

        for (size_t i = 0; i < elements.size(); ++i) {

            if (i == _labelIndex) {
                label = (elements[i] == labelValue)? true : false;
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
                        }
                    } else {
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

std::tuple<Dataset, Dataset> Dataset::split(double ratio) const {
    Dataset train;
    Dataset test;

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

void Dataset::shuffle() {
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(_data.begin(), _data.end(), g);
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
