#pragma once
#include <string>
#include <vector>
#include <tuple>
#include <fstream>
#include "argument.h"
#include "snippets.h"


class Data {

    public:
        Data();
        ~Data();

        void addFact(const std::string & fact);
        void setLabel(const std::string & label);
        const std::vector<std::string> & getFacts() const;
        const std::string & getLabel() const;

    private:
        std::vector<std::string> _facts;
        std::string _label;

};


class Dataset {

    public:
        Dataset();
        ~Dataset();

        void load(const std::string & src);
        std::tuple<Dataset, Dataset> split(double ratio = 0.7) const;  // ratio: train%, (1 - ratio): test%
        int size() const;
        Data & operator[](int i);
        Data & get(int i);
        void addAttribute(const std::string & attribute);

    private:
        int _labelIndex;
        char _delim;
        std::vector<int> _ignoredIndexes;
        std::vector<Argument> _arguments;
        std::vector<Data> _data;
        std::vector<std::string> _attributes;
};