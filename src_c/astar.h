#include "astar.cpp"


class AStar {

    public:
        AStar();
        ~AStar();

        void run(int maxIterations = -1);  // -1: no limit


    private:
        std::vector<Node> _queue;

        std::vector<Node> getNeighbors(const Node & node);
        void addNodeToQueue(Node & node);
        Node * getNextNode() const;
        Node * getBestNode() const;

};
