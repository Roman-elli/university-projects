
# =============================
# NeuroEvolution start setup
# =============================
# CONFIG
ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = None # RENDER_MODE = 'human' for a graphic demonstration of each test
EPISODES = 1000
STEPS = 500

nInputs = 8
nOutputs = 2
SHAPE = (nInputs,12,nOutputs)
GENOTYPE_SIZE = 0

POPULATION_SIZE = 100
NUMBER_OF_GENERATIONS = 100

PROB_CROSSOVER = 0.9

PROB_MUTATION = 0.05
STD_DEV = 0.1

ELITE_SIZE = 1

# =============================
# Thresholds
# =============================
THRESHOLD_THETA = 20
THRESHOLD_THETA_EXTREME = 90
THRESHOLD_VY = -0.07
THRESHOLD_Y = 0.5
THRESHOLD_X = 0.5
THRESHOLD_X_EXTREME = 0.005

# =============================
# Weights
# =============================
distance_weight = 0.4
velocity_weight = 0.6
theta_weight = 0.4
contact_left_rigth = 0.7
reward_sucess = 0