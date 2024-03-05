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