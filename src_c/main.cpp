#include <iostream>
#include "astar.h"
#include "dataset.h"
#include <tuple>
#include "node.h"
#include "test.h"
#include <chrono>

using namespace std::chrono;


int main(int argc, char * argv[]) {

    std::vector<high_resolution_clock::time_point> timestamps;
    timestamps.push_back(high_resolution_clock::now());

    // tests
    test();
    timestamps.push_back(high_resolution_clock::now());

    int runCount = 1;
    bool verbose = true;
    for (int runIndex = 0; runIndex < runCount; ++runIndex) {
    
        // config
        float ratio = 0.7;
        float minBalanceRatio = 0.4;  // should be < 0.5
        int maxIterations = 15;  // -1 for no limit
        int seed = 11 + runIndex;//10;
        float samplingInterval = 3;

        //std::cout << "Init Dataset" << std::endl;

        // init dataset
        Dataset d;
        //d.setSamplingInterval(samplingInterval);
        
        d.setSeed(seed);
        //d.loadBalloons();
        //d.loadCar();
        //d.loadMushroom();
        //d.loadVoting();
        //d.loadBreastCancer();
        //d.loadBreastCancerWisconsin();
        //d.loadHeartDisease();
        //d.loadIris();
        //d.loadFake();
        //d.loadMoralMachine();
        //d.loadMoralMachineExt();
        //d.loadMoralMachineBBTest();
        d.loadMoralMachineComplete();
        //d.loadMoralMachineCompleteBB();

        Dataset train;
        Dataset test;
        
        //d.balance(minBalanceRatio);  // re-balance dataset
        std::tuple<Dataset, Dataset> splitted = d.split(ratio);  // split into train/test
        train = std::get<0>(splitted);
        test = std::get<1>(splitted);
        train.setLabelAttribute(d.getLabelAttribute());
        test.setLabelAttribute(d.getLabelAttribute());

        timestamps.push_back(high_resolution_clock::now());
        
        // std::cout << train.size() << " " << test.size() << " " <<d.size() << std::endl;  // "70 30

        //std::cout << "Init AStar" << std::endl;
        // init astar graph
        AStar a;
        a.setVerbose(verbose);
        a.setData(&train);  // set dataset to compute distance
        a.setTestData(&test);  // set test dataset
        a.setMaxRsize(50);  // set maxRsize
        timestamps.push_back(high_resolution_clock::now());

        std::cout << "Run AStar" << std::endl;
        // run astar graph
        Node result = a.run(maxIterations);
        timestamps.push_back(high_resolution_clock::now());

        result.print("Result run " + std::to_string(runIndex) + ": ");

        std::cout << "Train acc.: " << result.getDistance() << "/" << train.size() <<
        " - " << result.getAccuracy(1) << std::endl;

        result.setDataset(&test);
        std::cout << "Test acc.: " << result.getDistance() << "/" << test.size() <<
        " - " << result.getAccuracy(1) << std::endl;

    }

    
    /*std::cout << "Clean" << std::endl;
    // cleanup

    std::cout << "Timestamps:" << std::endl;
    std::cout << "Tests: " << duration_cast<milliseconds>(timestamps[1] - timestamps[0]).count() << "ms" << std::endl;
    std::cout << "Init Dataset: " << duration_cast<milliseconds>(timestamps[2] - timestamps[1]).count() << "ms" << std::endl;
    std::cout << "Init AStar: " << duration_cast<milliseconds>(timestamps[3] - timestamps[2]).count() << "ms" << std::endl;
    std::cout << "Run AStar: " << duration_cast<milliseconds>(timestamps[4] - timestamps[3]).count() << "ms" << std::endl;
    std::cout << "Total: " << duration_cast<milliseconds>(timestamps[4] - timestamps[0]).count() << "ms" << std::endl;*/

    return 0;
}