from utils import get_subtables, formalize_rules, is_mono
from c45 import gain
import random as rd
import copy as cp
from tqdm import tqdm
import time

basestring = ""


def mine_c45(table, result):
    """ An entry point for C45 algorithm.

        _table_ - a dict representing data table in the following format:
        {
            "<column name>': [<column values>],
            "<column name>': [<column values>],
            ...
        }

        _result_: a string representing a name of column indicating a result.
    """
    col = max([(k, gain(table, k, result)) for k in table.keys() if k != result],
              key=lambda x: x[1])[0]
    tree = []
    for subt in get_subtables(table, col):
        v = subt[col][0]
        if is_mono(subt[result]):
            tree.append(['%s=%s' % (col, v),
                         '%s=%s' % (result, subt[result][0])])
        else:
            del subt[col]
            tree.append(['%s=%s' % (col, v)] + mine_c45(subt, result))
    return tree

def tree_to_rules(tree):
    return formalize_rules(__tree_to_rules(tree))


def __tree_to_rules(tree, rule=''):
    rules = []
    for node in tree:
        if True or isinstance(node, basestring):
            rule += node + ','
        else:
            rules += __tree_to_rules(node, rule)
    if rules:
        return rules
    return [rule]


def validate_table(table):
    assert isinstance(table, dict)
    for k, v in table.items():
        assert k
        #assert isinstance(k, basestring)
        assert len(v) == len(table.values()[0])
        for i in v: assert i


def get_size(tree):
    size = 0
    if type(tree[-1]) == str:
        return 1
    else:
        for index in range(len(tree)):
            size += get_size(tree[index])
    return size

def rearrange_numerical_values(values, num):

    v = cp.deepcopy(values)

    min_max = dict()
    for name in num:
        min_max[name] = [None, None]
    key = list(v.keys())[0]
    length = len(v[key])
    #print(v.keys())
    for i in range(length):
        for name in num:
            if v[name][i] != '?':
                value = float(v[name][i])
                if min_max[name][0] is None or value < min_max[name][0]:  # min
                    min_max[name][0] = value
                if min_max[name][1] is None or value > min_max[name][1]:  # max
                    min_max[name][1] = value

    for i in range(length):
        for name in num:
            if v[name][i] != '?':
                value = float(v[name][i])
                mod = (min_max[name][1] - min_max[name][0]) / 10
                v[name][i] = str(int((value - min_max[name][0]) / mod) + min_max[name][0])

    return v


def predict(tree, names, values):
    node = None
    if type(tree[-1]) == str:
        return tree[0]
    else:
        for index in range(len(tree)):
            k, v = tree[index][0].split(',')[0].split('=')
            pos = names.index(k)
            value = values[pos]
            if v == value:
                tree[index].pop(0)
                node = tree[index]
                break
    if node is None:
        index = rd.randint(0, len(tree) - 1)
        tree[index].pop(0)
        node = tree[index]
        #return "Fail"
    return predict(node, names, values)


def run_data(filename, names_param, reverse=False, ratio=0.7, agg=None, num=[]):

    file = open(filename)
    file.seek(0)
    line = file.readline()
    t = dict()
    test = dict()
    for n in names_param:
        t[n] = []
    for n in names_param:
        test[n] = []

    while line:
        values = line.split(',')
        if rd.randint(1, 100) < 100 * (1 - ratio):
            for i, v in enumerate(values):
                test[names_param[i]].append(v)
        else:
            for i, v in enumerate(values):
                t[names_param[i]].append(v)
        line = file.readline()
    file.close()

    t = rearrange_numerical_values(t, num)
    test = rearrange_numerical_values(test, num)

    tree = None
    if reverse:
        tree = mine_c45(t, names_param[0])
    else:
        tree = mine_c45(t, names_param[-1])
    #print(tree)
    # rules = tree_to_rules(tree)
    # for r in rules:
    #    print(r)

    predictions = [0, 0, 0]

    for i in range(len(test[names_param[-1]]) - 1):
        values = []
        for n in names_param:
            values.append(test[n][i])
        # print("restart", values)
        res = predict(cp.deepcopy(tree), names_param, values)
        # break
        #print(values, "===>", res, )
        if res == "Fail":
            predictions[2] += 1
        else:
            label = res.split('=')[1]
            val = values[-1]
            if reverse:
                val = values[0]
            label = label.replace("\n", "")
            val = val.replace("\n", "")
            if agg is not None:
                label = agg[label]
                val = agg[val]
            labels = [val]
            if label in labels:
                predictions[0] += 1
            else:
                predictions[1] += 1
    #print(predictions)
    #print(predictions, " Acc=", 100 * predictions[0] / sum(predictions))

    return [predictions, 100 * predictions[0] / sum(predictions)], get_size(tree)


def multiple_run(file, names_param, reverse=False, ratio=0.7, agg=None, num=[]):

    orig_name = cp.deepcopy(names_param)

    scores = []
    t_start = time.time()
    avg_size = 0

    count = 1#20

    for i in tqdm(range(count)):
        names_param = cp.deepcopy(orig_name)
        score, size = run_data(file, names_param, reverse, ratio, agg, num)
        avg_size += size
        scores.append(score[1])

    avg_size /= count
    avg_time = (time.time() - t_start) / count

    return sum(scores) / len(scores), min(scores), max(scores), avg_size, avg_time  # avg, min, max, avg_size


if __name__ == "__main__":

    num = []
    aggregate = dict()

    filename = "datasets/car/car.data.txt"
    names = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "acceptability"]
    aggregate["vgood"] = "vgood"
    aggregate["good"] = "other"
    aggregate["acc"] = "other"
    aggregate["unacc"] = "other"
    #print(multiple_run(filename, names, False, 0.7, aggregate))

    filename = "datasets/mushroom/agaricus-lepiota.data.txt"
    names = ["edible", "cap-shape", "cap-surface", "cap-color", "bruises?", "odor", "gill-attachement", "gill_spacing", "gill-size", "gill-color", "stalk-shape", "stalk-root", "stalk-surface-above-ring", "stalk-surface-below-ring", "stalk-color-above-ring", "stalk-color-below-ring", "veil-type", "veil-color", "ring-number", "ring-type", "spore-print-color", "population", "habitat"]
    #print(multiple_run(filename, names, True, 0.5))

    filename = "datasets/voting/house-votes-84.data.txt"
    names = ["parti", "handicapped-infants", "water-project-cost-sharing", "adoption-of-the-budget-resolution", "physician-fee-freeze", "el-salvador-aid", "religious-groups-in-schools", "anti-satellite-test-ban", "aid-to-nicaraguan-contras", "mx-missile", "immigration", "synfuels-corporation-cutback", "education-spending", "superfund-right-to-sue", "crime", "duty-free-exports", "export-administration-act-south-africa"]
    #print(multiple_run(filename, names, True, 0.7))

    filename = "datasets/heart-disease/processed.cleveland.data.txt"
    names = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]
    aggregate["0"] = "0"
    aggregate["1"] = "1"
    aggregate["2"] = "1"
    aggregate["3"] = "1"
    aggregate["4"] = "1"
    num = ["age",
               "trestbps",
               "chol",
               "thalach",
               "oldpeak"]
    #print(multiple_run(filename, names, False, 0.7, aggregate, num))
    filename = "datasets/breast-cancer-wisconsin/breast-cancer-wisconsin.data.txt"
    names = ["clump-thickness", "uniformity-of-cell-size", "uniformity-of-cell-shape", "marginal-adhesion", "single-epithelial-cell-size", "bare-nuclei", "bland-chromatin",
             "normal-nucleoli", "mitoses", "benign(2)"]
    num = ["clump-thickness",
           "uniformity-of-cell-size",
           "uniformity-of-cell-shape",
           "marginal-adhesion",
           "single-epithelial-cell-size",
           "bare-nuclei",
           "bland-chromatin",
           "normal-nucleoli",
           "mitoses"]
    #print(multiple_run(filename, names, False, 0.7, None, num))

    filename = "datasets/breast-cancer/breast-cancer.data.txt"
    names = ["class", "age", "menopause",
             "tumor-size", "inv-nodes",
             "node-caps", "deg-malig", "breast",
             "breast-quad", "irradiat"]
    #print(multiple_run(filename, names, True, 0.7))  # not working

    filename = "datasets/iris/iris.data"
    names = ["sepal-length", "sepal-width", "petal-length", "petal-width", "class"]

    aggregate["Iris-virginica"] = "Iris-virginica"
    aggregate["Iris-versicolor"] = "other"
    aggregate["Iris-setosa"] = "other"
    num = ["sepal-length", "sepal-width", "petal-length", "petal-width"]
    #print(multiple_run(filename, names, False, 0.7, aggregate, num))

    filename = "datasets/wine/wine.data"
    names = ["class", "alcohol", "malic-acid", "ash", "alcalinity-of-ash", "magnesium", "total-phenols", "flavanoids", "nonflavanoid-phenols", "proanthocyanins", "color-intensity", "hue", "od280/od315-of-diluted-wines", "proline"]
    num = ["alcohol", "malic-acid", "ash", "alcalinity-of-ash", "magnesium", "total-phenols", "flavanoids", "nonflavanoid-phenols", "proanthocyanins", "color-intensity", "hue", "od280/od315-of-diluted-wines", "proline"]
    print(multiple_run(filename, names, True, 0.7, None, num))

