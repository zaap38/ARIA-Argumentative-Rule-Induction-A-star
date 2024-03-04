#include <string>


class Argument {

    public:

        Argument(std::string attribute, std::string value, int id, bool status);
        ~Argument();

        std::string getAttribute() const;
        std::string getValue() const;
        std::string getName() const;  // get the full name, i.e. "attribute=value"
        int getId();
        bool getStatus();

    private:
        std::string _attribute;
        std::string _value;
        int _id;
        bool _status;

};