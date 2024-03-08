#include <iostream>
#include "astar.h"
#include "dataset.h"
#include <tuple>


int main(int argc, char * argv[]) {
    
    // config
    float ratio = 0.7;
    int maxIterations = -1;
    int datasetId = 0;

    // init dataset
    Dataset d;
    d.load("data.csv");  // load data
    Dataset train;
    Dataset test;
    std::tuple<Dataset, Dataset> splitted = d.split(ratio);  // split into train/test
    train = std::get<0>(splitted);
    test = std::get<1>(splitted);


    // init astar graph
    AStar a = AStar();
    a.setData(&train);  // set dataset to compute distance
    a.run(maxIterations);

    // run astar graph

    // cleanup
    
   std::cout << "Hello, World!" << std::endl;

   return 0;
}
