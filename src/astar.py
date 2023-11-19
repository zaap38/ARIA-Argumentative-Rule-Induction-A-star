import copy as cp
import af
import rules
import config
import random as rd
from tqdm import tqdm
from time import time
import numpy as np


class Tic:

    def __init__(self, name="", precision=2, disabled=False) -> None:
        self.time = time()
        self.name = name
        if name != "" and not disabled:
            print("Start:", name)
        self.disabled = disabled
        self.precision = precision

    def tic(self, name=""):
        if self.disabled:
            return
        if name == "":
            name = self.name
        t = time()
        print("End:", self.name, "in", round(t - self.time, self.precision), "s")
        print("Start:", name)
        self.name = name
        self.time = t


class Node:

    def __init__(self):
        self.obj = None
        self.distance = None
        self.color = 0
        self.to_check = []  # remaining lines of the dataset to fix
        self.incorrect_lines = []
        self.addon = ('', '')

    def compute_distance(self, data):
        # print(">>>", len(self.to_check))
        self.distance = 0
        dist = 0
        tic.disabled = True
        tic.tic("To check")
        if len(self.to_check) > 0:
            dist, self.incorrect_lines = self.obj.convert_to_AF().get_dist(data, self.to_check)
        # print(dist, len(self.to_check))
        if len(self.to_check) > 0 and dist == len(self.to_check):
            self.distance = len(data) + 1
        else:
            tic.tic("Comp")
            self.distance = dist
            complementary = []
            for i in range(len(data)):
                if i not in self.to_check:
                    complementary.append(i)
            dist, inc = self.obj.convert_to_AF().get_dist(data, complementary)
            self.distance += dist
            self.incorrect_lines += inc
        tic.disabled = True
        # print(len(self.incorrect_lines), len(data))

        self.distance += len(self.obj.convert_to_AF().R) / 1000

    def compute_distance_all(self, data):
        self.distance, self.incorrect_lines = self.obj.convert_to_AF().get_dist(data)


class AStar:

    def __init__(self, data, args, test):
        self.nodes = []
        self.queue = []
        self.data = data
        self.test_data = test
        self.args = args
        self.tried = []

    def select_node(self):
        node = None
        best = 0
        if len(self.queue) == 0:
            return None
        for i, n in enumerate(self.queue):
            if node is None or n.distance < node.distance:
                node = n
                best = i
        self.queue.pop(best)
        node.color = 2
        # print("select", node.distance, len(self.queue))
        # print(min([n.distance for n in self.queue], default=0))
        tic.tic("Add neighbours")
        self.add_neighbours_to_queue(node)
        self.nodes.append(node)
        return node

    def add_neighbours_to_queue(self, node):
        # possible = node.obj.compute_possible_attacks()
        tic.tic("Compute possible attacks")
        possible = node.obj.compute_v2().tolist()

        # for p in tqdm(possible):
        for p in possible:
            new_R = cp.deepcopy(node.obj.R)
            new_R[p] = 1
            #if not self.exist(new_R):
            # tic.disabled = False
            tic.tic("attack checked")
            if not self.attack_checked((p, 0)):
                tic.tic("make node")
                new_node = self.make_node(node.incorrect_lines, new_R)
                tic.tic("get attack")
                new_node.addon = node.obj.get_attack(p)
                self.tried.append((p, abs(new_node.distance - node.distance)))
                new_node.color = 1
                self.queue.append(new_node)

    def exist(self, R):
        for n in self.nodes:
            if n.obj.R == R:
                return True
        return False
    
    def attack_checked(self, t):
        return t in self.tried

    def get_best_node(self):
        node = None
        # print("-----")
        for n in self.nodes:
            # print(n.distance)
            if node is None or n.distance < node.distance:
                node = n
        # print(">>>", node.distance)
        return node
    
    def make_node(self, to_check=[], R=None):
        tic.disabled = True
        tic.tic("Make node")
        node = Node()
        node.obj = af.EncodedAF()
        node.obj.init(self.args)
        if R is not None:
            node.obj.R = R
        tic.tic("Copy")
        node.to_check = cp.deepcopy(to_check)
        tic.tic("Distance")
        node.compute_distance(self.data)
        tic.disabled = True
        return node

    def run(self, max_loop=None):
        good = True
        count = 0
        tic.tic("Make first node")
        self.queue = [self.make_node()]
        tic.tic("Start loop")
        while good:
            tic.tic("Select node")
            current = self.select_node()
            # print("Queue dist:", [(n.addon, n.distance) for n in self.queue])
            if count % 1 == 0 and count > 0:
                print("Step:", count, end=' | ')
                print("Error:", self.get_best_node().distance, "/", len(self.data), "| Acc.:" ,
                      round(100 - (100 * self.get_best_node().distance / len(self.data)), 2), "%")
            if current is None:
                break
            good = current.distance >= 1

            count += 1
            if max_loop is not None and count >= max_loop:
                good = False
        print("===Done===")
        best_node = self.get_best_node()
        best_node.obj.convert_to_AF().print_attacks()
        best_node.compute_distance_all(self.data)
        print("Error Train:", best_node.distance, "/", len(self.data), "|" , round(100 * best_node.distance / len(self.data), 2), "%")
        best_node.compute_distance_all(self.test_data)
        print("Error Test:", best_node.distance, "/", len(self.test_data), "|" , round(100 * best_node.distance / len(self.test_data), 2), "%")


if __name__ == "__main__":

    # dataset params ---------------------------------------------------------------
    # 0: mushroom
    # 1: voting
    # 2: breast-cancer
    # 3: heart-disease #2506: 78.41 ; 1301: 83.84 ; 9201: 74.73
    # 4: car (unbalanced) #2506: xx ; #1003: 98.62 ; 1301: 98.11
    # 5: breast-cancer-wisconsin
    # 6: balloons
    # 7: tic-tac-toe
    # 8: monks-1
    # 9: adult  # wip
    # 10: marco law dataset
    # 11: art

    seed = 1002
    rd.seed(seed)

    start_time = time()
    
    tic = Tic("Load dataset")
    tic.disabled = True

    r = rules.Rules()
    train, test, args, _ = r.load_dataset(0, 0.05, seed)
    # train = train + test
    if config.GLOBAL_TOP:
        args = [config.TOP] + args
    args = [config.TARGET] + args

    tic.tic("AStar start")

    astar = AStar(train, args, test)
    astar.run(20)

    end_time = time()
    minutes, seconds = divmod(end_time - start_time, 60)
    print("Time:", round(minutes), "min", round(seconds), "s | ", round(end_time - start_time, 2), "s")

