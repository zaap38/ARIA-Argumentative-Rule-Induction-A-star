import rules
import genetic
import time
import config
import sys
import random as rd
from tqdm import tqdm

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

    accuracy = dict()
    accuracy["train"] = []
    accuracy["test"] = []
    accuracy["fake"] = []
    accuracy["diff"] = []

    avg_size = 0

    start_time = time.time()

    nb_run = 1

    for run in range(nb_run):
        if config.SEED is not None:
            #rd.seed(run + config.SEED)
            pass

        print("Run:", str(run + 1) + "/" + str(nb_run))
        # start ----------------------
        args = []
        gen = genetic.GeneticAlgorithm(config.POPULATION)

        # true dataset
        if config.DATASET == 0:  # mushroom
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_mushroom(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 1:  # voting
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_voting(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 2:  # breast-cancer
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_breast_cancer(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 3:  # heart-disease
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_heart_disease(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 4:  # car
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_car(
                config.TRAIN_DATA_RATIO, config.NOISE, True)

        elif config.DATASET == 5:  # breast-cancer-wisconsin
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_breast_cancer_wisconsin(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 6:  # balloons
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_balloons(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 7:  # tic-tac-toe
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_tic_tac_toe(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 8:  # monks-1
            gen.data, gen.test_data, args = r.load_dataset_monk_1(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 9:  # adult
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_adult(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 10:  # marco-law
            gen.data, gen.test_data, args, gen.fake_test = r.load_dataset_law(
                config.TRAIN_DATA_RATIO, config.NOISE, True)
        # ------------

        if config.GLOBAL_TOP:
            args = [config.TOP] + args
        args = [config.TARGET] + args
        gen.possible = args

        # ----------------
        best_test, best_train, best_fake, best_size = gen.run_1(config.STEPS)
        accuracy["test"].append(best_test)
        accuracy["train"].append(best_train)
        accuracy["fake"].append(best_fake)
        accuracy["diff"].append(abs(best_fake - best_train))

        avg_size += best_size

    seconds = time.time() - start_time
    minutes = int(seconds / 60)
    print("Seconds:", seconds)
    seconds_raw = seconds
    seconds = int(seconds % 60)
    print("Time:", minutes, "m", seconds, "s")

    s = 0
    min_v = 100
    max_v = 0
    select_best = 100
    select_v = 0
    print(len(accuracy), "values: Test - Train - Fake - Diff")
    for index in range(nb_run):
        print(round(100 - accuracy["test"][index], 2))
        """print(index, ":", round(accuracy["test"][index], 2),
        round(accuracy["train"][index], 2),
        round(accuracy["fake"][index], 2),
        round(accuracy["diff"][index], 2))"""
        s += accuracy["test"][index]
        min_v = min(min_v, accuracy["test"][index])
        max_v = max(max_v, accuracy["test"][index])
        if select_best > accuracy["diff"][index]:
            select_best = accuracy["diff"][index]
            select_v = accuracy["test"][index]

    print("Final Result:")  # avg, (min, max), select, avg_size, avg_time
    print(round(100 - s / nb_run, 2),
          "(" + str(round(100 - max_v, 1)) + "-" + str(round(100 - min_v, 1)) + ")",
          round(100 - select_v, 1), round(avg_size / nb_run, 1), round(seconds_raw / nb_run, 1))
