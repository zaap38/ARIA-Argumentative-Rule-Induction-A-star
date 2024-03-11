#include "argument.h"


Argument::Argument() {
    _attribute = "";
    _value = "";
    _id = rand() % 100000000;
}

Argument::Argument(const std::string & attribute, const std::string & value) {
    _attribute = attribute;
    _value = value;
    _id = rand() % 100000000;
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

bool Argument::out() const {
    return _status == 2;
}

bool Argument::undec() const {
    return _status == 0;
}

void Argument::setIn() {
    _status = 1;
}

void Argument::setOut() {
    _status = 2;
}

void Argument::setUndec() {
    _status = 0;
}
