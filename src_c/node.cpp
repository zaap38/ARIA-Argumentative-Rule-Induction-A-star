#include "node.h"


Node::Node(int id) {
    _id = id;
    _color = 0;
    _distance = -1;
    _predecessor = -1;
    _value = nullptr;
    _dataset = nullptr;
}

Node::Node(int id, EncodedAF * value) {
    _id = id;
    _color = 0;
    _distance = -1;
    _predecessor = -1;
    _value = value;
    _dataset = nullptr;
}

Node::~Node() {
    if (_value != nullptr) {
        delete _value;
    }
}


float Node::getDistance(bool ignoreRSize = false) {
    if (_distance < 0) {
        computeDistance(ignoreRSize);
    }
    return _distance;
}

void Node::computeDistance(bool ignoreRSize = false) {
    
    int correct = 0;
    int total = _dataset->size();
    for (int i = 0; i < total; ++i) {
        AF af = *_value->convertToAF();
        af.updateAliveness(_dataset->get(i).getFacts());
        std::string predicted = af.predict();
        if (predicted == _dataset->get(i).getLabel()) {
            ++correct;
        }
    }
    int addedSizeDistance = 0;
    if (!ignoreRSize) {
        addedSizeDistance = _value->getAttacks().size() / 1000;
    }
    _distance = (total - correct) + addedSizeDistance;
}