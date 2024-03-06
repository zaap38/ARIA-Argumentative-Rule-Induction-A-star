#pragma once
#include <string>


class Argument {

    public:
        Argument();
        Argument(const std::string & attribute, const std::string & value);
        ~Argument();

        std::string getAttribute() const;
        std::string getValue() const;
        std::string getName() const;  // get the full name, i.e. "attribute=value"
        int getId() const;
        bool getStatus() const;
        void setValue(const std::string & value);
        void setAttribute(const std::string & attribute);

        bool operator==(const Argument & a) const;
        bool operator!=(const Argument & a) const;

    private:
        std::string _attribute;
        std::string _value;
        int _id;
        bool _status;  // true: alive; false: dead/not in facts

};