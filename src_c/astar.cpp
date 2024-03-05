#include "AStar.h"


AStar::AStar() {
    _queue = std::vector<Node>();
    _dataset = nullptr;
}

AStar::~AStar() {
    _queue.clear();
}

Node AStar::run(int maxIterations) {
    int iterations = 0;
    while (iterations != maxIterations) {
        Node * node = getNextNode();
        if (node == nullptr || node->getDistance() < 1) { // break if reached 0% errors or explored everything
            break;
        }
        std::vector<Node> neighbors = getNeighbors(*node);
        for (int i = 0; i < neighbors.size(); ++i) {
            addNodeToQueue(neighbors[i]);
        }
        ++iterations;
    }
    return *getBestNode();
}

std::vector<Node> AStar::getNeighbors(const Node & node) {
    std::vector<Node> neighbors = node.getNeighbors();
    return neighbors;
}

void AStar::addNodeToQueue(Node & node) {
    if (node.getColor() == 0) {  // add only white nodes
        node.setColor(1);  // become grey
        _queue.push_back(node);  // add to queue
    }
}

Node * AStar::getNextNode() {
    Node * bestNode = nullptr; // Declare the variable bestNode
    
    for (int i = 0; i < _queue.size(); ++i) {
        if (_queue[i].getColor() == 1) {  // grey
            if (bestNode == nullptr || _queue[i].getDistance() < bestNode->getDistance()) {
                bestNode = &_queue[i];
            }
        }
    }

    return bestNode;
}

Node * AStar::getBestNode() {
    Node * bestNode = nullptr; // Declare the variable bestNode
    
    for (int i = 0; i < _queue.size(); ++i) {
        if (_queue[i].getColor() == 1) {  // grey
            if (bestNode == nullptr || _queue[i].getDistance() < bestNode->getDistance()) {
                bestNode = &_queue[i];
            }
        }
    }

    return bestNode;
}

void AStar::setData(Dataset * dataset) {
    _dataset = dataset;
}