import random
import copy
import numpy as np
import gymnasium as gym 
import os
import config as cfg

from multiprocessing import Process, Queue

# Proccess initiation
NUM_PROCESSES = os.cpu_count()
evaluationQueue = Queue()
evaluatedQueue = Queue()

for i in range(1, len(cfg.SHAPE)):
    cfg.GENOTYPE_SIZE += cfg.SHAPE[i-1]*cfg.SHAPE[i]

def network(shape, observation,ind):
    #Computes the output of the neural network given the observation and the genotype
    x = observation[:]
    for i in range(1,len(shape)):
        y = np.zeros(shape[i])
        for j in range(shape[i]):
            for k in range(len(x)):
                y[j] += x[k]*ind[k+j*len(x)]
        x = np.tanh(y)
    return x

def check_successful_landing(observation):
    #Checks the success of the landing based on the observation
    x = observation[0]
    vy = observation[3]
    theta = observation[4]
    contact_left = observation[6]
    contact_right = observation[7]

    legs_touching = contact_left == 1 and contact_right == 1

    on_landing_pad = abs(x) <= 0.2

    stable_velocity = vy > -0.2
    stable_orientation = abs(theta) < np.deg2rad(20)
    stable = stable_velocity and stable_orientation
 
    if legs_touching and on_landing_pad and stable:
        return True
    return False

# Reward functions
def landed(contact_left, contact_right):
    return contact_left == 1 and contact_right == 1

# Reward for successful landing
def reward_landing(contact_left, contact_right):
    return 50 if landed(contact_left, contact_right) else 0

# Reward for the ship approaching the landing zone
def reward_approaching_zone(x, y, vy, theta):
    if y <= cfg.THRESHOLD_Y and abs(x) <= cfg.THRESHOLD_X and vy > cfg.THRESHOLD_VY and abs(theta) < np.deg2rad(cfg.THRESHOLD_THETA):
        return 100
    return 0

# Reward for the ship being about to land
def reward_close_to_zone(x, y, vy, theta):
    if y <= cfg.THRESHOLD_Y * 0.2 and abs(x) <= cfg.THRESHOLD_X * 0.2 and vy > cfg.THRESHOLD_VY * (-1.3) and abs(theta) < np.deg2rad(cfg.THRESHOLD_THETA - 5):
        return 500
    return 0

# Reward for successful landing within expected limits
def reward_perfect_landing(x, vy, theta, contact_left, contact_right):
    if landed(contact_left, contact_right) and abs(x) <= cfg.THRESHOLD_X_EXTREME and vy > cfg.THRESHOLD_VY * 0.005 and abs(theta) < np.deg2rad(cfg.THRESHOLD_THETA - 10):
        return 2300
    return 0

# Reward for the ship being centered
def reward_centering(x, vx):
    if (x > cfg.THRESHOLD_X and vx < 0) or (x < cfg.THRESHOLD_X_EXTREME and vx > 0):
        return 800
    return 0

# Reward for the ship being well positioned vertically
def reward_vertical_alignment(x, theta):
    if abs(x) < cfg.THRESHOLD_X * 0.2 and abs(theta) < np.deg2rad(cfg.THRESHOLD_THETA - 15):
        return 800
    return 0

# Functions for penalties
# Penalty for the ship being far from the landing zone
def penalty_far_from_zone(x, y, vx):
    if y < 1 and ((x > cfg.THRESHOLD_X * 0.2 and vx > 0) or (x < -cfg.THRESHOLD_X * 0.2 and vx < 0)):
        return 1000
    return 0

# Penalty for the ship being at too steep an angle to the ground
def penalty_extreme_angle(theta):
    if abs(theta) > np.deg2rad(cfg.THRESHOLD_THETA_EXTREME):
        return 1000
    return 0

def objective_function(observation):
    
    x = observation[0]
    y = observation[1]
    vx = observation[2]
    vy = observation[3]
    theta = observation[4]
    contact_left = observation[6]
    contact_right = observation[7]

    # Penalties:
    penalty_xy = abs(x) + abs(y) + penalty_far_from_zone(x, y, vx)
    penalty_vy = abs(vy)
    penalty_theta = abs(theta) + penalty_extreme_angle(theta)

    # Rewards:
    reward_success = (
        reward_landing(contact_left, contact_right)
        + reward_approaching_zone(x, y, vy, theta)
        + reward_close_to_zone(x, y, vy, theta)
        + reward_perfect_landing(x, vy, theta, contact_left, contact_right)
        + reward_centering(x, vx)
        + reward_vertical_alignment(x, theta)
    )

    # Fitness
    fitness = (
        - cfg.distance_weight * penalty_xy
        - cfg.velocity_weight * penalty_vy
        - cfg.theta_weight * penalty_theta
        + cfg.contact_left_rigth * reward_success
    )

    return fitness, check_successful_landing(observation)

def simulate(genotype, render_mode = None, seed=None, env = None):
    # Simulates an episode of Lunar Lander, evaluating an individual
    env_was_none = env is None
    if env is None:
        env = gym.make("LunarLander-v3", render_mode =render_mode, 
        continuous=True, gravity=cfg.GRAVITY, 
        enable_wind=cfg.ENABLE_WIND, wind_power=cfg.WIND_POWER, 
        turbulence_power=cfg.TURBULENCE_POWER)    
        
    observation, info = env.reset(seed=seed)

    for _ in range(cfg.STEPS):
        prev_observation = observation
        # Chooses an action based on the individual's genotype
        action = network(cfg.SHAPE, observation, genotype)
        observation, reward, terminated, truncated, info = env.step(action)        

        if terminated == True or truncated == True:
            break
    
    if env_was_none:    
        env.close()

    return objective_function(prev_observation)

def evaluate(evaluationQueue, evaluatedQueue):
    # Evaluates individuals until it receives None
    # This function runs on multiple processes
    
    env = gym.make("LunarLander-v3", render_mode =None, 
        continuous=True, gravity=cfg.GRAVITY, 
        enable_wind=cfg.ENABLE_WIND, wind_power=cfg.WIND_POWER, 
        turbulence_power=cfg.TURBULENCE_POWER)    
    while True:
        ind = evaluationQueue.get()

        if ind is None:
            break
            
        ind['fitness'] = simulate(ind['genotype'], seed = None, env = env)[0]
                
        evaluatedQueue.put(ind)
    env.close()
    
def evaluate_population(population):
    # Evaluates a list of individuals using multiple processes
    for i in range(len(population)):
        evaluationQueue.put(population[i])
    new_pop = []
    for i in range(len(population)):
        ind = evaluatedQueue.get()
        new_pop.append(ind)
    return new_pop

def generate_initial_population():
    # Generates the initial population
    population = []
    for i in range(cfg.POPULATION_SIZE):
        # Each individual is a dictionary with a genotype and a fitness value
        # At this time, the fitness value is None
        # The genotype is a list of floats sampled from a uniform distribution between -1 and 1
        
        genotype = []
        for j in range(cfg.GENOTYPE_SIZE):
            genotype += [random.uniform(-1,1)]
        population.append({'genotype': genotype, 'fitness': None})
    return population

def parent_selection(population):
    choice = 5  # Tournament size
    individuals = random.sample(population, choice)  # Randomly selects ‘choice’ individuals from the population
    individuals.sort(key=lambda x: x['fitness'], reverse=True)  # Sort individuals by 'fitness'
    return copy.deepcopy(individuals[0])  # Returns the best individual in the tournament

def crossover(p1, p2):
    offspring = {'genotype': [], 'fitness': None}  # The child's genotype will be a list.
    for i in range(cfg.GENOTYPE_SIZE):  # Go through all the genes
        if random.random() < 0.5:  # 50% chance of inheriting from each parent
            offspring['genotype'].append(p1['genotype'][i])
        else:
            offspring['genotype'].append(p2['genotype'][i])

    return offspring

def mutation(p):
    # Creates a copy of the individual's genotype to avoid modifying the original directly
    new_genotype = p['genotype'].copy()
    
    # For each gene, with a probability of mutation (cfg.PROB_MUTATION)
    for i in range(cfg.GENOTYPE_SIZE):
        if random.random() < cfg.PROB_MUTATION:  # Decide whether the gene will be mutated
            # Gene alteration, here we use a normal distribution with mean 0 and standard deviation cfg.STD_DEV
            new_genotype[i] += random.gauss(0, cfg.STD_DEV)
            
            # Limits the value of the gene to be within the range [-1, 1]
            new_genotype[i] = max(-1, min(1, new_genotype[i]))
    
    genotype_mutation = {'genotype': new_genotype, 'fitness': None}
    
    # Returns the new individual with the mutated genotype
    return genotype_mutation
   
def survival_selection(population, offspring):
    # Reevaluation of the elite
    offspring.sort(key = lambda x: x['fitness'], reverse=True)
    p = evaluate_population(population[:cfg.ELITE_SIZE])
    new_population = p + offspring[cfg.ELITE_SIZE:]
    new_population.sort(key = lambda x: x['fitness'], reverse=True)
    return new_population    
        
def evolution():
    # Create evaluation processes
    evaluation_processes = []
    for i in range(NUM_PROCESSES):
        evaluation_processes.append(Process(target=evaluate, args=(evaluationQueue, evaluatedQueue)))
        evaluation_processes[-1].start()
    
    # Create initial population
    bests = []
    population = list(generate_initial_population())
    population = evaluate_population(population)
    population.sort(key = lambda x: x['fitness'], reverse=True)
    best = (population[0]['genotype']), population[0]['fitness']
    bests.append(best)
    
    # Iterate over generations
    for gen in range(cfg.NUMBER_OF_GENERATIONS):
        offspring = []
        
        # create offspring
        while len(offspring) < cfg.POPULATION_SIZE:
            if random.random() < cfg.PROB_CROSSOVER:
                p1 = parent_selection(population)
                p2 = parent_selection(population)
                ni = crossover(p1, p2)

            else:
                ni = parent_selection(population)
                
            ni = mutation(ni)
            offspring.append(ni)
            
        # Evaluate offspring
        offspring = evaluate_population(offspring)

        # Apply survival selection
        population = survival_selection(population, offspring)
        
        # Print and save the best of the current generation
        best = (population[0]['genotype']), population[0]['fitness']
        bests.append(best)
        print(f'Best of generation {gen}: {best[1]}')

    # Stop evaluation processes
    for i in range(NUM_PROCESSES):
        evaluationQueue.put(None)
    for p in evaluation_processes:
        p.join()
        
    # Return the list of bests
    return bests

def load_bests(fname):
    # Load bests from file
    bests = []
    with open(fname, 'r') as f:
        for line in f:
            fitness, shape, genotype = line.split('\t')
            bests.append(( eval(fitness),eval(shape), eval(genotype)))
    return bests

def main():
    evolve = True # evolve = False
    render_mode = None
    Testes = 5
    if evolve:
        seeds = [964, 952, 364, 913, 140, 726, 112, 631, 881, 844, 965, 672, 335, 611, 457, 591, 551, 538, 673, 437, 513, 893, 709, 489, 788, 709, 751, 467, 596, 976]
        for i in range(Testes):    
            random.seed(seeds[i])
            bests = evolution()
            with open(f'log{i}.txt', 'w') as f:
                for b in bests:
                    f.write(f'{b[1]}\t{cfg.SHAPE}\t{b[0]}\n')

                
    else:
        # validate individual
        for i in range(Testes):
            bests = load_bests(f'log{i}.txt')
            b = bests[-1]
            cfg.SHAPE = b[1]
            ind = b[2]
                
            ind = {'genotype': ind, 'fitness': None}
                
                
            ntests = 1000

            fit, success = 0, 0
            for i in range(1,ntests+1):
                f, s = simulate(ind['genotype'], render_mode=render_mode, seed = None)
                fit += f
                success += s
            print(f"Fitness: {fit/ntests:.1f}, Success: {success/ntests * 100:.1f}%")

if __name__ == '__main__':
    main()
    