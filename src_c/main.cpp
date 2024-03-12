#include <iostream>
#include "astar.h"
#include "dataset.h"
#include <tuple>
#include "node.h"


int main(int argc, char * argv[]) {
    
    // config
    float ratio = 0.7;
    int maxIterations = 20;  // -1 for no limit
    int datasetId = 0;

    std::cout << "Init Dataset" << std::endl;

    // init dataset
    Dataset d;
    d.setAttributes({"color", "size", "act", "age", "inflated"});  // set attributes
    d.load("../src/datasets/balloons/yellow-small+adult-stretch.data.txt");  // load data
    Dataset train;
    Dataset test;
    std::tuple<Dataset, Dataset> splitted = d.split(ratio);  // split into train/test
    train = std::get<0>(splitted);
    test = std::get<1>(splitted);
    std::cout << train.size() << " " << test.size() << " " <<d.size() << std::endl;  // "70 30

    std::cout << "Init AStar" << std::endl;
    // init astar graph
    AStar a;
    a.setData(&train);  // set dataset to compute distance

    std::cout << "Run AStar" << std::endl;
    // run astar graph
    Node result = a.run(maxIterations);

    result.print();

    
    std::cout << "Clean" << std::endl;
    // cleanup
    
   std::cout << "Finish" << std::endl;

   return 0;
}
