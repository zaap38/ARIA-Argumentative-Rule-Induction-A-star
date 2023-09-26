import random as rd
import copy as cp
import config
import snippets as sn
import networkx as nx


class Argument:

    def __init__(self, name):
        self.name = name  # name to identify (str)
        self.alive = True


class AF:

    def __init__(self):
        self.A = []  # str()
        self.R = []  # 0: no attack ; 1: attack ; None: forbidden attack
        self.changes = []
        self.G = nx.DiGraph()

        # access to attack (a, b) -> self.R[index_a * len(self.A) + index_b]

    def init(self, arguments):
        self.A = cp.deepcopy(arguments)
        # arg 0 and 1 are Target and Top
        self.G.add_node(0, name=config.TARGET, value=False, edit=False)
        self.G.add_node(1, name=config.TOP, value=False, edit=False)
        self.G.add_edge(1, 0, id=1)
        # print(arguments)
        for i, a in enumerate(arguments):
            self.G.add_node(len(self.G), name=a, value=False, edit=True)
            # print(i + 2, self.G.nodes[i + 2])

    def get_attribute(self, arg):
        return arg.split('=')[0]

    def random_init(self):
        self.random_change()

    def compute_possible_changes(self):
        self.changes = []
        for i in range(len(self.A)):
            if self.is_attacker(self.A[i]):
                self.changes.append(i)
        self.changes.append(self.A.index(config.TARGET))

    def is_attacker(self, a):
        offset = self.A.index(a) * len(self.A)
        for i in range(len(self.A)):
            if self.R[offset + i] not in [0, None]:
                return True
        return False

    def attack_index(self, t):
        a = t[0]
        b = t[1]
        if a != config.TARGET and a != config.TOP and is_top(a):
            a = a[len(config.TOP) + 1:]
        return self.A.index(a) * len(self.A) + self.A.index(b)

    def attack_is_possible(self, a, b=None):
        # does not look at symmetrical attack
        # a and b are ids. a can be a tuple
        if b is None:
            b = a[1]
            a = a[0]
        return self.G.nodes[a]["edit"] and a != b

    def random_change(self):
        a = rd.randint(0, len(self.G) - 1)  # a attack b
        b = rd.choice([n for n in self.G if len(self.G.__getitem__(n)) > 0])
        if self.attack_is_possible(a, b):
            if self.G.has_edge(a, b):
                self.remove_attack(a, b)
            elif self.G.has_edge(b, a):
                value = self.G.get_edge_data(a, b, id)
                self.G.remove_edge(b, a)
                self.G.add_edge(a, b, id=value)
            elif config.MAX_R_SIZE is None or config.MAX_R_SIZE > len(self.get_R()):
                self.add_attack(a, b)
        # print(self.get_R())


    def recombination(self, graph_a, graph_b):
        # make it PMX friendly
        # TODO
        arg = rd.choice(graph_a.A)
        attacks = []
        for i in range(len(graph_b.R)):
            if arg in graph_b.R[i]:
                attacks.append(cp.deepcopy(graph_b.R[i]))
        new_R = attacks
        for i in range(len(graph_b.R)):
            if arg not in graph_b.R[i]:
                new_R.append(cp.deepcopy(graph_b.R[i]))
        graph_a.R = new_R
        return graph_a

    def add_attack(self, a, b=None):
        if b is None:
            b = a[1]
            a = a[0]
        self.G.add_edge(a, b, id=len(self.G.edges()) + 1)

    def size(self):
        return len(self.G.edges())

    def reduce_size(self, max_size):
        count = self.size() - max_size
        for i in range(len(self.R)):
            if self.get_attack(i)[0] != config.TARGET and self.get_attack(i)[0]\
                    != config.TOP and self.R[i] in [-1, 1]:
                self.R[i] = 0
                count -= 1
                if count < 0:
                    break

    def get_R(self):
        r = []
        for e in self.G.edges:
            r.append((self.G.nodes[e[0]]["name"], self.G.nodes[e[1]]["name"]))
        return r

    def polish(self):
        """
        Remove non-connect, symmetrical and useless attack relations.
        :return:
        """
        # remove symmetrical attacks
        for a in self.A:
            for b in self.A:
                if self.is_attacking(a, b) and self.is_attacking(b, a):
                    self.remove_attack(a, b)
                    self.remove_attack(b, a)

        # remove useless and non-connect attacks
        stop = False
        attacking_t = [config.TARGET, config.TOP]
        while not stop:
            stop = True
            for a in self.A:
                if a not in attacking_t:
                    for b in attacking_t:
                        if self.is_attacking(a, b):
                            stop = False
                            attacking_t.append(a)
                            break

        for i in range(len(self.R)):
            a, b = self.get_attack(i)
            if a not in attacking_t or b not in attacking_t or \
                    (self.is_attacking(a, config.TARGET) and
                     b != config.TARGET):
                self.remove_attack(a, b)

    def remove_attack(self, a, b=None):
        if b is None:
            b = a[1]
            a = a[0]
        value = self.G.get_edge_data(a, b, id)
        self.G.remove_edge(a, b)
        for e, _, i in self.G.edges(data=id):
            if i == self.size() + 1:
                e[id] = value

    def getSuccessors(self, n):
        nei = []
        for e in self.G.edges:
            if e[0] == n:
                nei.append(e[1])
        return nei

    def hasSuccessor(self, n):
        for e in self.G.edges:
            if n == e[0]:
                return True
        return False

    def getPredecessors(self, n):
        nei = []
        for e in self.G.edges:
            if e[1] == n:
                nei.append(e[0])
        return nei

    def compute_grounded(self, facts, fast_mode=False):
        # fast mod computes only until the target is IN or OUT
        # print(facts)
        facts += [config.TARGET, config.TOP]
        for n in self.G.nodes():
            self.G.nodes[n]["value"] = None if self.G.nodes[n]["name"] in facts else False
            #print(self.G.nodes[n]["name"], self.G.nodes[n]['value'])
        good = True
        # print("vvvvv")
        # print(self.get_R())
        while good:
            good = False
            for n in self.G.nodes:
                if self.G.nodes[n]["value"] is None and \
                        (self.hasSuccessor(n) or self.G.nodes[n]["name"] == config.TARGET):
                    # print(self.G.nodes[n]["name"])
                    # for ni in self.G.nodes:
                        # print(self.G.nodes[ni])
                    pred_out = True
                    # print(self.G.nodes[n]["name"], self.getPredecessors(n))
                    for pred in self.getPredecessors(n):  # check all pred are OUT
                        # print(">>>", self.G.nodes[pred]["name"], self.G.nodes[pred]["value"])
                        if self.G.nodes[pred]["value"] != False:
                            pred_out = False
                            break
                    if pred_out:
                        #print("ok")
                        self.G.nodes[n]["value"] = True
                        for nei in self.getSuccessors(n):
                            #print(self.G.nodes[n]["name"], self.G.nodes[nei]["name"])
                            self.G.nodes[nei]["value"] = False
                            if fast_mode and self.G.nodes[nei]["name"] == config.TARGET:  # stop computation if fast_mod and Target OUT
                                return
                        good = True
                        break
        # print(">>>", self.G.nodes[self.get_argument_by_name(config.TARGET)]["value"])

    def alive(self, a):
        n = cp.deepcopy(a)
        if type(a) == str:
            n = self.get_argument_by_name(a)
        return self.G.nodes[n]["value"]

    def dead(self, a):
        n = cp.deepcopy(a)
        if type(a) == str:
            n = self.get_argument_by_name(a)
        return not self.G.nodes[n]["value"]

    def get_argument_by_name(self, name):
        for n in self.G.nodes():
            if self.G.nodes[n]["name"] == name:
                return n
        return None

    def compare_to_data(self, data, verbose=0, percent=100):
        count = len(data)
        dist = 0
        true_count = 0
        false_count = 0
        true_predicted = 0
        false_predicted = 0
        data_quantity = 0
        for step in range(count):
            if rd.randint(0, 100) <= percent:
                data_quantity += 1
                self.compute_grounded(data[step][1], True)

                value = self.G.nodes[self.get_argument_by_name(config.TARGET)]["value"]
                if value is None:
                    value = False
                true_count += int(data[step][2])
                true_predicted += int(data[step][2] and value)
                false_count += 1 - int(data[step][2])
                false_predicted += int(not data[step][2] and not value)

                dist -= int(value == data[step][2])
        if verbose == 3:
            print("---------")
            print("True accuracy :", str(true_predicted) + "/" + str(true_count)
                  + " (" + str(true_predicted * 100 // max(true_count, 1)) + "%)")
            print("False accuracy:", str(false_predicted) + "/"
                  + str(false_count)
                  + " (" + str(false_predicted * 100 // max(false_count, 1)) + "%)")
        return dist + data_quantity, data_quantity

    def set_R(self, R):
        for r in R:
            self.add_attack(r)



