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
        "/", len(data), "|", round(100 * max(ga_instance.last_generation_fitness) / len(data) , 2), "%")
    return fitness


def custom_mutation(solutions, ga_instance):
    global CURRENTSOL
    for k, solution in enumerate(solutions):
        sol = cp.deepcopy(CURRENTSOL)
        index = rd.randint(0, len(solution) - 1)
        for i in range(len(solution)):
            if solution[i] not in sol and i != index:
                sol.append(solution[i])
        for _ in range(len(solution) // 2):
            possible = gen.GeneticAlgorithm().getPossibleChanges(args, sol)
            val = rd.choice(possible)
            while val in solution:
                val = rd.choice(possible)
            solution[index] = val
        solutions[k] = cp.deepcopy(solution)
    return solutions


if __name__ == "__main__":

    argv = sys.argv[1:]
    config.init(argv)

    r = rules.Rules()

    accuracy = dict()
    accuracy["train"] = []
    accuracy["test"] = []
    accuracy["fake"] = []
    accuracy["diff"] = []

    avg_size = 0

    start_time = time.time()

    nb_run = 1
    accuracy = 0
    
    seed = config.SEED
    if seed is None:
        seed = rd.randint(0, 100000)

    for run in range(nb_run):
        rd.seed(run + seed)

        CURRENTSOL = []

        print("Run:", str(run + 1) + "/" + str(nb_run))

        data, test_data, args, fake_test = r.load_dataset(config.DATASET)

        if config.GLOBAL_TOP:
            args = [config.TOP] + args
        args = [config.TARGET] + args
        gen.possible = args

        runCount = 8

        for incrementLearningCount in range(runCount):
            # Initialize the population
            n = len(args) ** 2
            addonSize = 2
            num_genes = addonSize
            num_generations=config.STEPS
            crossover_type = "single_point"
            parent_selection_type = "rws"  # "sss"
            num_parents_mating=config.POPULATION // 2
            keep_parents = 0
            domain = dict()
            domain["step"] = 1
            domain["low"] = 0
            domain["high"] = n
            if config.LOCAL_TOP:
                domain["low"] = -n
            mutation_type = custom_mutation
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
                            mutation_num_genes=addonSize,
                            gene_space=domain,
                            random_seed=seed + incrementLearningCount,
                            keep_elitism=1,
                            allow_duplicate_genes=False)

            # Run the pg optimization
            ga_instance.run()

            solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
            #minSol = gen.GeneticAlgorithm().minimize(args, solution)
            print("Fitnesses:", ga_instance.last_generation_fitness)
            minSol = cp.deepcopy(solution)
            solution = gen.GeneticAlgorithm().toNames(args, solution)
            minSolNames = gen.GeneticAlgorithm().toNames(args, minSol)
            print(CURRENTSOL)
            print(solution)
            for s in minSol:
                if s not in CURRENTSOL:
                    CURRENTSOL.append(s)
            print("Added", len(minSol), "at run", incrementLearningCount + 1, "/", runCount, "|", solution, "->", minSolNames)
            acc, details = gen.GeneticAlgorithm().unique_test_verbose(args, CURRENTSOL, test_data, True)
            print("True:", details["true_predicted"], "/", details["true_count"], "-",
                  round(100 * details["true_predicted"] / details["true_count"], 2), "%", end=" | ")
            print("False:", details["false_predicted"], "/", details["false_count"], "-",
                  round(100 * details["false_predicted"] / details["false_count"], 2), "%", end=" | ")
            print("Total:", acc, "/", len(test_data), "-", round(100 * acc / len(test_data), 2), "%")

        acc = gen.GeneticAlgorithm().unique_test_verbose(args, CURRENTSOL, test_data, True)[0]
        accuracy += round(100 * acc / len(test_data), 2)

    print(round(accuracy / nb_run, 2), "%")


    seconds = time.time() - start_time
    minutes = int(seconds / 60)
    # print("Seconds:", round(seconds))
    seconds_raw = seconds
    seconds = int(seconds % 60)
    print("Time:", minutes, "m", seconds, "s")
