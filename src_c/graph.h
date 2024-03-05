#include <vector>
#include "node.h"


class Graph<T> {
    /*
    Graph used by the AStar algorithm.
    */

    public:
        Graph();
        ~Graph();

    private:
        std::vector<Node> _nodes;

};