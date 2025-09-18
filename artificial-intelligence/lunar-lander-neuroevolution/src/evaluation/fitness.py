import numpy as np
import config as cfg

from evaluation.rewards import *

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
