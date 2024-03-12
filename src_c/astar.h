#pragma once
#include "dataset.h"
#include "node.h"
#include <vector>
#include <iostream>
#include "snippets.h"


class AStar {

    public:
        AStar();
        ~AStar();

        Node run(int maxIterations = -1);  // -1: no limit
        void setData(Dataset * dataset);
        void isDatasetNullptr();


    private:
        std::vector<Node> _queue;
        Dataset * _dataset;  // pointer to the dataset

        std::vector<Node> getNeighbors(const Node & node);
        void addStartNodeToQueue();
        void addNodeToQueue(Node & node);
        Node * getNextNode();
        Node * getBestNode();

};
