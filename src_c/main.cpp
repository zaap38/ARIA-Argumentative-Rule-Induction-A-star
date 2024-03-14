#include <iostream>
#include "astar.h"
#include "dataset.h"
#include <tuple>
#include "node.h"
#include "test.h"


int main(int argc, char * argv[]) {

    // tests
    test();
    
    // config
    float ratio = 0.7;
    int maxIterations = -1;  // -1 for no limit
    int datasetId = 0;

    std::cout << "Init Dataset" << std::endl;

    // init dataset
    Dataset d;
    //d.loadBalloons();
    //d.loadCar();
    //d.loadMushroom();
    //d.loadVoting();
    //d.loadBreastCancer();
    d.loadFake();
    Dataset train;
    Dataset test;
    
    std::tuple<Dataset, Dataset> splitted = d.split(ratio);  // split into train/test
    train = std::get<0>(splitted);
    test = std::get<1>(splitted);
    train.setLabelAttribute(d.getLabelAttribute());
    test.setLabelAttribute(d.getLabelAttribute());
    
    // std::cout << train.size() << " " << test.size() << " " <<d.size() << std::endl;  // "70 30

    std::cout << "Init AStar" << std::endl;
    // init astar graph
    AStar a;
    a.setData(&train);  // set dataset to compute distance

    std::cout << "Run AStar" << std::endl;
    // run astar graph
    Node result = a.run(maxIterations);

    result.print("Result: ");

    
    std::cout << "Clean" << std::endl;
    // cleanup
    
   std::cout << "Finish" << std::endl;

   return 0;
}
