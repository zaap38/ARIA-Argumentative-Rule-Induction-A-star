#pragma once
#include "astar.cpp"
#include "dataset.h"
#include "node.h"


class AStar {

    public:
        AStar();
        ~AStar();

        void run(int maxIterations = -1);  // -1: no limit
        void setData(const dataset::Dataset * dataset);


    private:
        std::vector<Node> _queue;
        dataset::Dataset * _dataset;  // pointer to the dataset

        std::vector<Node> getNeighbors(const Node & node);
        void addNodeToQueue(Node & node);
        Node * getNextNode() const;
        Node * getBestNode() const;

};
