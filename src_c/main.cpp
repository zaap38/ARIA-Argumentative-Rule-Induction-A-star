#pragma once
#include <iostream>
#include "astar.h"
#include "dataset.h"


void main(int argc, char *argv[]) {

    // config
    float ratio = 0.7;
    int maxIterations = -1;
    int datasetId = 0;

    // init dataset
    dataset::Dataset d = new dataset::Dataset();
    d.load("data.csv");  // load data
    dataset::Dataset train;
    dataset::Dataset test;
    std::<dataset::Dataset, dataset::Dataset> splitted = d.split(ratio);  // split into train/test
    train = std::get<0>(splitted);
    test = std::get<1>(splitted);


    // init astar graph
    astar::AStar a = astar::AStar();
    a.setData(&train);  // set dataset to compute distance

    // run astar graph

    // cleanup

}
