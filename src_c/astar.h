#pragma once
#include "dataset.h"
#include "node.h"


class AStar {

    public:
        AStar();
        ~AStar();

        Node run(int maxIterations = -1);  // -1: no limit
        void setData(Dataset * dataset);


    private:
        std::vector<Node> _queue;
        Dataset * _dataset;  // pointer to the dataset

        std::vector<Node> getNeighbors(const Node & node);
        void addNodeToQueue(Node & node);
        Node * getNextNode();
        Node * getBestNode();

};
