import gymnasium as gym 
import config as cfg

from evaluation.fitness import network, objective_function
from evolution.evolution import evaluationQueue, evaluatedQueue

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

   