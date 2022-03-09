import sys
import getopt


STEPS = 100
POPULATION = 10

EXTENSION = "g"  # preferred=p ; grounded=g
MAX_R_SIZE = None
INCREASE = False
INCREASE_STEP = 50
INCREASE_VALUE = 1
TARGET = 'T'
REDUCE = 30
FORCE_REDUCE = True
NEGATION = False

MUTATIONS_INTENSITY = 4
HEAVY_MUTATIONS_INTENSITY = 10
HEAVY_MUTATIONS_PERCENT = 10
CROSSOVER_PERCENT = 10
SAVE_BEST_AGENT = True

# 0: mushroom
# 1: voting
# 2: breast-cancer
# 3: heart-disease
# 4: car (unbalanced)
# 5: breast-cancer-wisconsin
# 6: balloons
# 7: tic-tac-toe
DATASET = 4
TRAIN_DATA_RATIO = 0.7
TEST_DATA_SIZE = 10_000
BALANCE = 0.3
NOISE = 0  # percent -> 10%, 20%, ...
NUMERICAL = 10  # numerical attributes separations
IGNORE_UNKNOWN = True

TRAIN_DATA_VERBOSE = False
TEST_DATA_VERBOSE = False
LEARNING_VERBOSE = 0
FINAL_VERBOSE = 3
EXPORT = False
EXPORT_LOC = "output/"


def init(argv):

    try:
        opts, args = getopt.getopt(argv,
                                   "e:d:r:m:h:x:t:n:i:p:s:",
                                   ["reduce", "negation"])
    except getopt.GetoptError:
        print('main.py'
              '-e <export_file>'
              '-d <dataset>'
              '-r <max_size>'
              '-m <mutation_intensity>'
              '-h <heavy_mutation_intensity'
              '-x <extension>'
              '-t <train_test_ratio>'
              '-n <noise_percent>'
              '-i <numerical_interpolation>'
              '-p <population_size>'
              '-s <steps>'
              '--reduce'
              '--negation')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-e':
            global EXPORT_LOC
            EXPORT_LOC = arg
        elif opt == '-d':
            global DATASET
            DATASET = int(arg)
        elif opt == '-r':
            global MAX_R_SIZE
            MAX_R_SIZE = int(arg)
        elif opt == '-m':
            global MUTATIONS_INTENSITY
            MUTATIONS_INTENSITY = int(arg)
        elif opt == '-h':
            global HEAVY_MUTATIONS_INTENSITY
            HEAVY_MUTATIONS_INTENSITY = int(arg)
        elif opt == '-x':
            global EXTENSION
            EXTENSION = arg
        elif opt == '-t':
            global TRAIN_DATA_RATIO
            TRAIN_DATA_RATIO = float(arg)
        elif opt == '-n':
            global NOISE
            NOISE = int(arg)
        elif opt == '-i':
            global NUMERICAL
            NUMERICAL = int(arg)
        elif opt == '-p':
            global POPULATION
            POPULATION = int(arg)
        elif opt == '-s':
            global STEPS
            STEPS = int(arg)
        elif opt == '--reduce':
            global REDUCE
            REDUCE = True
        elif opt == '--negation':
            global NEGATION
            NEGATION = True
