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

    int runCount = 10;
    bool verbose = true;

    std::vector<float> train_accuracies, test_accuracies;

    for (int runIndex = 0; runIndex < runCount; ++runIndex) {
    
        // config
        float ratio = 0.7;
        float minBalanceRatio = 0.4;  // should be < 0.5
        int maxIterations = 10;  // -1 for no limit
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
        //d.loadMoralMachineComplete();
        //d.loadMoralMachineCompleteBB();
        d.loadWine();

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
        train_accuracies.push_back(result.getAccuracy(1));

        result.setDataset(&test);
        std::cout << "Test acc.: " << result.getDistance() << "/" << test.size() <<
        " - " << result.getAccuracy(1) << std::endl;
        test_accuracies.push_back(result.getAccuracy(1));

    }

    
    /*std::cout << "Clean" << std::endl;
    // cleanup

    std::cout << "Timestamps:" << std::endl;
    std::cout << "Tests: " << duration_cast<milliseconds>(timestamps[1] - timestamps[0]).count() << "ms" << std::endl;
    std::cout << "Init Dataset: " << duration_cast<milliseconds>(timestamps[2] - timestamps[1]).count() << "ms" << std::endl;
    std::cout << "Init AStar: " << duration_cast<milliseconds>(timestamps[3] - timestamps[2]).count() << "ms" << std::endl;
    std::cout << "Run AStar: " << duration_cast<milliseconds>(timestamps[4] - timestamps[3]).count() << "ms" << std::endl;
    std::cout << "Total: " << duration_cast<milliseconds>(timestamps[4] - timestamps[0]).count() << "ms" << std::endl;*/

    // if multi-run
    if (train_accuracies.size() > 1) {
        float train_sum = 0, test_sum = 0;
        for (float acc : train_accuracies) {
            train_sum += acc;
        }
        for (float acc : test_accuracies) {
            test_sum += acc;
        }
        float train_mean = train_sum / train_accuracies.size();
        float test_mean = test_sum / test_accuracies.size();

        // Compute standard deviation
        float train_sq_sum = 0, test_sq_sum = 0;
        for (float acc : train_accuracies) {
            train_sq_sum += (acc - train_mean) * (acc - train_mean);
        }
        for (float acc : test_accuracies) {
            test_sq_sum += (acc - test_mean) * (acc - test_mean);
        }
        float train_stddev = std::sqrt(train_sq_sum / train_accuracies.size());
        float test_stddev = std::sqrt(test_sq_sum / test_accuracies.size());

        std::cout << "Average Train Accuracy: " << train_mean << " (stddev: " << train_stddev << ")" << std::endl;
        std::cout << "Average Test Accuracy: " << test_mean << " (stddev: " << test_stddev << ")" << std::endl;
    }

    return 0;
}