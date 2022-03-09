import af
import copy as cp
import random as rd
from tqdm import tqdm
import string
import config


class Agent:

    def __init__(self):

        self.error = 0
        self.fitness = 0

        self.obj = None

    def mutate(self, possible, intensity=1):
        self.obj.compute_possible_changes()
        for _ in range(intensity):
            self.obj.random_change()
        self.obj.polish()

    def compute_fitness(self, data, reduce=False, verbose=0):
        # Verbose:
        # 0 - nothing
        # 1 - errors only
        # 2 - all
        data_size = len(data)
        if data_size == 0:
            self.error = None
            return
        wrong = self.obj.convert_to_AF()\
            .compare_to_data(data, config.EXTENSION, verbose)
        self.fitness = wrong
        if wrong == 0 or reduce:
            self.fitness += self.obj.size() / 1000.0
        else:
            self.fitness += 1
        self.error = 100 * wrong / data_size

    def random_init(self, possible):
        self.init(possible, [])

    def init(self, a, r):
        self.obj = af.EncodedAF()
        self.obj.init(a)
        self.obj.random_init()
        self.obj.set_R(r)

    def reduce_size(self, max_size):
        self.obj.reduce_size(max_size)

    def remove_trash(self):
        self.obj.remove_trash()


class GeneticAlgorithm:

    def __init__(self, pop_size=100):

        self.agents = []
        self.data = None
        self.training_data = None
        self.test_data = None
        self.possible = None
        self.pop_size = pop_size
        self.verbose = False
        self.last_best = None
        self.best_error = 0
        self.no_change_count = 0
        self.reduce = False

        self.log = dict()  # export logs
        self.log["train"] = dict()
        self.log["train"]["sizes"] = dict()  # [index][agent]
        self.log["train"]["error"] = dict()
        self.log["train"]["error"]["train"] = dict()  # [step]
        self.log["train"]["error"]["test"] = dict()  # [step]

        self.log["final"] = dict()
        self.log["final"]["graph"] = None

    def run_1(self, max_loop):  # program 1
        """
        Limit the graph size.
        """

        self.generate(self.pop_size)

        for step in tqdm(range(max_loop)):

            self.training_data = self.data

            # CORE
            self.compute_fitness()
            self.next_generation(config.SAVE_BEST_AGENT)
            self.cross_over_2(config.CROSSOVER_PERCENT)

            # TOGGLE REDUCE
            if config.MAX_R_SIZE is None or config.FORCE_REDUCE:
                if self.best_error is not None and \
                        self.best_error == self.agents[0].error:
                    self.no_change_count += 1
                    if self.no_change_count > config.REDUCE or \
                            config.FORCE_REDUCE:
                        self.reduce = True
                else:
                    self.no_change_count = 0
                    self.reduce = False
                    self.best_error = self.agents[0].error

            # PRINT
            if step % 10 == 0 and config.LEARNING_VERBOSE > 0:
                best_agent = cp.deepcopy(self.agents[0])
                print("\nError:", str(best_agent.error) + "%",
                      "- Fitness:", self.agents[0].fitness,
                      "- size(R) =", str(best_agent.obj.size()) +
                      "/" + str(config.MAX_R_SIZE))
                print(best_agent.obj.convert_to_AF().R)
                best_agent.compute_fitness(self.test_data)
                print("True Data Err.:", best_agent.error)

            if config.EXPORT:
                best_agent = cp.deepcopy(self.agents[0])
                self.log["train"]["error"]["train"][step] = str(best_agent.error) \
                    .replace('.', ',')
                best_agent.compute_fitness(self.test_data)
                self.log["train"]["error"]["test"][step] = str(best_agent.error) \
                    .replace('.', ',')
                self.log["train"]["sizes"][step] = dict()
                for i, a in enumerate(self.agents):
                    self.log["train"]["sizes"][step][i] = str(a.obj.size())

            if step % config.INCREASE_STEP == 0 and step > 0 \
                    and config.MAX_R_SIZE is not None \
                    and config.INCREASE:
                config.MAX_R_SIZE += config.INCREASE_VALUE

            # CORE
            self.mutate(config.MUTATIONS_INTENSITY,
                        config.SAVE_BEST_AGENT)
            self.heavy_mutate(config.HEAVY_MUTATIONS_PERCENT,
                              config.HEAVY_MUTATIONS_INTENSITY,
                              config.SAVE_BEST_AGENT)
            # self.remove_trash()
            if config.MAX_R_SIZE is not None:
                self.remove_excedent(config.MAX_R_SIZE)

        best_agent = self.agents[0]
        # best_agent = self.rename_blank(best_agent)

        self.print_agent(best_agent, config.FINAL_VERBOSE)

        if config.EXPORT:
            self.log["final"]["graph"] = best_agent.obj.convert_to_AF().R
            self.export()

    def export(self, loc=config.EXPORT_LOC):
        f = open(loc + "error.csv", "w")
        f.write("step;train_e;test_e\n")
        for s in range(len(self.log["train"]["error"]["train"])):
            f.write(str(s) + ";" + self.log["train"]["error"]["train"][s]
                    + ";" + self.log["train"]["error"]["test"][s] + "\n")
        f.close()

        f = open(loc + "sizes.csv", "w")
        to_write = "step"
        for i in range(len(self.log["train"]["sizes"][0])):
            to_write += ";agent_" + str(i)
        to_write += "\n"
        f.write(to_write)
        for s in range(len(self.log["train"]["sizes"])):
            to_write = str(s)
            for i in range(len(self.log["train"]["sizes"][s])):
                to_write += ";" + self.log["train"]["sizes"][s][i]
            f.write(to_write + "\n")
        f.close()

        f = open(loc + "graph.txt", "w")
        for r in self.log["final"]["graph"]:
            f.write(r[0] + " " + r[1] + "\n")
        f.close()

        f = open(loc + "info.txt", "w")
        f.write("STEPS=" + str(config.STEPS) + "\n")
        f.write("POPULATION=" + str(config.POPULATION) + "\n")
        f.write("DATASET=" + str(config.DATASET) + "\n")
        f.write("TEST/TRAIN RATIO=" + str(config.TRAIN_DATA_RATIO) + "\n")
        f.write("IGNORE UNKNOWN=" + str(config.IGNORE_UNKNOWN) + "\n")
        f.write("MUT/HEAVY=" + str(config.MUTATIONS_INTENSITY) + "/"
                + str(config.HEAVY_MUTATIONS_INTENSITY) + "\n")
        f.write("MAX_R_SIZE=" + str(config.MAX_R_SIZE) + "\n")
        f.write("EXTENSION=" + str(config.EXTENSION) + "\n")
        f.write("REDUCE=" + str(config.REDUCE) + "\n")
        f.close()

        print("Data exported to ", loc)

    def print_agent(self, a, verbose=0):
        print("Agent:---------------------------\n")
        a.compute_fitness(self.test_data, True, verbose)
        print("Error:", str(a.error) + "%",
              "- size(A) =", len(a.obj.A),
              "- size(R) =", a.obj.size())
        a.obj.convert_to_AF().print_arg()
        a.obj.convert_to_AF().print_attacks()

    def remove_trash(self):
        for i in range(len(self.agents)):
            self.agents[i].remove_trash()

    def rename_blank(self, a):
        for k, r in enumerate(a.obj.R):
            if is_blank(r[0]) and '|' not in r[0]:
                blank = r[0]
                to_change_a = []
                to_change_b = []
                attacks = []
                attacked_by = []
                for j, r2 in enumerate(a.obj.R):
                    if r2[0] == blank:
                        if not is_blank(r2[1]):
                            attacks.append(r2[1])
                        to_change_a.append(j)
                    elif r2[1] == blank:
                        if not is_blank(r2[0]):
                            attacked_by.append(r2[0])
                        to_change_b.append(j)

                attacks = sorted(attacks)
                attacked_by = sorted(attacked_by)
                attacks_str = ""
                for c in attacks:
                    attacks_str += str(c)
                attacked_by_str = ""
                for c in attacked_by:
                    attacked_by_str += str(c)
                rename = "b0" + attacked_by_str + '|' + attacks_str

                for index in to_change_a:
                    a.obj.R[index] = (rename, a.obj.R[index][1])
                for index in to_change_b:
                    a.obj.R[index] = (a.obj.R[index][0], rename)
                for index, arg in enumerate(a.obj.A):
                    if arg.name == blank:
                        a.obj.A[index].name = rename
        return a

    def generate(self, pop_size=100):
        self.agents = []
        for _ in range(pop_size):
            self.agents.append(Agent())
            self.agents[-1].random_init(self.possible)

    def mutate(self, intensity=1, save_best_agent=False):
        best_agent = cp.deepcopy(self.agents[0])
        for i in range(len(self.agents)):  # skip mutation of agent 0 (best)
            self.agents[i].mutate(self.possible, rd.randint(1, intensity))
        if save_best_agent:
            self.agents[0] = best_agent

    def heavy_mutate(self, percent=10, intensity=5, save_best_agent=False):
        count = len(self.agents) // percent
        best_agent = cp.deepcopy(self.agents[0])
        for i in range(count):
            rand_index = rd.randint(0, len(self.agents) - 1)
            # agent = self.agents[rand_index]
            agent = cp.deepcopy(best_agent)
            for k in range(rd.randint(0, intensity)):
                agent.mutate(self.possible)
            self.agents[rand_index] = cp.deepcopy(agent)
        if save_best_agent:
            self.agents[0] = best_agent

    def cross_over(self, percent=10):
        count = 2 * (len(self.agents) // percent)
        if count % 2 != 0:
            count -= 1
        new_agents = []
        for i in range(count // 2):
            new_agent = cp.deepcopy(self.agents[i])
            second_parent = self.agents[count - i - 1]
            new_agent_arguments = []
            for r in new_agent.obj.R:
                if r[1] not in new_agent_arguments:
                    new_agent_arguments.append(cp.deepcopy(r[1]))
            if not new_agent_arguments:
                continue
            rand_arg = new_agent_arguments[rd.randint(0,
                                                      len(new_agent_arguments)
                                                      - 1)]
            new_attacks = []
            for r in second_parent.obj.R:
                if r[1] == rand_arg:
                    new_attacks.append(cp.deepcopy(r))
            to_remove = []
            for r in new_agent.obj.R:
                if r[1] == rand_arg:
                    to_remove.append(r)
            for r in new_attacks:
                if (r[1], r[0]) not in new_agent.obj.R and\
                        (r[0], r[1]) not in new_agent.obj.R:
                    new_agent.obj.R.append(r)
            new_agents.append(cp.deepcopy(new_agent))
            for r in to_remove:
                new_agent.obj.R.remove(r)

        for i, a in enumerate(new_agents):
            self.agents[- i - 1] = cp.deepcopy(a)

    def cross_over_2(self, percent=10):
        count = 2 * (len(self.agents) // percent)
        count -= count % 2
        new_agents = []
        for i in range(count // 2):
            """new_agent = cp.deepcopy(self.agents[i])
            parent_1 = self.agents[i]
            parent_2 = self.agents[count - i - 1]
            new_agent.obj.R = []
            all_R = parent_1.obj.R + parent_2.obj.R
            for r in all_R:
                if ((r in parent_1.obj.R and r in parent_2.obj.R) or
                        rd.randint(0, 1) == 1) and \
                        r not in new_agent.obj.R and \
                        (r[1], r[0]) not in new_agent.obj.R:
                    new_agent.obj.R.append(cp.deepcopy(r))"""
            # parent_1 = self.agents[rd.randint(0, len(self.agents) - 1)]
            # parent_2 = self.agents[rd.randint(0, len(self.agents) - 1)]

            parent_1 = self.agents[i]
            parent_2 = self.agents[count - i - 1]
            new_agent = cp.deepcopy(parent_1)
            new_agent.obj.recombination(parent_1.obj, parent_2.obj)

            new_agents.append(cp.deepcopy(new_agent))

        for i, a in enumerate(new_agents):
            self.agents[- i - 1] = cp.deepcopy(a)

    def remove_excedent(self, max_R_size):
        for i in range(len(self.agents)):
            if i > 0:
                self.agents[i].reduce_size(max_R_size)

    def next_generation(self, save_best_agent):
        max_value = (len(self.agents) * (len(self.agents) + 1)) // 2
        count = len(self.agents)
        new_agents = []
        self.agents = sorted(self.agents, key=lambda x: x.fitness)
        best_agent = cp.deepcopy(self.agents[0])
        for i in range(count):
            rand_value = rd.randint(0, max_value - 1)
            cpt = 0
            rand_value -= 2 * count - cpt - 1
            while rand_value > 0:
                cpt += 1
                rand_value -= (count - cpt - 1)
            new_agents.append(cp.deepcopy(self.agents[cpt]))
            # print("Add", cpt)
        self.agents = new_agents
        if save_best_agent:
            self.agents[0] = best_agent

    def compute_fitness(self, verbose=False):
        for i in range(len(self.agents)):
            self.agents[i].compute_fitness(self.training_data, self.reduce, verbose)
            verbose = False

    def unique_test(self, args, attacks, data):
        agent = Agent()
        agent.init(args, attacks)
        agent.compute_fitness(data)
        print("Error:", agent.error)


def is_blank(node_name):
    return len(node_name) > 1 and node_name[0] == 'b' and \
           node_name[1] in string.digits
