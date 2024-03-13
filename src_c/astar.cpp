#include "AStar.h"


AStar::AStar() {
    _queue = std::vector<Node>();
    _dataset = nullptr;
    _maxRsize = 3;
}

AStar::~AStar() {
    _queue.clear();
}

Node AStar::run(int maxIterations) {
    int iterations = 0;
    int distance = -1;
    addStartNodeToQueue();
    std::vector<std::string> visitedHashes;

    while (iterations != maxIterations) {
        Node * node = getNextNode();
        distance = (node->getDistance() < distance) || distance == -1? node->getDistance() : distance;
        if (iterations % 100 == 0 && iterations > 0) {
            std::cout << "It: " << iterations << " - Best distance: " << distance << std::endl;
            std::cout << _queue.size() << std::endl;
            //node->print();
        }
        if (node == nullptr || node->getDistance() < 1) { // break if reached 0% errors or explored everything
            break;
        }
        std::vector<Node> neighbors = getNeighbors(*node);
        int added = 0;
        for (int i = 0; i < neighbors.size(); ++i) {
            std::string hash = neighbors[i].getValue()->getHash();
            if (!strIn(visitedHashes, hash)) {
                addNodeToQueue(neighbors[i]);
                ++added;
                visitedHashes.push_back(hash);
            }
        }
        std::cout << added << " added" << std::endl;
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
    int bestNodeIndex = -1;
    std::cout << "vvvvvvvvvvvvv" << std::endl;
    for (int i = 0; i < _queue.size(); ++i) {
        if (_queue[i].getColor() == 1 && (false || _queue[i].getAttackSize() <= _maxRsize)) {  // grey
            if (bestNode == nullptr || bestNode->getDistance() == -1 ||
                    _queue[i].getDistance() < bestNode->getDistance()) {
                if (_queue[i].getDistance() != -1) {
                    bestNode = &_queue[i];
                    bestNodeIndex = i;
                }
            }
            std::cout << _queue[i].getValue()->getHash() << std::endl;
        }
    }
    if (bestNodeIndex != -1) {
        _queue[bestNodeIndex].setColor(2);  // black
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

void AStar::addStartNodeToQueue() {
    Node startNode = Node(0, _dataset, new EncodedAF(_dataset->getArguments()));
    startNode.setColor(1);  // grey
    _queue.push_back(startNode);
}

void AStar::isDatasetNullptr() {
    if (_dataset == nullptr) std::cout << "null" << std::endl;
    else std::cout << "not null" << std::endl;
}