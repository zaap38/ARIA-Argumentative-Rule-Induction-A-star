#include "dataset.h"


Dataset::Dataset() {
    _delim = ',';
    std::random_device rd;
    _seed = rd();
    _negation = "!";  // default negation
    _samplingInterval = 5;  // default sampling interval
}

Dataset::~Dataset() {

}

void Dataset::loadBalloons() {
    setAttributes({"color", "size", "act", "age", "inflated"});  // set attributes
    load("./datasets/balloons/yellow-small+adult-stretch.data.txt", "T");  // load data
}

void Dataset::loadCar() {
    setAttributes({"buying", "maint", "doors", "persons", "lug_boot", "safety", "acceptability"});  // set attributes
    load("./datasets/car/car.data.txt", "vgood");  // load data
}

void Dataset::loadMushroom() {
    setAttributes({"class", "cap-shape", "cap-surface", "cap-color", "bruises", "odor", "gill-attachment",
                    "gill-spacing", "gill-size", "gill-color", "stalk-shape", "stalk-root",
                    "stalk-surface-above-ring", "stalk-surface-below-ring", "stalk-color-above-ring",
                    "stalk-color-below-ring", "veil-type", "veil-color", "ring-number", "ring-type",
                    "spore-print-color", "population", "habitat"});  // set attributes
    load("./datasets/mushroom/agaricus-lepiota.data.txt", "e", 0);  // load data
}

void Dataset::loadBreastCancer() {
    setAttributes({"class", "age", "menopause", "tumor-size", "inv-nodes", "node-caps", "deg-malign",
                "breast", "breast-quad", "irradiat"});  // set attributes
    load("./datasets/breast-cancer/breast-cancer.data.txt", "recurrence-events", 0);  // load data
}

/*
XGboost: 92.7
SVM: 92.7
Random Forest: 93.6
NN: 96.3
Logistic: 93.6
*/
void Dataset::loadVoting() {
    setAttributes({"party", "handicapped-infants", "water-project-cost-sharing", "adoption-of-the-budget-resolution",
                    "physician-fee-freeze", "el-salvador-aid", "religious-groups-in-schools", "anti-satellite-test-ban",
                    "aid-to-nicaraguan-contras", "mx-missile", "immigration", "synfuels-corporation-cutback", "education-spending",
                    "superfund-right-to-sue", "crime", "duty-free-exports", "export-administration-act-south-africa"});  // set attributes
    load("./datasets/voting/house-votes-84.data.txt", "republican", 0);  // load data
}

/*
XGboost: 97.2
SVM: 94.4
Random Forest: 97.9
NN: 92.3
Logistic: 95.8
*/
void Dataset::loadBreastCancerWisconsin() {
    setAttributes({"id", "clump-thickness", "uniformity-of-cell-size", "uniformity-of-cell-shape",
                    "marginal-adhesion", "single-epithelial-cell-size", "bare-nuclei", "bland-chromatin",
                    "normal-nucleoli", "mitoses", "class"});  // set attributes
    load("./datasets/breast-cancer-wisconsin/breast-cancer-wisconsin.data.txt", "4", 10,
        {1, 2, 3, 4, 5, 6, 7, 8, 9}, {0});  // load data
}

/*
XGboost: 81.6
SVM: 65.8
Random Forest: 80.3
NN: 78.9
Logistic: 81.6
*/
void Dataset::loadHeartDisease() {
    setAttributes({"age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach",
                    "exang", "oldpeak", "slope", "ca", "thal", "class"});  // set attributes
    load("./datasets/heart-disease/processed.cleveland.data.txt", "0", -1,
        {0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12});  // load data
}

void Dataset::loadHeartDiseaseBB() {
    setAttributes({"age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach",
                    "exang", "oldpeak", "slope", "ca", "thal", "class"});  // set attributes
    load("./datasets/heart-disease/bb_hdc.txt", "T", -1,
        {0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12});  // load data
}

void Dataset::loadTestBipolar() {
    setAttributes({"a", "b", "x", "class"});  // set attributes
    //load("./datasets/test-bipolar/test-bipolar.txt", "1");  // load data
    load("./datasets/test-bipolar/test-bipolar-nozero.txt", "1");  // load data
}

/*
XGboost: 92.1
SVM: 94.7
Random Forest: 89.5
NN: 97.4
Logistic: 94.7
*/
void Dataset::loadIris() {
    setAttributes({"sepal-length", "sepal-width", "petal-length", "petal-width", "class"});  // set attributes
    load("./datasets/iris/iris.data", "Iris-virginica", 4,
    {0, 1, 2, 3});  // load data
}

void Dataset::loadFake() {
    setAttributes({"a", "b", "c", "label"});  // set attributes
    load("./datasets/fake/fake.data.txt", "T");  // load data
}

void Dataset::loadMoralMachine() {
    setAttributes({"persons", "kids", "animals", "legal", "legal_alt", "saved"});
    load("./datasets/moral-machine/annotated_delta.csv", "yes");  // load data
}

void Dataset::loadMoralMachineExt() {
    setAttributes({"persons", "kids", "animals", "criminals", "pregnants", "legal", "legal_alt", "saved"});  // set attributes
    load("./datasets/moral-machine/mm_delta_2000_ext.csv", "yes");  // load data
}

void Dataset::loadMoralMachineBBTest() {
    setAttributes({"persons", "kids", "animals", "criminals", "pregnants", "legal", "legal_alt", "saved"});  // set attributes
    load("./datasets/moral-machine/mm_predictions_test.csv", "yes");  // load data
}

void Dataset::loadMoralMachineComplete() {
    setAttributes({"person","person_alt","kid","kid_alt","animal","animal_alt","criminal","criminal_alt",
        "pregnant","pregnant_alt","legal","legal_alt","label"});  // set attributes
    load("./datasets/moral-machine/mm_delta_2000_complete.csv", "yes");  // load data
}

void Dataset::loadMoralMachineCompleteBB() {
    setAttributes({"person","person_alt","kid","kid_alt","animal","animal_alt","criminal","criminal_alt",
        "pregnant","pregnant_alt","legal","legal_alt","label"});  // set attributes
    load("./datasets/moral-machine/bb_mm_delta_2000_complete.csv", "true");  // load data
}

void Dataset::loadAnnotatedMM() {
    setAttributes({"person","person_alt","kid","kid_alt","animal","animal_alt","criminal","criminal_alt",
        "pregnant","pregnant_alt","legal","legal_alt","label"});  // set attributes
    load("./datasets/moral-machine/annotated.csv", "yes", -1, {0, 1, 2, 3, 4, 5, 6, 7, 8, 9});  // load data
}


/*
XGboost: 97.8
SVM: 80.0
Random Forest: 100.0
NN: 97.8
Logistic: 93.3
*/
void Dataset::loadWine() {
    setAttributes({"class", "alcohol", "malic-acid", "ash", "alcalinity-of-ash", "magnesium",
                    "total-phenols", "flavanoids", "nonflavanoid-phenols", "proanthocyanins",
                    "color-intensity", "hue", "od280/od315-of-diluted-wines", "proline"});  // set attributes
    load("./datasets/wine/wine.data", "1", 0, {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13});  // load data
}

/*
Literature accuracies (see https://link.springer.com/article/10.1007/s00405-023-08299-w):
KNN: 93.0
SVM: 96.0
Decision Tree: 96.0
Random Forest: 95.0
ANN: 96.0
*/
void Dataset::loadThyroid() {
    setAttributes({"Age", "Gender", "Smoking", "Hx Smoking", "Hx Radiothreapy", "Thyroid Function",
                "Physical Examination", "Adenopathy", "Pathology", "Focality", "Risk", "T", "N", "M",
                "Stage", "Response", "Recurred"});
    load("./datasets/thyroid/data.csv", "Yes", -1, {0});  // load data
}

void Dataset::load(const std::string & filename,
                   const std::string & labelValue,
                   int labelIndex,
                   const std::vector<int> & floatingValues,
                   const std::vector<int> & ignoredIndexes) {
    
    std::ifstream file(filename);
    std::string line;

    Ranges ranges = getRanges(filename, floatingValues);
    _arguments.clear();
    _data.clear();
    _labelIndex = labelIndex;
    _ignoredIndexes = ignoredIndexes;
    std::vector<std::string> argumentNames;
    while (std::getline(file, line)) {
        std::vector<std::string> elements = splitStr(line, _delim);
        std::vector<std::string> facts;
        bool label;
        if (_labelIndex == -1) {
            _labelIndex = elements.size() - 1;
        }
        _labelAttribute = _attributes[_labelIndex];

        for (size_t i = 0; i < elements.size(); ++i) {

            if (i == _labelIndex) {
                label = (elements[i] == labelValue)? true: false;
            }
            
            if (!intIn(_ignoredIndexes, i)) {

                std::string attribute = _attributes[i];
                std::string value = elements[i];

                // sampling of continuous attributes
                if (intIn(floatingValues, i) && value != "?" && value[0] != 0) {
                    float min = std::get<0>(ranges[attribute]);
                    float max = std::get<1>(ranges[attribute]);
                    float fvalue = std::stof(value);
                    float range = max - min;
                    float step = range / _samplingInterval;
                    int interval = (fvalue - min) / step;
                    double valMin = round(interval * step + min, 2);
                    double valMax = round((interval + 1) * step + min, 2);
                    value = trim(std::to_string(valMin)) + "-" + trim(std::to_string(valMax));
                }

                std::string full = attribute + "=" + value;
                if (!strIn(argumentNames, full)) {  // incorrect type
                    Argument a;
                    a.setAttribute(attribute);  // to add based on index i
                    a.setValue(value);
                    /*Argument neg_arg;
                    neg_arg.setAttribute(attribute);
                    neg_arg.setValue(value);*/
                    if (i == _labelIndex) {
                        if (value == labelValue) {
                            a.setIsLabel(true);
                            _arguments.insert(_arguments.begin(), a);
                            argumentNames.push_back(full);
                            Argument neg;  // LAMBDA ARGUMENT - do not remove
                            neg.setAttribute(_negation);
                            neg.setValue(full);
                            neg.setIsNegation(true);
                            argumentNames.push_back(neg.getName());
                            _arguments.insert(_arguments.begin() + 1, neg);
                        }
                    } else if (value != "?") {
                        _arguments.push_back(a);
                        argumentNames.push_back(full);
                        // Argument neg;
                        // neg.setAttribute('!' + attribute);
                        // neg.setValue(value);
                        // _arguments.push_back(neg);
                        // argumentNames.push_back(neg.getName());
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
    printVector(argumentNames);
}

Ranges Dataset::getRanges(const std::string & filename, const std::vector<int> & floatingValues) const {

    Ranges ranges;
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("File not found: " + filename);
    }
    std::string line;

    while (std::getline(file, line)) {

        std::vector<std::string> elements = splitStr(line, _delim);

        for (size_t i = 0; i < elements.size(); ++i) {

            if (intIn(floatingValues, i) && elements[i] != "?" && elements[i][0] != 0) {
                std::string attribute = _attributes[i];
                float value = std::stof(elements[i]);

                if (ranges.find(attribute) == ranges.end()) {
                    ranges.insert(std::make_pair(attribute, std::make_tuple(value, value)));
                } else {
                    float min = std::get<0>(ranges[attribute]);
                    float max = std::get<1>(ranges[attribute]);

                    if (value < min) {
                        min = value;
                    } else if (value > max) {
                        max = value;
                    }

                    ranges[attribute] = std::make_tuple(min, max);
                }
            }
        }
    }

    return ranges;
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

void Dataset::setSamplingInterval(float interval) {
    _samplingInterval = interval;
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