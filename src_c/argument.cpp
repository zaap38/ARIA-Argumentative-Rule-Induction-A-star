#include "argument.h"


Argument::Argument() {
    _attribute = "";
    _value = "";
    _id = rand() % 100000000;
}

Argument::Argument(const std::string & attribute, const std::string & value) {
    _attribute = attribute;
    _value = value;
}

Argument::~Argument() {
    // nothing to do
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

bool Argument::getStatus() const {
    return _status;
}

void Argument::setStatus(bool status) {
    _status = status;
}

int Argument::getId() const {
    return _id;
}
