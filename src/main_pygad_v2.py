import rules
import genetic as gen
import time
import config
import sys
import random as rd
from tqdm import tqdm
import pygad as pg
import copy as cp

CURRENTSOL = []


def fitness_function(ga_instance : pg.GA, solution, solution_index):
    verbose = False
    #print(ga_instance.generations_completed, solution_index)
    if ga_instance.generations_completed % 10 == 0:
        verbose = False
    sol = cp.deepcopy(CURRENTSOL)
    for s in solution:
        if s not in sol:
            sol.append(s)
    fitness = gen.GeneticAlgorithm().unique_test(args, sol, data, verbose)
    if ga_instance.generations_completed > 0 and solution_index == config.POPULATION - 1:
        print(ga_instance.generations_completed,
        ": best fitness =", int(max(ga_instance.last_generation_fitness)),
        "/", len(data), round(100 * max(ga_instance.last_generation_fitness) / len(data) , 2))
    return fitness


def custom_mutation(solution, ga_instance):
    for i in range(len(solution)):
        sol = cp.deepcopy(CURRENTSOL)
        for s in solution[i]:
            if s not in sol:
                sol.append(s)
        possible = gen.GeneticAlgorithm().getPossibleChanges(args, sol)
        solution[i][rd.randint(0, len(solution[i]) - 1)] = rd.choice(possible)
        # print(solution[i])
    return solution


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
    
    seed = config.SEED
    if seed is None:
        seed = rd.randint(0, 100000)

    for run in range(nb_run):
        rd.seed(run + seed)

        print("Run:", str(run + 1) + "/" + str(nb_run))
        # start ----------------------
        args = []

        data = []
        test_data = []
        fake_test = []  # ignored

        # true dataset
        if config.DATASET == 0:  # mushroom
            data, test_data, args, fake_test = r.load_dataset_mushroom(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 1:  # voting
            data, test_data, args, fake_test = r.load_dataset_voting(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 2:  # breast-cancer
            data, test_data, args, fake_test = r.load_dataset_breast_cancer(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 3:  # heart-disease
            data, test_data, args, fake_test = r.load_dataset_heart_disease(
                config.TRAIN_DATA_RATIO, config.NOISE)

        elif config.DATASET == 4:  # car
            data, test_data, args, fake_test = r.load_dataset_car(
                config.TRAIN_DATA_RATIO, config.NOISE, True)

        elif config.DATASET == 5:  # breast-cancer-wisconsin
            data, test_data, args, fake_test = r.load_dataset_breast_cancer_wisconsin(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 6:  # balloons
            data, test_data, args, fake_test = r.load_dataset_balloons(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 7:  # tic-tac-toe
            data, test_data, args, fake_test = r.load_dataset_tic_tac_toe(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 8:  # monks-1
            data, test_data, args = r.load_dataset_monk_1(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 9:  # adult
            data, test_data, args, fake_test = r.load_dataset_adult(
                config.TRAIN_DATA_RATIO,
                config.NOISE)

        elif config.DATASET == 10:  # marco-law
            data, test_data, args, fake_test = r.load_dataset_law(
                config.TRAIN_DATA_RATIO, config.NOISE, True)
        # ------------

        if config.GLOBAL_TOP:
            args = [config.TOP] + args
        args = [config.TARGET] + args
        gen.possible = args

        runCount = 8

        for incrementLearningCount in range(runCount):
            best_fit = 0
            # Initialize the population
            n = len(args) - 1
            n = n * n # ((n + 1) * n) // 2  # triangle
            addonSize = 2
            num_genes = addonSize #config.MAX_R_SIZE
            # print(num_genes)
            num_generations=config.STEPS
            crossover_type = "single_point"
            parent_selection_type = "rws"  # "sss"
            num_parents_mating=config.POPULATION // 2
            keep_parents = 1
            domain = dict()
            domain["step"] = 1
            domain["low"] = 0
            domain["high"] = n + 1  # not included
            mutation_type = custom_mutation#"random"
            ga_instance = pg.GA(num_generations=num_generations,
                            num_parents_mating=num_parents_mating,
                            fitness_func=fitness_function,
                            sol_per_pop=config.POPULATION,
                            num_genes=num_genes,
                            init_range_low=domain["low"],
                            init_range_high=domain["high"],
                            parent_selection_type=parent_selection_type,
                            keep_parents=keep_parents,
                            crossover_type=crossover_type,
                            mutation_type=mutation_type,
                            mutation_num_genes=addonSize, #// 2,
                            gene_space=domain,
                            random_seed=seed + runCount,
                            keep_elitism=1,
                            allow_duplicate_genes=False)

            # Run the pg optimization
            ga_instance.run()

            solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
            minSol = gen.GeneticAlgorithm().minimize(args, solution)
            solution = gen.GeneticAlgorithm().toNames(args, solution)
            minSolNames = gen.GeneticAlgorithm().toNames(args, minSol)
            print("Reduced:", solution, "->", minSolNames)
            for s in minSol:
                if s not in CURRENTSOL:
                    CURRENTSOL.append(s)
            print("Best:", solution_fitness)
            print("Added", len(minSol), "at run", incrementLearningCount + 1, "/", runCount)
            acc = gen.GeneticAlgorithm().unique_test(args, CURRENTSOL, test_data, True)
            print(acc, "/", len(test_data), "-", round(100 * acc / len(test_data), 2))


    seconds = time.time() - start_time
    minutes = int(seconds / 60)
    print("Seconds:", seconds)
    seconds_raw = seconds
    seconds = int(seconds % 60)
    print("Time:", minutes, "m", seconds, "s")
