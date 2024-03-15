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

int Node::runOnDataset(int offset, int coreCount) {
    /*
    Used for multi-threading purpose.
    */
   std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    AF * af = _value->convertToAF();
    int correctCount = 0;
    for (int i = offset; i < _dataset->size(); i += coreCount) {
        if (af->predict(_dataset->get(i).getFacts(), _dataset->getLabelAttribute()) == _dataset->get(i).getLabel()) {
            ++correctCount;
        }
    }
    delete af;
    return correctCount;
}

void Node::computeDistance(bool ignoreRSize) {
    /*
    _distance = number of misclassified examples + (number of attacks / 1000)
    Perfect score is 0
    */
    int correct = 0;
    int total = _dataset->size();
    const auto processor_count = std::thread::hardware_concurrency();
    std::vector<std::future<int>> corrects;
    for (int i = 0; i < processor_count; ++i) {
        corrects.push_back(std::async(&Node::runOnDataset, this, i, processor_count));
    }
    for (int i = 0; i < processor_count; ++i) {
        correct += corrects[i].get();
    }
    float addedSizeDistance = 0;
    if (!ignoreRSize) {
        addedSizeDistance = _value->getAttackSize() / 1000.0;
    }
    _distance = (total - correct) + addedSizeDistance;
}

int Node::getColor() const {
    return _color;
}

EncodedAF * Node::getValue() const {
    return _value;
}

int Node::getAttackSize() const {
    return _value->getAttackSize();
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
        if (true || _neighbors[i].getColor() == 0) {
            Node neighborNode;
            neighborNode._value = new EncodedAF(*_value);
            neighborNode._dataset = _dataset;
            neighborNode._value->addAttack(possibleAddons[i]);
            neighbors.push_back(neighborNode);
        }
    }
    return neighbors;
}

void Node::print(const std::string & prefix) const {
    std::cout << prefix << "Distance: " << _distance << '/' << _dataset->size() << std::endl;
    std::cout << "vvvvvv" << std::endl;
    _value->print();
    std::cout << "======" << std::endl;
}

std::string Node::getLabelAttribute() const {
    return _dataset->getLabelAttribute();
}