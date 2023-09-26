import sys
import getopt


# core params ------------------------------------------------------------------

STEPS = 200
POPULATION = 10

EXTENSION = "g"  # preferred=p ; grounded=g

TARGET = 'T'

# variant params ---------------------------------------------------------------
MAX_R_SIZE = 16  # max attack relation count in the graph
INCREASE = False  # progressively increases the limit
INCREASE_STEP = 50
INCREASE_VALUE = 1

TOP = 'Top'
GLOBAL_TOP = True  # Top argument attacking target (Top -> T)
LOCAL_TOP = False  # Top argument for each argument (arg -> t_arg)
AND = False  # Add "And" nodes

MULTI_VALUE = False  # handled multi-valued attributes, but less efficient

REDUCE = 30
FORCE_REDUCE = True  # try to reduce the size of the graph
STRONGER = False  # increases the mutation intensity if stuck for a long time
NO_OVERFIT = True

NEGATION = False  # depreciated, use LOCAL_TOP instead

SA = False  # Simulating Annealing - affect the selection rule
HEAT = 100
LAMBDA = 0.95
EPSILON_E = 1
MAX_SEQ = 5

SELECT = False


# Genetic Algorithm params -----------------------------------------------------
MUTATIONS_INTENSITY = 2  # default 4
HEAVY_MUTATIONS_INTENSITY = 0  # default 10
HEAVY_MUTATIONS_PERCENT = 10
CROSSOVER_PERCENT = 100
SAVE_BEST_AGENT = True  # default True

# dataset params ---------------------------------------------------------------
# 0: mushroom
# 1: voting
# 2: breast-cancer
# 3: heart-disease
# 4: car (unbalanced)
# 5: breast-cancer-wisconsin
# 6: balloons
# 7: tic-tac-toe
# 8: monks-1
# 9: adult  # wip
# 10: marco law dataset
DATASET = 4
TRAIN_DATA_RATIO = 0.7
TEST_DATA_SIZE = 10_000
BALANCE = 0.3
NOISE = 0  # percent -> 10%, 20%, ...
NUMERICAL = 10  # numerical attributes separations
IGNORE_UNKNOWN = True
SEED = None
PATH = "./src/datasets"

# verbose params ---------------------------------------------------------------

TRAIN_DATA_VERBOSE = True
TEST_DATA_VERBOSE = True
LEARNING_VERBOSE = 1
FINAL_VERBOSE = 3
EXPORT = True
EXPORT_LOC = "output/"


def init(argv):

    try:
        opts, args = getopt.getopt(argv,
                                   "e:d:r:m:h:x:t:n:i:p:s:",
                                   ["reduce", "negation", "topg", "topl", "sa", "path"])
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
              '--negation'
              '--topg'
              '--topl'
              '--sa'
              '--path <dataset_root_path>')
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
        elif opt == '--topg':
            global GLOBAL_TOP
            GLOBAL_TOP = True
        elif opt == '--topl':
            global LOCAL_TOP
            LOCAL_TOP = True
        elif opt == '--sa':
            global SA
            SA = True
        elif opt == '--path':
            global PATH
            PATH = arg
