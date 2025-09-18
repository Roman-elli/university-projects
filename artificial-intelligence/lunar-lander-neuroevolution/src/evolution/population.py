import random
import config as cfg
import copy

from evaluation.environment import evaluate_population

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
   