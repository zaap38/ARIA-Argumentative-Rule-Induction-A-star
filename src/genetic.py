import af
import copy as cp
import random as rd
from tqdm import tqdm
import string
import config
import snippets as sn
import math


class Agent:

    def __init__(self):

        self.error = 0
        self.fitness = 0
        self.old_fitness = 0

        self.obj = None

    def mutate(self, possible, intensity=1):
        self.obj.compute_possible_changes()
        for _ in range(rd.randint(1, intensity)):
            self.obj.random_change()
        # if rd.randint(0, 20) == 0:
        # self.obj.polish()

    def compute_fitness(self, data, reduce=False, verbose=0):
        # Verbose:
        # 0 - nothing
        # 1 - errors only
        # 2 - all
        self.old_fitness = self.fitness
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

        delta = abs(self.fitness - self.old_fitness)
        if delta < 5 and delta >= 1:
            self.fitness = self.fitness + 1000

        return self.error

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
        self.fake_test = None
        self.possible = None
        self.pop_size = pop_size
        self.verbose = False
        self.best_error_train = 0
        self.best_error_fake = 0
        self.best_error = 0
        self.no_change_count = 0
        self.reduce = False
        self.heat = config.HEAT * int(config.SA)  # 0 if not config.SA
        self.best_error_bis = 100
        self.last_best = None
        self.very_best = 100
        self.seq = 0  # consecutive times where delta E < config.EPSILON_E
        self.delta_e = 0

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
        Returns the best agent error percent.
        """

        self.generate(self.pop_size)

        for step in tqdm(range(max_loop)):

            self.training_data = self.data

            # CORE
            self.compute_fitness()

            self.sa_update_seq(self.delta_e)

            self.next_generation(config.SAVE_BEST_AGENT)
            self.cross_over_2(config.CROSSOVER_PERCENT, config.SAVE_BEST_AGENT)

            if config.STRONGER:
                if self.best_error is not None and \
                        self.best_error == self.agents[0].error:
                    self.no_change_count += 1
                    if self.no_change_count > 20:
                        self.no_change_count = 0
                        if config.MUTATIONS_INTENSITY < 16:
                            config.MUTATIONS_INTENSITY = config.MUTATIONS_INTENSITY + 1
                            config.HEAVY_MUTATIONS_INTENSITY = config.HEAVY_MUTATIONS_INTENSITY + 1
                else:
                    config.MUTATIONS_INTENSITY = 2
                    config.HEAVY_MUTATIONS_INTENSITY = 4
                            
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
                print("\nError:", str(round(best_agent.error, 3)) + "%",
                      "- Fitness:", self.agents[0].fitness,
                      "- Heat:", round(self.heat, 2),
                      "- size(R) =", str(best_agent.obj.size()) +
                      "/" + str(config.MAX_R_SIZE))
                print(best_agent.obj.convert_to_AF().R)
                best_agent.compute_fitness(self.test_data)
                # print("Mutations:", config.MUTATIONS_INTENSITY)
                print("True Data Err.:", round(best_agent.error, 3))

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

        best_agent = cp.deepcopy(self.agents[0])
        # best_agent = self.rename_blank(best_agent)

        self.best_error_train = best_agent.error
        if config.SELECT:
            best_agent.compute_fitness(self.fake_test)
            self.best_error_fake = best_agent.error
        self.print_agent(best_agent, config.FINAL_VERBOSE)

        if config.EXPORT:
            self.log["final"]["graph"] = best_agent.obj.convert_to_AF().R
            self.export()

        return best_agent.error, self.best_error_train, self.best_error_fake, best_agent.obj.size()

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
            # self.agents[i].obj.convert_to_AF().print_attacks()
        if save_best_agent:
            self.agents[0] = cp.deepcopy(best_agent)

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
            self.agents[0] = cp.deepcopy(best_agent)

    def cross_over(self, percent=10, save_best_agent=False):
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
            rand_arg = sn.pick(new_agent_arguments)
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

    def cross_over_2(self, percent=10, save_best_agent=False):
        if save_best_agent:
            best_agent = cp.deepcopy(self.agents[0])
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
            # parent_1 = sn.pick(self.agents)
            # parent_2 = sn.pick(self.agents)

            parent_1 = self.agents[i]
            parent_2 = self.agents[count - i - 1]
            new_agent = cp.deepcopy(parent_1)
            new_agent.obj.recombination(parent_1.obj, parent_2.obj)

            new_agents.append(cp.deepcopy(new_agent))

        for i, a in enumerate(new_agents):
            self.agents[- i - 1] = cp.deepcopy(a)

        if save_best_agent:
            self.agents[0] = cp.deepcopy(best_agent)

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
            if config.SA and self.sa_select():
                new_agents.append(cp.deepcopy(sn.pick(self.agents)))
            else:
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
            self.agents[0] = cp.deepcopy(best_agent)

    def compute_fitness(self, verbose=False):
        best_e = None
        for i in range(len(self.agents)):
            value = self.agents[i].compute_fitness(self.training_data,
                                                   self.reduce,
                                                   verbose)
            if best_e is None or value < best_e:
                best_e = value
            verbose = False
        self.last_best = self.best_error_bis
        self.delta_e = self.last_best - best_e
        self.best_error_bis = min(best_e, self.best_error_bis)
        # print(self.delta_e, best_e, self.last_best)

    def unique_test(self, args, attacks, data):
        agent = Agent()
        agent.init(args, attacks)
        agent.compute_fitness(data)
        print("Error:", agent.error)

    def sa_update_seq(self, delta_e):
        if delta_e <= config.EPSILON_E:
            self.seq += 1
        else:
            self.seq = 0
        self.sa_update_heat()

    def sa_update_heat(self):
        if self.seq >= config.MAX_SEQ:
            self.heat = self.heat * config.LAMBDA
            if self.heat < 1:
                self.heat = 0

    def sa_select(self):
        return self.heat >= 1 and rd.randint(0, 99) < self.heat


def is_blank(node_name):
    return len(node_name) > 1 and node_name[0] == 'b' and \
           node_name[1] in string.digits
