import random as rd
import copy as cp
import config
import snippets as sn


class Argument:

    def __init__(self, name):
        self.name = name  # name to identify (str)
        self.alive = True


class EncodedAF:

    def __init__(self):
        self.A = []  # str()
        self.R = []  # 0: no attack ; 1: attack ; None: forbidden attack
        self.changes = []

        # access to attack (a, b) -> self.R[index_a * len(self.A) + index_b]

    def init(self, arguments):
        self.A = cp.deepcopy(arguments)
        for i, a in enumerate(self.A):
            for j, b in enumerate(self.A):
                if a == b or \
                        a == "not-" + b or \
                        b == "not-" + a or \
                        a == config.TARGET or \
                        a == config.TOP or \
                        (not config.MULTI_VALUE and
                        self.get_attribute(a) == self.get_attribute(b)):
                    self.R.append(None)
                else:
                    if a == config.TOP and b == config.TARGET:
                        self.R.append(1)
                    else:
                        self.R.append(0)

    def get_attribute(self, arg):
        return arg.split('=')[0]

    def random_init(self):
        attacker = config.TARGET
        base_arg = [config.TARGET]
        if config.GLOBAL_TOP:
            base_arg = base_arg + [config.TOP]
            self.add_attack(config.TOP, config.TARGET)
        while attacker in base_arg:
            # print(self.A)
            attacker = sn.pick(self.A)
        self.add_attack(attacker, sn.pick(base_arg))

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
        if a != config.TARGET and a != config.TOP and a[0] == 'T':
            a = a[2:]
        return self.A.index(a) * len(self.A) + self.A.index(b)

    def attack_is_possible(self, t):
        return self.R[self.attack_index(t)] is not None

    def random_change(self):
        a = None
        b = None

        good = False

        while not good:
            a = sn.pick(self.A)
            b = self.A[sn.pick(self.changes)]
            good = self.attack_is_possible((a, b)) and a != config.TOP and a != config.TARGET
            if config.MAX_R_SIZE is not None and \
                    config.MAX_R_SIZE <= self.size():
                if not self.is_attacking(a, b):
                    good = False
        index = self.attack_index((a, b))
        # self.R[index] = 1 - self.R[index]
        if config.LOCAL_TOP and a != config.TARGET and a != config.TOP:
            if self.R[index] == -1:
                self.R[index] = rd.randint(0, 1)
            elif self.R[index] == 0:
                self.R[index] = -1
                if rd.randint(0, 1) == 1:
                    self.R[index] = 1
            elif self.R[index] == 1:
                self.R[index] = -rd.randint(0, 1)

        else:
            self.R[index] = 1 - self.R[index]
        index_a = self.A.index(a)
        if index_a not in self.changes:
            self.changes.append(index_a)
        else:
            if not self.is_attacker(a):
                self.changes.remove(index_a)

    def recombination(self, graph_a, graph_b):
        new = EncodedAF()
        new.A = cp.deepcopy(graph_a.A)
        new.R = graph_a.R[:len(graph_a.R) // 2] \
            + graph_b.R[len(graph_b.R) // 2:]
        return new

    def convert_to_AF(self):

        af = AF()

        for a in self.A:
            af.A.append(Argument(a))
        # TODO: local top
        """for i in range(len(self.R)):
            if bool(self.R[i]):
                attack = self.get_attack(i)
                af.R.append(attack)"""
        for i in range(len(self.R)):
            if self.R[i] == 1:
                attack = self.get_attack(i)
                af.R.append(attack)

            elif self.R[i] == -1:
                a, b = self.get_attack(i)
                old_a = a
                a = "T_" + a
                if not af.exist(a):
                    af.add_argument(a)
                    attack_local_top = (old_a, a)
                    af.R.append(attack_local_top)
                attack = (a, b)
                af.R.append(attack)

        return af

    def get_attack(self, index):
        a = self.A[index // len(self.A)]
        b = self.A[index % len(self.A)]
        return a, b

    def is_attacking(self, a, b):
        return self.R[self.A.index(a) * len(self.A) + self.A.index(b)]\
               not in [0, None]

    def set_A(self, a):
        self.A = cp.deepcopy(a)

    def set_R(self, r):
        for attack in r:
            self.add_attack_tuple(attack)

    def add_attack(self, a, b):
        self.R[self.A.index(a) * len(self.A) + self.A.index(b)] = 1

    def add_attack_tuple(self, t):
        a = t[0]
        b = t[1]
        self.R[self.A.index(a) * len(self.A) + self.A.index(b)] = 1

    def size(self):
        count = 0
        for v in self.R:
            if bool(v):
                count += 1
        return count

    def reduce_size(self, max_size):
        count = self.size() - max_size
        for i in range(len(self.R)):
            if self.get_attack(i)[0] != config.TARGET and self.get_attack(i)[0]\
                    != config.TOP and self.R[i] in [-1, 1]:
                self.R[i] = 0
                count -= 1
                if count < 0:
                    break

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

    def remove_attack(self, a, b):
        index = self.attack_index((a, b))
        self.R[index] = 0


class AF:

    def __init__(self):
        self.A = []
        self.R = []  # (arg_name, arg_name)

    def add_argument(self, name):
        a = Argument(name)
        self.A.append(a)

    def size(self):
        return len(self.R)

    def add_attack(self, a, b):
        if self.exist(a) and self.exist(b):
            self.R.append((a, b))

    def reduce_size(self, max_size):
        while len(self.R) > max_size:
            self.R.pop(rd.randint(1, len(self.R) - 1))

    def random_change(self, possible):
        a = sn.pick(possible)
        while a == config.TARGET:
            a = sn.pick(possible)
        already_in = []
        for r in self.R:
            if r[0] not in already_in:
                already_in.append(r[0])
        already_in += [config.TARGET]
        b = sn.pick(already_in)
        while a == b:
            b = sn.pick(already_in)
        if self.exist((a, b)):
            self.R.remove((a, b))
        elif self.exist((b, a)):
            self.R.remove((b, a))
        else:
            self.R.append((a, b))

    def random_init(self, possible, count=1):
        for a in possible:
            self.A.append(Argument(a))
        for _ in range(count):
            self.random_change(possible)

    def exist(self, obj):
        if type(obj) == Argument:  # argument
            for a in self.A:
                if a.name == obj.name:
                    return True
        elif type(obj) == str:  # argument name
            for a in self.A:
                if a.name == obj:
                    return True
        elif type(obj) == tuple:  # attack relation
            name_a = obj[0]
            name_b = obj[1]
            if type(name_a) == Argument:
                name_a = name_a.name
            if type(name_b) == Argument:
                name_b = name_b.name
            for r in self.R:
                if r == (name_a, name_b):
                    return True
        else:
            print("Function AF.exist(): Invalid type", str(type(obj)), "!")
            quit()
        return False

    def alive(self, obj):
        name = obj
        if type(name) == Argument:
            name = name.name
        for a in self.A:
            if a.name == name:
                a.alive = True
                return

    def dead(self, obj):
        name = obj
        if type(name) == Argument:
            name = name.name
        for a in self.A:
            if a.name == name:
                a.alive = False
                return

    def print_arg(self):
        to_print = []
        for a in self.A:
            to_print.append(a.name)
        print(to_print)

    def print_attacks(self, graph_R=None):
        if graph_R is None:
            graph_R = self.R
        for r in graph_R:
            attacker = r[0]
            attacked = r[1]
            if attacker[0] == 'T' and attacker != config.TOP:
                attacker = attacker[2:]
                string = attacker + " " + r[1] + " +"
            else:
                string = attacker + " " + r[1]
            if attacked[0] != 'T' or attacked in [config.TOP, config.TARGET]:
                print(string)

    def add(self, element):
        added = False
        if element[1] is None or not self.exist(element[1]):
            self.A.append(Argument(element[0]))
            added = True
        else:
            if not self.exist(element[0]):
                self.A.append(Argument(element[0]))
                added = True
            self.R.append(element)
        return added

    def get_argument_by_name(self, name):
        for i, a in enumerate(self.A):
            if a.name == name:
                return self.A[i]

    def compare_to_data(self, data, ext_choice, verbose=0):
        count = len(data)
        dist = count
        true_count = 0
        false_count = 0
        true_predicted = 0
        false_predicted = 0
        for step in range(count):
            for i, a in enumerate(self.A):
                if a.name in data[step][1] or a.name == config.TOP:
                    self.alive(self.A[i])
                else:
                    self.dead(self.A[i])

            self.compute_graph(data[step][1], ext_choice)

            value = self.get_argument_by_name(config.TARGET).alive

            true_count += int(data[step][2])
            true_predicted += int(data[step][2] and value)
            false_count += 1 - int(data[step][2])
            false_predicted += int(not data[step][2] and not value)

            dist -= int(value == data[step][2])
            if verbose > 0:
                if verbose == 2 or (verbose == 1 and data[step][2] != value):
                    extension = []
                    for a in self.A:
                        if a.alive:
                            extension.append(a.name)
                    print("---------------------------")
                    print("Facts:", data[step][1])
                    print("Extension:", extension)
                    print("Expected:", data[step][2],
                          "Got:", value)
        if verbose == 3:
            print("---------")
            print("True accuracy :", str(true_predicted) + "/" + str(true_count)
                  + " (" + str(true_predicted * 100 // true_count) + "%)")
            print("False accuracy:", str(false_predicted) + "/"
                  + str(false_count)
                  + " (" + str(false_predicted * 100 // false_count) + "%)")

        return dist

    def update_aliveness(self, grounded):
        for i, a in enumerate(self.A):
            if a.name in grounded:
                self.alive(self.A[i])
            else:
                self.dead(self.A[i])

    def is_attacked(self, arg):
        name = arg
        if type(name) == Argument:
            name = name.name
        for r in self.R:
            if r[1] == name:
                return True
        return False

    def attacked_by(self, arg):
        name = arg
        if type(name) == Argument:
            name = name.name
        attacked = []
        for r in self.R:
            if r[0] == name:
                attacked.append(r[1])
        return attacked

    def get_attackers(self, arg):
        name = arg
        if type(name) == Argument:
            name = name.name
        attackers = []
        for r in self.R:
            if r[1] == name:
                attackers.append(r[0])
        return attackers

    def compute_graph(self, facts, extension):
        extension = self.compute_extension(facts, extension)
        self.update_aliveness(extension)

    def compute_extension(self, facts, extension):
        if extension == "p":
            return self.compute_preferred(facts)
        elif extension == "g":
            return self.compute_grounded(facts)

    def grounded_loop_condition(self, d):
        for k in d.keys():
            if d[k] == "undecided":
                valid = True
                attackers = self.get_attackers(k)
                for a in attackers:
                    if d[a] != "out":
                        valid = False
                        break
                if valid:
                    return k

    def compute_grounded(self, facts):
        labels = dict()
        for x in self.A:
            if x.name in facts or x.name in [config.TARGET, config.TOP] or x.name[0] == 'T':
                labels[x.name] = "undecided"
            else:
                labels[x.name] = "out"
        x = self.grounded_loop_condition(labels)
        while x is not None:
            labels[x] = "in"
            attacked = self.attacked_by(x)
            for z in attacked:
                labels[z] = "out"
            x = self.grounded_loop_condition(labels)

        grounded = []
        for x in labels.keys():
            # print(self.nodes[x].name, "is", labels[x])
            if labels[x] == "in":
                grounded.append(x)
        return grounded

    def for_all_eq(self, d, value, not_eq=False):
        if type(value) is not list:
            value = [value]
        for x in d.keys():
            if not_eq:
                if d[x] in value:
                    return False
            else:
                if d[x] not in value:
                    return False
        return True

    def sub_graph_of(self, small, big):
        if len(small) > len(big):
            return False
        for a in small:
            if a not in big:
                return False
        return True

    def compute_preferred(self, facts):
        mu = dict()
        args = []
        for r in self.R:
            if r[0] not in args:
                args.append(r[0])
            if r[1] not in args:
                args.append(r[1])
        activated_args = []
        for a in args:
            if a in facts or a in [config.TARGET, config.TOP] or a[0] == 'T':
                activated_args.append(a)
        for x in activated_args:
            mu[x] = "BLANK"
        p_ext = []
        self.find_preferred_extensions(mu, activated_args, p_ext)

        ext = []
        for a in p_ext[0]:
            in_all = True
            for e in p_ext:
                if a not in e:
                    in_all = False
                    break
            if in_all:
                ext.append(a)

        return ext

    def find_preferred_extensions(self, mu, args, p_ext):
        if self.for_all_eq(mu, ["BLANK", "MUST_OUT"], True):
            s = []
            for y in mu.keys():
                if mu[y] == "IN":
                    s.append(y)
            is_sub = False
            for t in p_ext:
                if self.sub_graph_of(s, t):
                    is_sub = True
                    break
            if not is_sub:
                p_ext.append(cp.deepcopy(s))

        else:
            for x in args:
                if mu[x] == "BLANK":
                    mu_bis = self.in_trans(x, mu, args)
                    self.find_preferred_extensions(mu_bis, args, p_ext)
                    mu_bis = self.undec_trans(x, mu)
                    self.find_preferred_extensions(mu_bis, args, p_ext)
                    break

    def in_trans(self, x, mu, args):
        mu_bis = cp.deepcopy(mu)
        mu_bis[x] = "IN"
        for y in self.attacked_by(x):
            if y in args:
                mu_bis[y] = "OUT"
        for z in self.get_attackers(x):
            if z in args:
                if mu_bis[z] != "OUT":
                    mu_bis[z] = "MUST_OUT"
        return mu_bis

    def undec_trans(self, x, mu):
        mu_bis = cp.deepcopy(mu)
        mu_bis[x] = "UNDEC"
        return mu_bis

    def remove_trash(self):
        attacking = [config.TARGET]
        for r in self.R:
            attacking.append(r[0])
        new_R = cp.deepcopy(self.R)
        for r in self.R:
            if r[1] not in attacking:
                new_R.remove(r)
        self.R = new_R

    def compute_sub_graph(self, attacks, facts):
        new_attacks = []
        nodes = facts + [config.TARGET]
        for r in attacks:
            if (r[0] in nodes or r[0][1] == '0') and \
                    (r[1] in nodes or r[1][1] == '0'):
                new_attacks.append(r)

        final = []
        size = -1
        while size != len(final):
            size = len(final)
            attackers = []
            for r in new_attacks:
                if r[1] == config.TARGET or r[1] in attackers:
                    if r[0] not in attackers:
                        attackers.append(r[0])
                    if r not in final:
                        final.append(r)

        return final
