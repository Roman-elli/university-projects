import config as cfg
from engine.simulation import simulate
from policies.agent import *

def main():
    success = 0.0
    steps = 0.0

    for i in range(cfg.EPISODES):
        if(not cfg.ENABLE_WIND): st, su = simulate(steps=1000000, policy=agent_no_wind)
        else: st, su = simulate(steps=1000000, policy=agent_wind)

        if su:
            steps += st
        success += su
        
        if su>0:
            print('Average number of successful landings:', steps/success*100)
        print(': Success rate:', success/(i+1)*100)

if __name__ == "__main__":
   main()