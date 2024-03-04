#include "graph.h"


class AStar {

    public:
        AStar();
        ~AStar();


    private:
        Graph *_graph;

        std::vector<Node> _queue;

        std::vector<Node> getNeighbors(const Node & node);
        void addNodeToQueue(const Node & node);
        Node getNextNode();

};
