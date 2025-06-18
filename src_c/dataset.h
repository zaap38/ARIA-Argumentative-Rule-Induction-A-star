#pragma once
#include <string>
#include <vector>
#include <tuple>
#include <fstream>
#include "argument.h"
#include "snippets.h"
#include <random>
#include <algorithm>
#include <iostream>
#include <map>


typedef std::map<std::string, std::tuple<float, float>> Ranges;

class Data {

    public:
        Data();
        ~Data();

        void addFact(const std::string & fact);
        void setFacts(const std::vector<std::string> & facts);
        void setLabel(bool label);
        const std::vector<std::string> & getFacts() const;
        bool getLabel() const;

    private:
        std::vector<std::string> _facts;
        bool _label;

};


class Dataset {

    public:
        Dataset();
        ~Dataset();

        void load(const std::string & src,
                  const std::string & labelValue,
                  int labelIndex = -1,
                  const std::vector<int> & floatingValues = {},
                  const std::vector<int> & ignoredIndexes = {});
        std::tuple<Dataset, Dataset> split(double ratio = 0.7);  // ratio: train%, (1 - ratio): test%
        int size() const;
        Data & operator[](int i);
        Data & get(int i);
        void addAttribute(const std::string & attribute);
        void setAttributes(const std::vector<std::string> & attributes);
        void shuffle();
        void balance(float minRatio = 0.3);
        void setLabelIndex(int index);
        void setDelim(char delim);
        void addIgnoredIndex(int index);
        std::vector<Argument> getArguments() const;
        std::string getLabelAttribute() const;
        void setLabelAttribute(const std::string & labelAttribute);
        void setSeed(int seed);
        void randomizeSeed();
        void setSamplingInterval(float interval);

        void loadBalloons();
        void loadCar();
        void loadCarBB();
        void loadTestBipolar();
        void loadMushroom();
        void loadVoting();
        void loadBreastCancer();
        void loadFake();
        void loadHeartDisease();
        void loadHeartDiseaseBB();
        void loadBreastCancerWisconsin();
        void loadIris();
        void loadMoralMachine();
        void loadMoralMachineExt();
        void loadMoralMachineBBTest();
        void loadMoralMachineComplete();
        void loadMoralMachineCompleteBB();
        void loadAnnotatedMM();
        void loadWine();
        void loadThyroid();

    private:
        int _labelIndex;
        std::string _labelAttribute;
        std::string _negation;
        char _delim;
        float _samplingInterval;
        int _seed;
        std::vector<int> _ignoredIndexes;
        std::vector<Argument> _arguments;
        std::vector<Data> _data;
        std::vector<std::string> _attributes;

        Ranges getRanges(const std::string & filename,
                         const std::vector<int> & floatingValues) const;
};