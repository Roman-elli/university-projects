import random
import copy
import numpy as np
import gymnasium as gym 
import os

from multiprocessing import Process, Queue

# CONFIG
ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = None 
#RENDER_MODE = 'human'
EPISODES = 1000
STEPS = 500

NUM_PROCESSES = os.cpu_count()
evaluationQueue = Queue()
evaluatedQueue = Queue()

nInputs = 8
nOutputs = 2
SHAPE = (nInputs,12,nOutputs)
GENOTYPE_SIZE = 0
for i in range(1, len(SHAPE)):
    GENOTYPE_SIZE += SHAPE[i-1]*SHAPE[i]

POPULATION_SIZE = 100
NUMBER_OF_GENERATIONS = 100

PROB_CROSSOVER = 0.9

PROB_MUTATION = 0.05
STD_DEV = 0.1

ELITE_SIZE = 1

#Limiares
LIMIAR_THETA = 20
LIMIAR_THETA_EXTREMO = 90
LIMIAR_VY = -0.07
LIMIAR_Y = 0.5
LIMIAR_X = 0.5
LIMIAR_X_EXTREMO = 0.005

# Pesos 
distance_weight = 0.4
velocity_weight = 0.6
theta_weight = 0.4
contact_left_rigth = 0.7

reward_sucess = 0

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
import numpy as np

#Funções de recompensa
def landed(contact_left, contact_right):
    return contact_left == 1 and contact_right == 1

#Recompensa pela aterragem bem sucedida
def reward_landing(contact_left, contact_right):
    return 50 if landed(contact_left, contact_right) else 0

#Recompensa pela nave se aproximar da zona de aterragem
def reward_approaching_zone(x, y, vy, theta):
    if y <= LIMIAR_Y and abs(x) <= LIMIAR_X and vy > LIMIAR_VY and abs(theta) < np.deg2rad(LIMIAR_THETA):
        return 100
    return 0

#Recompensa pela nave estar quase a aterrar
def reward_close_to_zone(x, y, vy, theta):
    if y <= LIMIAR_Y * 0.2 and abs(x) <= LIMIAR_X * 0.2 and vy > LIMIAR_VY * (-1.3) and abs(theta) < np.deg2rad(LIMIAR_THETA - 5):
        return 500
    return 0

#Recompensa pela aterragem bem sucedida dentro dos limites esperados
def reward_perfect_landing(x, vy, theta, contact_left, contact_right):
    if landed(contact_left, contact_right) and abs(x) <= LIMIAR_X_EXTREMO and vy > LIMIAR_VY * 0.005 and abs(theta) < np.deg2rad(LIMIAR_THETA - 10):
        return 2300
    return 0

#Recompensa pela nave estar centrada
def reward_centering(x, vx):
    if (x > LIMIAR_X and vx < 0) or (x < LIMIAR_X_EXTREMO and vx > 0):
        return 800
    return 0

#Recompensa pela nave estar bem posicionada verticalmente
def reward_vertical_alignment(x, theta):
    if abs(x) < LIMIAR_X * 0.2 and abs(theta) < np.deg2rad(LIMIAR_THETA - 15):
        return 800
    return 0

#Funções para penalidades
#Penalidade pela nave estar longe da zona de aterragem
def penalty_far_from_zone(x, y, vx):
    if y < 1 and ((x > LIMIAR_X * 0.2 and vx > 0) or (x < -LIMIAR_X * 0.2 and vx < 0)):
        return 1000
    return 0

#Penalidade pela nave estar a um angulo muito acentuado do solo
def penalty_extreme_angle(theta):
    if abs(theta) > np.deg2rad(LIMIAR_THETA_EXTREMO):
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

    # Penalidades:
    penalty_xy = abs(x) + abs(y) + penalty_far_from_zone(x, y, vx)
    penalty_vy = abs(vy)
    penalty_theta = abs(theta) + penalty_extreme_angle(theta)

    # Recompensas:
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
        - distance_weight * penalty_xy
        - velocity_weight * penalty_vy
        - theta_weight * penalty_theta
        + contact_left_rigth * reward_success
    )

    return fitness, check_successful_landing(observation)

def simulate(genotype, render_mode = None, seed=None, env = None):
    #Simulates an episode of Lunar Lander, evaluating an individual
    env_was_none = env is None
    if env is None:
        env = gym.make("LunarLander-v3", render_mode =render_mode, 
        continuous=True, gravity=GRAVITY, 
        enable_wind=ENABLE_WIND, wind_power=WIND_POWER, 
        turbulence_power=TURBULENCE_POWER)    
        
    observation, info = env.reset(seed=seed)

    for _ in range(STEPS):
        prev_observation = observation
        #Chooses an action based on the individual's genotype
        action = network(SHAPE, observation, genotype)
        observation, reward, terminated, truncated, info = env.step(action)        

        if terminated == True or truncated == True:
            break
    
    if env_was_none:    
        env.close()

    return objective_function(prev_observation)

def evaluate(evaluationQueue, evaluatedQueue):
    #Evaluates individuals until it receives None
    #This function runs on multiple processes
    
    env = gym.make("LunarLander-v3", render_mode =None, 
        continuous=True, gravity=GRAVITY, 
        enable_wind=ENABLE_WIND, wind_power=WIND_POWER, 
        turbulence_power=TURBULENCE_POWER)    
    while True:
        ind = evaluationQueue.get()

        if ind is None:
            break
            
        ind['fitness'] = simulate(ind['genotype'], seed = None, env = env)[0]
                
        evaluatedQueue.put(ind)
    env.close()
    
def evaluate_population(population):
    #Evaluates a list of individuals using multiple processes
    for i in range(len(population)):
        evaluationQueue.put(population[i])
    new_pop = []
    for i in range(len(population)):
        ind = evaluatedQueue.get()
        new_pop.append(ind)
    return new_pop

def generate_initial_population():
    #Generates the initial population
    population = []
    for i in range(POPULATION_SIZE):
        #Each individual is a dictionary with a genotype and a fitness value
        #At this time, the fitness value is None
        #The genotype is a list of floats sampled from a uniform distribution between -1 and 1
        
        genotype = []
        for j in range(GENOTYPE_SIZE):
            genotype += [random.uniform(-1,1)]
        population.append({'genotype': genotype, 'fitness': None})
    return population

def parent_selection(population):
    choice = 5  # Tamanho do torneio
    individuals = random.sample(population, choice)  # Seleciona aleatoriamente 'choice' indivíduos da população
    individuals.sort(key=lambda x: x['fitness'], reverse=True)  # Ordena os indivíduos pelo 'fitness'
    return copy.deepcopy(individuals[0])  # Retorna o melhor indivíduo do torneio

def crossover(p1, p2):
    offspring = {'genotype': [], 'fitness': None}  # Genótipo do filho vai ser uma lista
    for i in range(GENOTYPE_SIZE):  # Percorre todos os genes
        if random.random() < 0.5:  # 50% de chance de pegar de cada pai
            offspring['genotype'].append(p1['genotype'][i])
        else:
            offspring['genotype'].append(p2['genotype'][i])

    return offspring

def mutation(p):
    # Cria uma cópia do genótipo do indivíduo para evitar modificar o original diretamente
    new_genotype = p['genotype'].copy()
    
    # Para cada gene, com uma probabilidade de mutação (PROB_MUTATION)
    for i in range(GENOTYPE_SIZE):
        if random.random() < PROB_MUTATION:  # Decide se o gene será mutado
            # Alteração do gene, aqui utilizamos uma distribuição normal com média 0 e desvio padrão STD_DEV
            new_genotype[i] += random.gauss(0, STD_DEV)
            
            # Limita o valor do gene para estar dentro do intervalo [-1, 1]
            new_genotype[i] = max(-1, min(1, new_genotype[i]))
    
    genotype_mutation = {'genotype': new_genotype, 'fitness': None}
    
    # Retorna o novo indivíduo com o genótipo mutado
    return genotype_mutation
 
    
def survival_selection(population, offspring):
    #reevaluation of the elite
    offspring.sort(key = lambda x: x['fitness'], reverse=True)
    p = evaluate_population(population[:ELITE_SIZE])
    new_population = p + offspring[ELITE_SIZE:]
    new_population.sort(key = lambda x: x['fitness'], reverse=True)
    return new_population    
        
def evolution():
    #Create evaluation processes
    evaluation_processes = []
    for i in range(NUM_PROCESSES):
        evaluation_processes.append(Process(target=evaluate, args=(evaluationQueue, evaluatedQueue)))
        evaluation_processes[-1].start()
    
    #Create initial population
    bests = []
    population = list(generate_initial_population())
    population = evaluate_population(population)
    population.sort(key = lambda x: x['fitness'], reverse=True)
    best = (population[0]['genotype']), population[0]['fitness']
    bests.append(best)
    
    #Iterate over generations
    for gen in range(NUMBER_OF_GENERATIONS):
        offspring = []
        
        #create offspring
        while len(offspring) < POPULATION_SIZE:
            if random.random() < PROB_CROSSOVER:
                p1 = parent_selection(population)
                p2 = parent_selection(population)
                ni = crossover(p1, p2)

            else:
                ni = parent_selection(population)
                
            ni = mutation(ni)
            offspring.append(ni)
            
        #Evaluate offspring
        offspring = evaluate_population(offspring)

        #Apply survival selection
        population = survival_selection(population, offspring)
        
        #Print and save the best of the current generation
        best = (population[0]['genotype']), population[0]['fitness']
        bests.append(best)
        print(f'Best of generation {gen}: {best[1]}')

    #Stop evaluation processes
    for i in range(NUM_PROCESSES):
        evaluationQueue.put(None)
    for p in evaluation_processes:
        p.join()
        
    #Return the list of bests
    return bests

def load_bests(fname):
    #Load bests from file
    bests = []
    with open(fname, 'r') as f:
        for line in f:
            fitness, shape, genotype = line.split('\t')
            bests.append(( eval(fitness),eval(shape), eval(genotype)))
    return bests

if __name__ == '__main__':
    
    #evolve = False
    evolve = True
    render_mode = None
    Testes = 5
    if evolve:
        seeds = [964, 952, 364, 913, 140, 726, 112, 631, 881, 844, 965, 672, 335, 611, 457, 591, 551, 538, 673, 437, 513, 893, 709, 489, 788, 709, 751, 467, 596, 976]
        for i in range(Testes):    
            random.seed(seeds[i])
            bests = evolution()
            with open(f'log{i}.txt', 'w') as f:
                for b in bests:
                    f.write(f'{b[1]}\t{SHAPE}\t{b[0]}\n')

                
    else:
        #validate individual
        for i in range(Testes):
            bests = load_bests(f'log{i}.txt')
            b = bests[-1]
            SHAPE = b[1]
            ind = b[2]
                
            ind = {'genotype': ind, 'fitness': None}
                
                
            ntests = 1000

            fit, success = 0, 0
            for i in range(1,ntests+1):
                f, s = simulate(ind['genotype'], render_mode=render_mode, seed = None)
                fit += f
                success += s
            print(f"Fitness: {fit/ntests:.1f}, Success: {success/ntests * 100:.1f}%")
