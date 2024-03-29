#pragma once
#include "dataset.h"
#include "node.h"
#include <vector>
#include <iostream>
#include "snippets.h"
#include <chrono>
#include <thread>
#include <future>


class AStar {

    public:
        AStar();
        ~AStar();

        Node run(int maxIterations = -1);  // -1: no limit
        void setData(Dataset * dataset);
        void setTestData(Dataset * test);  // set test dataset (for validation
        void isDatasetNullptr();
        void setMaxRsize(int maxRsize);


    private:
        std::vector<Node> _queue;
        Dataset * _dataset;  // pointer to the dataset
        Dataset * _testDataset;  // pointer to the test dataset
        int _maxRsize;

        std::vector<Node> getNeighbors(const Node & node);
        void addStartNodeToQueue();
        void addNodeToQueue(Node & node);
        Node * getNextNode();
        std::tuple<Node*, int> runOnQueue(int offset, int coreCount);
        Node * getBestNode();

};
