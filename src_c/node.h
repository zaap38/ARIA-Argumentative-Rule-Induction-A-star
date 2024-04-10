#pragma once
#include "af.h"
#include <vector>
#include "dataset.h"
#include <string>
#include <random>
#include <typeinfo>
#include <thread>
#include <future>
#include <chrono>
#include <mutex>


class Node {

    public:
        Node();
        Node(int id);
        Node(int id, Dataset * dataset, EncodedAF * value);
        Node(const Node & node);
        ~Node();

        float getDistance(bool ignoreRSize = false);
        float getAccuracy(int precision = 0);
        int getColor() const;
        EncodedAF * getValue() const;

        void setColor(int color);
        void setPredecessor(int predecessor);
        int getAttackSize() const;
        std::vector<Node> getNeighbors() const;
        void print(const std::string & prefix = "") const;
        std::string getLabelAttribute() const;

        void setDataset(Dataset * dataset);
        bool changes();

        void printArguments() const;

    private:
        int _id;
        EncodedAF * _value;
        int _color;  // 0: white; 1: grey; 2: black
        float _distance;  // -1 means not initialized
        float _predDistance;  // predecessor distance
        int _predecessor;  // predecessor id
        std::vector<Node> _neighbors;
        Dataset * _dataset;  // pointer to the dataset

        std::mutex _lock; // Mutex for synchronizing cout
        int _sharedIndex;
        
        void computeDistance(bool ignoreRSize = false);
        int runOnDataset(int offset, int coreCount);

};