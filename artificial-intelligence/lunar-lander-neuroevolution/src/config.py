# =============================
# ENVIRONMENT CONFIG
# =============================
ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = None  # 'human' (play visible simulation)
STEPS = 500

# =============================
# EVOLUTION SETTINGS
# =============================
EVOLVE = True
EPISODES = 1000
TESTS = 5
N_TESTS = 1000

SEEDS = [
    964, 952, 364, 913, 140, 726, 112, 631, 881, 844,
    965, 672, 335, 611, 457, 591, 551, 538, 673, 437,
    513, 893, 709, 489, 788, 709, 751, 467, 596, 976
]

# =============================
# NEURAL NETWORK ARCHITECTURE
# =============================
N_INPUTS = 8
N_OUTPUTS = 2
SHAPE = (N_INPUTS, 12, N_OUTPUTS)
GENOTYPE_SIZE = 0

# =============================
# GENETIC ALGORITHM
# =============================
POPULATION_SIZE = 100
NUMBER_OF_GENERATIONS = 100
PROB_CROSSOVER = 0.9
PROB_MUTATION = 0.05
STD_DEV = 0.1
ELITE_SIZE = 1

# =============================
# THRESHOLDS
# =============================
THRESHOLD_THETA = 20
THRESHOLD_THETA_EXTREME = 90
THRESHOLD_VY = -0.07
THRESHOLD_Y = 0.5
THRESHOLD_X = 0.5
THRESHOLD_X_EXTREME = 0.005

# =============================
# FITNESS WEIGHTS
# =============================
DISTANCE_WEIGHT = 0.4
VELOCITY_WEIGHT = 0.6
THETA_WEIGHT = 0.4
CONTACT_LEFT_RIGHT = 0.7
REWARD_SUCCESS = 0
