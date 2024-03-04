#include "argument.h"


class EncodedAF {

    public:
        EncodedGraph();
        ~EncodedGraph();

    private:
        std::vector<Argument> _a;  // argument list
        std::vector<std::vector<int>> _r;  // encoded attack relation
};

class AF {

    public:
        AF();
        ~AF();

    private:
        std::vector<Node> _nodes;

};