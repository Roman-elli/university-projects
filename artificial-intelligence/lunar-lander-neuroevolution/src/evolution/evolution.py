import os
import random
import config as cfg

from evolution.population import *
from evaluation.environment import evaluate
from multiprocessing import Process, Queue

# Proccess initiation
NUM_PROCESSES = os.cpu_count()
evaluationQueue = Queue()
evaluatedQueue = Queue()

for i in range(1, len(cfg.SHAPE)):
    cfg.GENOTYPE_SIZE += cfg.SHAPE[i-1]*cfg.SHAPE[i]


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
