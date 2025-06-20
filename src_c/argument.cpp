#include "argument.h"


Argument::Argument() {
    _attribute = "";
    _value = "";
    _id = rand() % 100000000;
    _isLabel = false;
    _isNegation = false;
}

Argument::Argument(const std::string & attribute, const std::string & value) {
    _attribute = attribute;
    _value = value;
    _id = rand() % 100000000;
    _isLabel = false;
    _isNegation = false;
}

Argument::~Argument() {
    // nothing to do
}

bool Argument::isLabel() const {
    return _isLabel;
}

void Argument::setIsLabel(bool isLabel) {
    _isLabel = isLabel;
}

bool Argument::isNegation() const {
    return _isNegation;
}

void Argument::setIsNegation(bool isNegation) {
    _isNegation = isNegation;
}

std::string Argument::getName() const {
    return _attribute + "=" + _value;
}

std::string Argument::getValue() const {
    return _value;
}

void Argument::setValue(const std::string & value) {
    _value = value;
}

std::string Argument::getAttribute() const {
    return _attribute;
}

void Argument::setAttribute(const std::string & attribute) {
    _attribute = attribute;
}

bool Argument::operator==(const Argument & a) const {
    return getName() == a.getName();
}

bool Argument::operator!=(const Argument & a) const {
    return !(getName() == a.getName());
}

int Argument::getStatus() const {
    return _status;
}

void Argument::setStatus(int status) {
    _status = status;
}

int Argument::getId() const {
    return _id;
}

bool Argument::in() const {
    return _status == 1;
}

bool Argument::inSup() const {
    return _status == 3;
}

bool Argument::tempInSup() const {
    return _status == 4;  // temporary in support, used for bipartite AFs
}

bool Argument::out() const {
    return _status == 2;
}

bool Argument::undec() const {
    return _status == 0;
}

void Argument::setIn() {
    _status = 1;
}

void Argument::setInSup() {
    _status = 3;
}

void Argument::setTempInSup() {
    _status = 4;  // temporary in support, used for bipartite AFs
}

void Argument::setOut() {
    _status = 2;
}

void Argument::setUndec() {
    _status = 0;
}
