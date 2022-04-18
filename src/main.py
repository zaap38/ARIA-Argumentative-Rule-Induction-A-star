import rules
import genetic
import time
import config
import sys

if __name__ == "__main__":

    argv = sys.argv[1:]
    config.init(argv)

    r = rules.Rules()

    # config ---------------------

    # args = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']  # medium set
    # args = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'b1', 'b2']  # medium set + small blank
    # args = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'b1', 'b2', 'b3', 'b4', 'b5']  # medium set + blank
    # args = ['a', 'b', 'c', 'd', 'e', 'f']  # facts only set
    # args = ['a', 'b', 'c', 'd', 'e', 'f', 'b1', 'b2', 'b3', 'b4', 'b5']  # blank node (always fact) but not used in formula
    # args = ['a', 'b', 'b1', 'b2', 'b3', 'b4', 'b5']  # blank + small
    # args = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7']  # large + blank
    # args = ['a', 'b']  # small set
    # args = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'b1', 'b2', 'b3', 'b4', 'b5']  # large + blank
    # args = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']  # large

    accuracy = []
    start_time = time.time()

    nb_run = 1

    for run in range(nb_run):
        print("Run:", str(run + 1) + "/" + str(nb_run))
        # start ----------------------
        args = []
        gen = genetic.GeneticAlgorithm(config.POPULATION)

        # true dataset
        if config.DATASET == 0:  # mushroom
            gen.data, gen.test_data, args = r.load_dataset_mushroom(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 1:  # voting
            gen.data, gen.test_data, args = r.load_dataset_voting(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 2:  # breast-cancer
            gen.data, gen.test_data, args = r.load_dataset_breast_cancer(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 3:  # heart-disease
            gen.data, gen.test_data, args = r.load_dataset_heart_disease(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 4:  # car
            gen.data, gen.test_data, args = r.load_dataset_car(
                config.TRAIN_DATA_RATIO, config.NOISE, True)

        elif config.DATASET == 5:  # breast-cancer-wisconsin
            gen.data, gen.test_data, args = r.load_dataset_breast_cancer_wisconsin(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 6:  # balloons
            gen.data, gen.test_data, args = r.load_dataset_balloons(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 7:  # tic-tac-toe
            gen.data, gen.test_data, args = r.load_dataset_tic_tac_toe(
                config.TRAIN_DATA_RATIO,
                config.NOISE)
        # ------------

        if config.GLOBAL_TOP:
            args = [config.TOP] + args
        args = [config.TARGET] + args
        gen.possible = args

        # ----------------

        accuracy.append(gen.run_1(config.STEPS))

    seconds = time.time() - start_time
    minutes = int(seconds / 60)
    seconds = int(seconds % 60)
    print("Time:", minutes, "m", seconds, "s")

    s = 0
    print(len(accuracy), "values")
    for index, a in enumerate(accuracy):
        print(index, ":", a)
        s += a
    print(s / len(accuracy))
