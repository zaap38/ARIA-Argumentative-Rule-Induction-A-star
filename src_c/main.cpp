#inlude <iostream>
#include "astar.h"
#include "dataset.h"


void main(int argc, char *argv[]) {

    // config
    float ratio = 0.7;
    int maxIterations = -1;
    int datasetId = 0;

    // load dataset
    dataset::Dataset * d = new dataset::Dataset();

    // init astar graph
    astar::AStar * a = new astar::AStar();

    // run astar graph

    // cleanup
    delete a;

}
