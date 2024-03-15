#pragma once
#include <string>
#include <iostream>


class Argument {

    public:
        Argument();
        Argument(const std::string & attribute, const std::string & value);
        ~Argument();

        std::string getAttribute() const;
        std::string getValue() const;
        std::string getName() const;  // get the full name, i.e. "attribute=value"
        int getId() const;
        int getStatus() const;
        bool in() const;
        bool out() const;
        bool undec() const;
        void setStatus(int status);
        void setIn();
        void setOut();
        void setUndec();
        void setValue(const std::string & value);
        void setAttribute(const std::string & attribute);

        bool operator==(const Argument & a) const;
        bool operator!=(const Argument & a) const;
        bool isLabel() const;
        void setIsLabel(bool isLabel);
        bool isNegation() const;
        void setIsNegation(bool isNegation);

    private:
        std::string _attribute;
        std::string _value;
        bool _isLabel;
        bool _isNegation;
        int _id;
        int _status;  // 0: TBD ; 1: in ; 2: out
        int _degree;  // depth of the node - used to avoid cycles

};