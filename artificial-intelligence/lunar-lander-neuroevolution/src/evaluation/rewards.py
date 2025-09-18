import config as cfg
import numpy as np

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
