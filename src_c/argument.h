#pragma once
#include <string>


class Argument {

    public:
        Argument();
        Argument(std::string attribute, std::string value, int id, bool status);
        ~Argument();

        std::string getAttribute() const;
        std::string getValue() const;
        std::string getName() const;  // get the full name, i.e. "attribute=value"
        int getId();
        bool getStatus();
        void setValue(std::string value);
        void setAttribute(std::string attribute);

        bool operator==(const Argument & a) const;

    private:
        std::string _attribute;
        std::string _value;
        int _id;
        bool _status;  // true: alive; false: dead/not in facts

};