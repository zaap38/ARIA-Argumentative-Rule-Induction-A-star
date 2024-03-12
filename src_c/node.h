#pragma once
#include "af.h"
#include <vector>
#include "dataset.h"
#include <string>
#include <random>


class Node {

    public:
        Node();
        Node(int id);
        Node(int id, Dataset * dataset, EncodedAF * value);
        Node(const Node & node);
        ~Node();

        float getDistance(bool ignoreRSize = false);
        int getColor() const;
        EncodedAF * getValue() const;

        void setColor(int color);
        void setPredecessor(int predecessor);
        std::vector<Node> getNeighbors() const;
        void print() const;

    private:
        int _id;
        EncodedAF * _value;
        int _color;  // 0: white; 1: grey; 2: black
        int _distance;  // -1 means not initialized
        int _predecessor;  // predecessor id
        std::vector<Node> _neighbors;
        Dataset * _dataset;  // pointer to the dataset
        
        void computeDistance(bool ignoreRSize = false);

};