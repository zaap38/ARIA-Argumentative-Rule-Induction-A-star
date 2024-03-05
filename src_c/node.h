#include "af.h"
#include <vector>
#include "node.cpp"
#include "dataset.h"
#include <string>


class Node {

    public:
        Node(int id);
        Node(int id, af::EncodedAF * value);
        ~Node();

        float getDistance() const;
        int getColor() const;
        af::EncodedAF * getValue() const;

        void setColor(int color);
        void setPredecessor(int predecessor);

    private:
        int _id;
        af::EncodedAF * _value;
        int _color;  // 0: white; 1: grey; 2: black
        int _distance(-1);  // -1 means not initialized
        int _predecessor;  // predecessor id
        std::vector<Node> _neighbors;
        dataset::Dataset * _dataset;  // pointer to the dataset
        
        void computeDistance();

};