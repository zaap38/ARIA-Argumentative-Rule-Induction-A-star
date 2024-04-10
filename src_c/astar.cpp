#include "AStar.h"


AStar::AStar() {
    _queue = std::vector<Node>();
    _dataset = nullptr;
    _maxRsize = 1000;
}

AStar::~AStar() {
    _queue.clear();
}

void AStar::setMaxRsize(int maxRsize) {
    _maxRsize = maxRsize;
}

Node AStar::run(int maxIterations) {
    int iterations = 0;
    int distance = -1;
    addStartNodeToQueue();
    std::vector<std::string> visitedHashes;

    using namespace std::chrono;

    high_resolution_clock::time_point startTime = high_resolution_clock::now();
    high_resolution_clock::time_point time = high_resolution_clock::now();

    while (iterations != maxIterations) {
        std::cout << "vvvvv" << std::endl;
        time = high_resolution_clock::now();
        Node * node = getNextNode();
        //std::cout << "getNextNode() = " << duration_cast<milliseconds>(high_resolution_clock::now() - time).count() << std::endl;
        time = high_resolution_clock::now();
        if (node == nullptr || node->getDistance() < 1) { // break if reached 0% errors or explored everything
            std::string reason = node == nullptr? "No more nodes" : "Reached 0 errors";
            std::cout << "Break! Reason: " << reason << std::endl;
            break;
        }
        distance = (node->getDistance() < distance) || distance == -1? node->getDistance() : distance;
        if (true && iterations % 1 == 0 && iterations > 0) {
            std::cout << "It: " << iterations << " - " <<
                duration_cast<milliseconds>(time - startTime).count() / 1000.0 << "s" << std::endl;
            Node copyBestNode = *getBestNode();
            float accTrain = copyBestNode.getAccuracy(1);
            copyBestNode.setDataset(_testDataset);
            float accTest = copyBestNode.getAccuracy(1);
            std::cout << "Train: " << accTrain << "% - Test: " << accTest << "%" << std::endl;
            //std::cout << "It: " << iterations << " - Best distance: " << distance << " - Data: " << _dataset->size() << std::endl;
            std::cout << "Rsize: " << node->getAttackSize() << std::endl;
            //node->printArguments();
            //node->print();
            //node->getValue()->printMatrix();

        }
        
        std::vector<Node> neighbors = getNeighbors(*node);

        int added = 0;
        for (int i = 0; i < neighbors.size(); ++i) {
            std::string hash = neighbors[i].getValue()->getHash("run");
            if (!strIn(visitedHashes, hash)) {
                addNodeToQueue(neighbors[i]);
                ++added;
                visitedHashes.push_back(hash);
            }
        }
        //std::cout << added << " added" << std::endl;
        ++iterations;
    }
    if (iterations == maxIterations) {
        std::cout << "Max iterations reached" << std::endl;
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

std::tuple<Node*, int> AStar::runOnQueue(int offset, int coreCount) {
    Node * bestNode = nullptr; // Declare the variable bestNode
    int bestNodeIndex = -1;
    //int candidateCount = 0;
    for (int i = offset; i < _queue.size(); i += coreCount) {

        if (_queue[i].getColor() == 1 &&  // grey node
            _queue[i].changes() &&  // branch is having an impact
            (_queue[i].getAttackSize() <= _maxRsize)) {
            //++candidateCount;

            if (bestNode == nullptr || _queue[i].getDistance() < bestNode->getDistance()) {
                bestNode = &_queue[i];
                bestNodeIndex = i;
            }

        }
    }
    //std::cout << "Candidate count: " << candidateCount << std::endl;
    return std::make_tuple(bestNode, bestNodeIndex);
}

Node * AStar::getNextNode() {

    // MULTI-THREADING
    //const auto processor_count = std::thread::hardware_concurrency();
    // multi-threading useless because we already split proc for data eval
    const auto processor_count = 1;
    using namespace std::chrono;
    high_resolution_clock::time_point time = high_resolution_clock::now();

    std::vector<std::future<std::tuple<Node*, int>>> bestNodes;
    for (int i = 0; i < processor_count; ++i) {
        bestNodes.push_back(std::async(&AStar::runOnQueue, this, i, processor_count));
    }
    Node * bestNode = nullptr;
    int bestNodeIndex = -1;
    for (int i = 0; i < processor_count; ++i) {
        std::tuple<Node*, int> best = bestNodes[i].get();
        Node * candidate = std::get<0>(best);
        if (candidate != nullptr) {
            if (bestNode == nullptr || candidate->getDistance() < bestNode->getDistance()) {
                bestNode = candidate;
                bestNodeIndex = std::get<1>(best);
            }
        }
    }
    //std::cout << "getNextNode() = " << duration_cast<milliseconds>(high_resolution_clock::now() - time).count() << std::endl;

    if (bestNodeIndex != -1) {
        _queue[bestNodeIndex].setColor(2);  // black
    }

    return bestNode;
}

Node * AStar::getBestNode() {
    Node * bestNode = nullptr; // Declare the variable bestNode

    for (int i = 0; i < _queue.size(); ++i) {
        if (_queue[i].getColor() == 2) {  // black
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

void AStar::setTestData(Dataset * test) {
    _testDataset = test;
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