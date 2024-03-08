#include "dataset.h"


Dataset::Dataset() {
    _delim = ',';
}

Dataset::~Dataset() {

}

void Dataset::load(const std::string & filename) {
    std::ifstream
    file(filename);
    std::string line;

    _arguments.clear();
    _data.clear();
    std::vector<std::string> argumentNames;

    while (std::getline(file, line)) {

        std::vector<std::string> elements = splitStr(line, _delim);
        std::vector<std::string> facts;
        std::string label;

        for (int i = 0; i < elements.size(); ++i) {

            if (i == _labelIndex) {
                label = elements[i];
            } else if (!intIn(_ignoredIndexes, i)) {

                std::string value = elements[i];
                std::string attribute = _attributes[i];
                std::string full = attribute + "=" + value;

                if (!strIn(argumentNames, elements[i])) {  // incorrect type
                    Argument a;
                    a.setAttribute(attribute);  // to add based on index i
                    a.setValue(value);
                    _arguments.push_back(a);
                    argumentNames.push_back(full);
                }
                facts.push_back(full);
            }
        }
    }
}

std::tuple<Dataset, Dataset> Dataset::split(double ratio) const {
    Dataset train;
    Dataset test;

    int trainSize = _data.size() * ratio;
    int testSize = _data.size() - trainSize;

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

void Data::addFact(const std::string & fact) {
    _facts.push_back(fact);
}

void Data::setLabel(const std::string & label) {
    _label = label;
}

const std::vector<std::string> & Data::getFacts() const {
    return _facts;
}

const std::string & Data::getLabel() const {
    return _label;
}
