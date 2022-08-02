import random as rd
import string
import config
import copy as cp


class Rules:

    def __init__(self):
        self.a = dict()  # axioms
        for a in string.ascii_lowercase:
            self.a[a] = False

    def random_init_atoms(self):
        for a in string.ascii_lowercase:
            self.a[a] = bool(rd.randint(0, 1))

    def compute(self, facts):
        self.set_facts(facts)
        return self.formula_7()  # choose the formula to use here

    def set_facts(self, facts):
        for a in string.ascii_lowercase:
            self.a[a] = False if a not in facts else True

    def formula_1(self):
        return (self.a['a'] and not (self.a['b'] or self.a['c'])) or (
                self.a['e'] and (not self.a['f'] or self.a['d']))

    def formula_2(self):
        return not self.a['a'] and not self.a['c'] and not self.a['d']

    def formula_3(self):
        return (not self.a['b'] and not self.a['d']) or self.a['c']

    def formula_4(self):
        return (self.a['a'] and not (self.a['b'] or self.a['c'])) or self.a['e']

    def formula_5(self):
        return self.a['a']

    def formula_6(self):
        return ((self.a['a'] and not self.a['b']) or not self.a['c']) and (
                not (self.a['e'] and not self.a['d']) and self.a['f'])

    def formula_7(self):
        return ((self.a['a'] and not self.a['b']) or not self.a['c']) and (
                not (self.a['e'] and not self.a['d']) and self.a['f']) or \
               (self.a['a'] and self.a['o'] and not self.a['m']) or \
               ((not (self.a['g'] and self.a['i'])) and
                (not self.a['j'] and self.a['n']))

    def formula_8(self):
        return ((self.a['a'] and self.a['b']) or not self.a['c']) and (
                not (self.a['e'] and self.a['d']) and not self.a['f']) or \
               (self.a['a'] and self.a['g'] and not self.a['h']) and \
               (self.a['i'] or self.a['j'])

    def prison_kill(self):
        """
        Is he guilt AND go to jail?
        a: killed someone
        b: defence
        c: has judiciary antecedents
        d: suspicious defence
        e: the suspect is dead
        f: killed nobody in judiciary antecedents
        """
        return (self.a['a'] and not self.a['f']) and \
               (not self.a['b'] or self.a['d']) and \
               self.a['c'] and not self.a['e']

    def car_break(self):
        """
        Should the car break?
        a: someone will cross the road
        b: he is not moving and looking the car
        c: he is at the middle of the road
        d: car has the place to dodge on sides
        e: a car or other persons are on the sides
        f: someone is sticking behind
        g: there is no alternative hurting less people (i.e. should not break)
        h: it is too late to break (too close)
        """
        return self.a['a'] and (not self.a['b'] or self.a['c']) and \
               (not self.a['d'] or self.a['e']) and \
               (not self.a['f']) and \
               (not self.a['g']) and \
               (not self.a['h'])

    def image_classifier(self):
        """
        Is this a bee?
        a: it is yellow
        b: it has no black strip
        c: it is bigger than a bee
        d: is has 8 legs
        e: it has at least 6 legs
        f: it has wings
        g: it makes honey
        h: it has green eyes
        i: sun is making eyes look the wrong color
        j: it eats bees
        """
        return self.a['a'] and not self.a['b'] and not self.a['d'] and \
               self.a['e'] and self.a['f'] and self.a['g'] and \
               (not self.a['h'] or self.a['i']) and \
               not (self.a['j'] and self.a['c'])

    def xor(self):
        return (self.a['a'] and not self.a['b']) \
               or (not self.a['a'] and self.a['b'])

    def nand(self):
        return not (self.a['a'] and self.a['b'])

    def a_and(self):
        return not (self.a['a'] and self.a['b'])

    def generate_data(self, possible, count=100, balance=100, verbose=False,
                      noise_percent=0):
        data = []
        poss_count = 0
        tolerance = balance / 100
        noise_count = 0
        for p in possible:
            if not (p[0] == 'b' and len(p) > 1):
                poss_count += 1
        step = 0
        t_f_count = [0, 0]
        while step < count:
            facts = []
            for p in possible:
                if rd.randint(0, 1) == 0 or p[0] == 'b' and len(p) > 1:
                    facts.append(p)
            value = self.compute(facts)

            true_value = value
            if rd.randint(0, 99) < noise_percent:
                value = not value
                noise_count += 1

            if true_value:
                t_f_count[0] += 1
            else:
                t_f_count[1] += 1

            t = (step, facts, value)
            if true_value and t_f_count[0] <= tolerance * count:
                data.append(t)
            elif not true_value and t_f_count[1] <= tolerance * count:
                data.append(t)
            else:
                step -= 1
                if true_value != value:
                    noise_count -= 1
            step += 1

        if verbose:
            true_count = 0
            for d in data:
                if d[2]:
                    true_count += 1
            print("----------- Dataset info: -----------")
            print("Input size:", len(possible))
            print("States count:", 2 ** poss_count)
            print("Object count:", len(data))
            print("True count:", true_count,
                  "(" + str(100 * true_count / len(data)) + "%)")
            print("False count:", len(data) - true_count,
                  "(" + str(100 * (len(data) - true_count) / len(data)) + "%)")
            print("Noise count:", noise_count,
                  "(" + str(100 * noise_count / len(data)) + "%)")
            print("-------------------------------------")
        return data

    def balancing(self, data, true_count, adding=True):
        dataset = cp.deepcopy(data)
        b_inf = config.BALANCE
        b_sup = 1 - b_inf
        ratio = true_count / len(dataset)
        if config.TEST_DATA_VERBOSE:
            print("Balance: " + str(int(100 * ratio)) + "%/" +
                  str(int(100 * (1 - ratio))) + "% to ", end='')
        while not b_inf <= true_count / len(dataset) <= b_sup:
            rand = rd.randint(0, len(dataset) - 1)
            if true_count / len(dataset) < b_inf and dataset[rand][-1]:
                if adding:
                    dataset.append(cp.deepcopy(dataset[rand]))
                else:
                    rand_2 = rd.randint(0, len(dataset) - 1)
                    true_count -= int(dataset[rand_2][-1])
                    dataset[rand_2] = dataset[rand]
                true_count += 1

            elif true_count / len(dataset) > b_sup and not dataset[rand][-1]:
                if adding:
                    dataset.append(cp.deepcopy(dataset[rand]))
                else:
                    rand_2 = rd.randint(0, len(dataset) - 1)
                    true_count -= int(dataset[rand_2][-1])
                    dataset[rand_2] = dataset[rand]

        ratio = true_count / len(dataset)
        if config.TEST_DATA_VERBOSE:
            print(str(int(100 * ratio)) + "%/" +
                  str(int(100 * (1 - ratio))) + "%")
        return dataset, true_count

    def attributes_to_arg(self, f, attributes, num, ignore,
                          l_index=0, sep=','):
        data = dict()
        att_val = dict()
        for a in attributes:
            att_val[a] = []
        args = []
        step = 0
        for line in f:
            step += 1
            value = line.split(sep)
            value[-1] = value[-1].replace('\n', '')
            if value[0] == "":
                value.pop(0)
            new_value = []
            for i, v in enumerate(value):
                if i not in ignore:
                    new_value.append(cp.deepcopy(v))
            value = new_value
            label = value.pop(l_index)

            for i, v in enumerate(value):
                pair = attributes[i] + "=" + v
                if v not in att_val[attributes[i]] and v != '?':
                    att_val[attributes[i]].append(v)
                value[i] = attributes[i] + "=" + v  # to fill the dataset tuples
                if pair not in args and v != '?':  # ? <=> missing data
                    args.append(pair)
            data[tuple(value + [str(step)])] = label

        if num is not None:  # re-arrange numerical attributes
            old = cp.deepcopy(data)
            data.clear()
            bounds = dict()
            for a in num:
                bounds[a] = [None, None, None]  # [min, max]
            for k in old.keys():
                for i, att in enumerate(attributes):
                    if att in num:
                        chain = k[i].split('=')
                        if chain[-1] == '?':
                            continue
                        att_name = chain[0] + '='
                        value = float(chain[-1])
                        # replace the min
                        if None not in bounds[att]:
                            bounds[att] = [min(value, bounds[att][0]),
                                           max(value, bounds[att][1])]
                        else:
                            bounds[att] = [value, value]

            for k in old.keys():
                new_k = list(k)
                for i, att in enumerate(attributes):
                    if att in num:
                        chain = k[i].split('=')
                        if chain[-1] == '?':
                            continue
                        att_name = chain[0] + '='
                        value = float(chain[-1])
                        new_value = bounds[att][0]
                        add = (bounds[att][1] - bounds[att][0]) \
                              / config.NUMERICAL
                        old_k = float(new_k[i].split('=')[-1])
                        while old_k > new_value + add:
                            new_value += add
                        new_k[i] = att_name + str(round(new_value, 4)) + "-" \
                                   + str(round(new_value + add, 4))
                data[tuple(new_k)] = old[k]

            args.clear()

            for k in data.keys():
                for i in range(len(k) - 1):
                    if k[i] not in args:
                        if not config.IGNORE_UNKNOWN or \
                                k[i].split('=')[-1] != '?':
                            args.append(k[i])

        if config.AND:
            args.append("And_1")
            args.append("And_2")
            args.append("And_3")

        if not config.NEGATION:
            return data, args

        final_data = dict()
        for k in data.keys():
            key_value = list(k)
            step = key_value.pop(-1)
            for a in attributes:
                for v in att_val[a]:
                    if str(a + "=" + v) not in key_value:
                        key_value.append(str("not-" + a + "=" + v))
                    if str("not-" + a + "=" + v) not in args:
                        if not config.IGNORE_UNKNOWN or v != '?':
                            args.append(str("not-" + a + "=" + v))
            final_data[tuple(key_value + [str(step)])] = data[k]

        return final_data, args

    def generate_dataset(self, ratio, data, label_name, noise_percent, balance):
        probability = int(ratio * 100)
        dataset = []
        test_data = []
        true_count = 0
        noise_count = 0
        keys = list(data.keys())

        for c in range(len(data)):
            k = keys[c]
            label_value = False
            if type(label_name) == str:
                label_value = data[k] == label_name
            elif type(label_name) == list:
                label_value = data[k] in label_name
            input_attr = list(k)
            input_attr.pop(-1)
            if (rd.randint(0, 99) < probability and
                len(dataset) <= ratio * len(data)) or \
                    len(test_data) > (1 - ratio) * len(data):
                if rd.randint(0, 99) < noise_percent:
                    label_value = not label_value
                    noise_count += 1
                true_count += int(label_value)
                dataset.append((c, input_attr, label_value))
            else:
                test_data.append((c, input_attr, label_value))

        if balance:
            dataset, true_count = self.balancing(dataset, true_count)

        return dataset, test_data, true_count, noise_count

    def load(self, f, attributes_names, num, ignore,
             l_index, ratio, label, noise, balance):

        ignore = sorted(ignore, reverse=True)

        data, args = self.attributes_to_arg(f, attributes_names, num, ignore,
                                            l_index)

        dataset, test_data, true_count, noise_count = self \
            .generate_dataset(ratio,
                              data,
                              label,
                              noise,
                              balance)
        print("Args =", args)

        fake_test = []
        if config.SELECT:
            tmp_data = cp.deepcopy(dataset)
            rd.shuffle(tmp_data)
            split = int(0.7 * len(tmp_data))
            dataset = tmp_data[:split]
            fake_test = tmp_data[split:]

        return dataset, test_data, true_count, noise_count, args, fake_test

    def load_both(self, f_train, f_test, attributes_names, num, ignore,
                  l_index, label, noise, balance, sep=','):
        ignore = sorted(ignore, reverse=True)

        data_train, args = self.attributes_to_arg(f_train, attributes_names, num, ignore,
                                            l_index, sep)
        data_test, args = self.attributes_to_arg(f_test, attributes_names,
                                                  num, ignore,
                                                  l_index, sep)

        dataset, _, true_count, noise_count = self \
            .generate_dataset(1,
                              data_train,
                              label,
                              noise,
                              balance)
        test_data, _, true_count, noise_count = self \
            .generate_dataset(1,
                              data_test,
                              label,
                              noise,
                              balance)
        print("Args =", args)
        return dataset, test_data, true_count, noise_count, args

    def print_dataset_info(self, dataset, true_count, args, noise_count):
        print("----------- Dataset info: -----------")
        print("Input size:", len(args))
        print("Object count:", len(dataset))
        print("True count:", true_count,
              "(" + str(100 * true_count / len(dataset)) + "%)")
        print("False count:", len(dataset) - true_count,
              "(" + str(
                  100 * (len(dataset) - true_count) / len(dataset)) + "%)")
        print("Noise count:", noise_count,
              "(" + str(100 * noise_count / len(dataset)) + "%)")
        print("-------------------------------------")

    def load_dataset_mushroom(self, ratio=0.7, noise_percent=0, balance=False):
        # True == Edible, False == Poisonous
        # train = 3988
        label_name = "e"
        l_index = 0
        attributes_names = ["cap-shape",
                            "cap-surface",
                            "cap-color",
                            "bruises?",
                            "odor",
                            "gill-attachment",
                            "gill-spacing",
                            "gill-size",
                            "gill-color",
                            "stalk-shape",
                            "stalk-root",
                            "stalk-surface-above-ring",
                            "stalk-surface-below-ring",
                            "stalk-color-above-ring",
                            "stalk-color-below-ring",
                            "veil-type",
                            "veil-color",
                            "ring-number",
                            "ring-type",
                            "spore-print-color",
                            "population",
                            "habitat"]
        num = []
        ignore = []
        f = open("datasets/mushroom/agaricus-lepiota.data.txt")

        dataset, test_data, true_count, noise_count, args, fake_test = self.load(
            f, attributes_names, num, ignore,
            l_index, ratio, label_name, noise_percent, balance)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args, fake_test

    def load_dataset_voting(self, ratio=0.7, noise_percent=0, balance=False):
        # True == democrat, False == republican
        # train = 300
        label_name = "democrat"
        l_index = 0
        attributes_names = ["handicapped-infants",
                            "water-project-cost-sharing",
                            "adoption-of-the-budget-resolution",
                            "physician-fee-freeze",
                            "el-salvador-aid",
                            "religious-groups-in-schools",
                            "anti-satellite-test-ban",
                            "aid-to-nicaraguan-contras",
                            "mx-missile",
                            "immigration",
                            "synfuels-corporation-cutback",
                            "education-spending",
                            "superfund-right-to-sue",
                            "crime",
                            "duty-free-exports",
                            "export-administration-act-south-africa"]
        num = []
        ignore = []
        f = open("datasets/voting/house-votes-84.data.txt")

        dataset, test_data, true_count, noise_count, args, fake_test = self.load(
            f, attributes_names, num, ignore,
            l_index, ratio, label_name, noise_percent, balance)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args, fake_test

    def load_dataset_breast_cancer(self, ratio=0.7, noise_percent=0,
                                   balance=False):
        # True == recurrence-events, False == no-recurrence-events
        # train = 70%
        label_name = "recurrence-events"
        l_index = 0
        attributes_names = ["age",
                            "menopause",
                            "tumor-size",
                            "inv-nodes",
                            "node-caps",
                            "deg-malig",
                            "breast",
                            "breast-quad",
                            "irradiat"]
        num = []
        ignore = []
        f = open("datasets/breast-cancer/breast-cancer.data.txt")

        dataset, test_data, true_count, noise_count, args, fake_test = self.load(
            f, attributes_names, num, ignore,
            l_index, ratio, label_name, noise_percent, balance)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args, fake_test

    def load_dataset_heart_disease(self, ratio=0.7, noise_percent=0,
                                   balance=False):
        # True == 0 (no disease), False == 1, 2, 3
        # train = 70%
        label_name = "0"
        l_index = -1
        attributes_names = ["age",
                            "sex",
                            "cp",
                            "trestbps",
                            "chol",
                            "fbs",
                            "restecg",
                            "thalach",
                            "exang",
                            "oldpeak",
                            "slope",
                            "ca",
                            "thal"]
        num = ["age",
               "trestbps",
               "chol",
               "thalach",
               "oldpeak"]
        ignore = []
        f = open("datasets/heart-disease/processed.cleveland.data.txt")

        dataset, test_data, true_count, noise_count, args, fake_test = self.load(
            f, attributes_names, num, ignore,
            l_index, ratio, label_name, noise_percent, balance)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args, fake_test

    def load_dataset_car(self, ratio=0.7, noise_percent=0, balance=False):
        # True == acc (acceptable), False == unacc, good, vgood
        # train = 70%
        label_name = ["vgood"]
        l_index = -1
        attributes_names = ["buying",
                            "maint",
                            "doors",
                            "persons",
                            "lug_boot",
                            "safety"]
        num = []
        ignore = []
        f = open("datasets/car/car.data.txt")

        dataset, test_data, true_count, noise_count, args, fake_test = self.load(
            f, attributes_names, num, ignore,
            l_index, ratio, label_name, noise_percent, balance)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args, fake_test

    def load_dataset_breast_cancer_wisconsin(self, ratio=0.7, noise_percent=0,
                                             balance=False):
        # True == 4 (malignant), False == 2 (benign)
        # train = 70%
        label_name = "2"
        l_index = -1
        attributes_names = ["clump-thickness",
                            "uniformity-of-cell-size",
                            "uniformity-of-cell-shape",
                            "marginal-adhesion",
                            "single-epithelial-cell-size",
                            "bare-nuclei",
                            "bland-chromatin",
                            "normal-nucleoli",
                            "mitoses"]
        num = ["clump-thickness",
               "uniformity-of-cell-size",
               "uniformity-of-cell-shape",
               "marginal-adhesion",
               "single-epithelial-cell-size",
               "bare-nuclei",
               "bland-chromatin",
               "normal-nucleoli",
               "mitoses"]
        ignore = [0]
        f = open(
            "datasets/breast-cancer-wisconsin/breast-cancer-wisconsin.data.txt")

        dataset, test_data, true_count, noise_count, args, fake_test = self.load(
            f, attributes_names, num, ignore,
            l_index, ratio, label_name, noise_percent, balance)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args, fake_test

    def load_dataset_balloons(self, ratio=0.7, noise_percent=0, balance=False):
        # True == T, False == F
        # train = 100%
        label_name = "T"
        l_index = -1
        attributes_names = ["color",
                            "size",
                            "act",
                            "age"]
        num = []
        ignore = []
        f = open("datasets/balloons/yellow-small+adult-stretch.data.txt")

        dataset, test_data, true_count, noise_count, args, fake_test = self.load(
            f, attributes_names, num, ignore,
            l_index, ratio, label_name, noise_percent, balance)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args, fake_test

    def load_dataset_tic_tac_toe(self, ratio=0.7, noise_percent=0,
                                 balance=False):
        # True == negative (x player can't win), False == positive
        # train = 70%
        label_name = "negative"
        l_index = -1
        attributes_names = ["top-left-square",
                            "top-middle-square",
                            "top-right-square",
                            "middle-left-square",
                            "middle-middle-square",
                            "middle-right-square",
                            "bottom-left-square",
                            "bottom-middle-square",
                            "bottom-right-square"]
        num = []
        ignore = []
        f = open("datasets/tic-tac-toe/tic-tac-toe.data.txt")

        dataset, test_data, true_count, noise_count, args, fake_test = self.load(
            f, attributes_names, num, ignore,
            l_index, ratio, label_name, noise_percent, balance)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args, fake_test

    def load_dataset_monk_1(self, ratio=0.7, noise_percent=0, balance=False):
        # True == (a1 == a2) or (a5 == 1)
        # train = 70%
        label_name = "1"
        l_index = 0
        attributes_names = ["a1",
                            "a2",
                            "a3",
                            "a4",
                            "a5",
                            "a6"]
        num = []
        ignore = [7]
        sep = ' '
        f_train = open("datasets/monks-1/monks-1.train.txt")
        f_test = open("datasets/monks-1/monks-1.test.txt")

        dataset, test_data, true_count, noise_count, args = self.load_both(
            f_train, f_test, attributes_names, num, ignore,
            l_index, label_name, noise_percent, balance, sep)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args

    def load_dataset_adult(self, ratio=0.1, noise_percent=0, balance=False):
        # True == T, False == F
        # train = 100%
        label_name = ">50K"
        l_index = -1
        attributes_names = ["age",
                            "workclass",
                            "education",
                            "marital-status",
                            "occupation",
                            "relationship",
                            "race",
                            "sex",
                            "hours-per-week",
                            "native-country"]
        num = ["age", "hours-per-week"]
        ignore = [2, 4, 10, 11]
        f = open("datasets/adult/adult_small.data.txt")

        dataset, test_data, true_count, noise_count, args, fake_test = self.load(
            f, attributes_names, num, ignore,
            l_index, ratio, label_name, noise_percent, balance)

        if config.TEST_DATA_VERBOSE:
            self.print_dataset_info(dataset, true_count, args, noise_count)
        if config.TRAIN_DATA_VERBOSE:
            true_count = 0
            for d in test_data:
                true_count += int(d[-1])
            self.print_dataset_info(test_data, true_count, args, 0)

        return dataset, test_data, args, fake_test