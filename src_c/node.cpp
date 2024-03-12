#include "node.h"

Node::Node() {
    _id = std::rand() % 100000000;  // fix that one day
    _color = 0;
    _distance = -1;
    _predecessor = -1;
    _value = nullptr;
    _dataset = nullptr;
}


Node::Node(int id) {
    _id = id;
    _color = 0;
    _distance = -1;
    _predecessor = -1;
    _value = nullptr;
    _dataset = nullptr;
}

Node::Node(int id, Dataset * dataset, EncodedAF * value) {
    _dataset = dataset;
    _id = id;
    _color = 0;
    _distance = -1;
    _predecessor = -1;
    _value = value;
}

Node::Node(const Node & node) {
    _id = std::rand() % 100000000;  // fix that one day
    _color = node._color;
    _distance = node._distance;
    _predecessor = node._predecessor;
    _value = new EncodedAF(*node._value);
    _dataset = node._dataset;
}

Node::~Node() {
    if (_value != nullptr) {
        delete _value;
    }
}


float Node::getDistance(bool ignoreRSize) {
    if (_distance < 0) {
        computeDistance(ignoreRSize);
    }
    return _distance;
}

void Node::computeDistance(bool ignoreRSize) {
    /*
    _distance = number of misclassified examples + (number of attacks / 1000)
    Perfect score is 0
    */
    int correct = 0;
    int total = _dataset->size();
    for (int i = 0; i < total; ++i) {
        AF * af = _value->convertToAF();
        if (af->predict(_dataset->get(i).getFacts(), _dataset->get(i).getLabel())) {
            ++correct;
        }
        delete af;
    }
    std::cout << "after" << std::endl;
    int addedSizeDistance = 0;
    if (!ignoreRSize) {
        addedSizeDistance = _value->getAttacks().size() / 1000;
    }
    _distance = (total - correct) + addedSizeDistance;
}

int Node::getColor() const {
    return _color;
}

EncodedAF * Node::getValue() const {
    return _value;
}

void Node::setColor(int color) {
    _color = color;
}

void Node::setPredecessor(int predecessor) {
    _predecessor = predecessor;
}

std::vector<Node> Node::getNeighbors() const {
    std::vector<Node> neighbors;
    std::vector<Attack> possibleAddons = _value->getPossibleAddons();
    for (int i = 0; i < possibleAddons.size(); ++i) {
        if (_neighbors[i].getColor() == 0) {
            Node neighborNode;
            neighborNode._value = new EncodedAF(*_value);
            neighborNode._value->addAttack(possibleAddons[i]);
            neighbors.push_back(neighborNode);
        }
    }
    return neighbors;
}

void Node::print() const {
    std::cout << "Distance: " << _distance << std::endl;
    _value->print();
}