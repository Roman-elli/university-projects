import random
import os
import config as cfg

from evolution.evolution import evolution
from utils.io import *
from evaluation.environment import simulate

def main():
    os.makedirs("data", exist_ok=True)
    
    if cfg.EVOLVE:
        for i in range(cfg.Tests):    
            random.seed(cfg.SEEDS[i])
            bests = evolution()
            save_bests(bests, f"data/log{i}.txt")
        
    else:
        # validate individual
        for i in range(cfg.Tests):
            bests = load_bests(f'data/log{i}.txt')
            b = bests[-1]
            cfg.SHAPE = b[1]
            ind = b[2]
                
            ind = {'genotype': ind, 'fitness': None}
            fit, success = 0, 0

            for i in range(1,cfg.ntests+1):
                f, s = simulate(ind['genotype'], render_mode=cfg.RENDER_MODE, seed = None)
                fit += f
                success += s
                
            print(f"Fitness: {fit/cfg.ntests:.1f}, Success: {success/cfg.ntests * 100:.1f}%")

if __name__ == '__main__':
    main()
    