import gymnasium as gym
import numpy as np
import pygame

ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = 'human'
RENDER_MODE = None # testing scenario
EPISODES = 1000

env = gym.make("LunarLander-v3", render_mode =RENDER_MODE, 
    continuous=True, gravity=GRAVITY, 
    enable_wind=ENABLE_WIND, wind_power=WIND_POWER, 
    turbulence_power=TURBULENCE_POWER)

def check_successful_landing(observation):
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
        print("✅ Successful landing!")
        return True

    print("⚠️ Failed landing!")        
    return False
        
def simulate(steps=1000,seed=None, policy = None):    
    observ, _ = env.reset(seed=seed)
    for step in range(steps):
        action = policy(observ)

        observ, _, term, trunc, _ = env.step(action)

        if term or trunc:
            break

    success = check_successful_landing(observ)
    return step, success

# Perceptions
# Horizontal position relative to the center
def horizontal_position(observation):
    return observation[0]

# Vertical position relative to the center
def vertical_position(observation):
    return observation[1]

# Horizontal velocity
def horizontal_velocity(observation):
    return observation[2]

# Vertical velocity
def vertical_velocity(observation):
    return observation[3]

# Ship orientation
def orientation(observation):
    return observation[4]

# Angle velocity
def angle_velocity(observation):
    return observation[5]

# Left ship foot
def left_foot_touch(observation):
    if (observation[6] == 1): return True
    return False

# Right ship foot
def right_foot_touch(observation):
    if (observation[7] == 1): return True
    return False

# Actions
# Turn the ship to the right with the left engine
def turn_right_with_full_power(action):
    action[1] = 0.8
    return action
def turn_right_with_partial_power(action):
    action[1] = 0.51
    return action

# Turn the ship to the left with the right engine
def turn_left_with_full_power(action):
    action[1] = -0.8
    return action
def turn_left_with_partial_power(action):
    action[1] = -0.51
    return action

# Activate main engine
def main_engine_full_power(action):
    action[0] = 0.9
    return action
def main_engine_parcial_power(action):
    action[0] = 0.51
    return action

# Thresholds defined for the NO wind scenario
ANGLE_THRESHOLD = 0.005
EXTERN_ANGLE_THRESHOLD = 0.053
VERTICAL_VELOCITY_THRESHOLD = -0.07
HORIZONTAL_VELOCITY_THRESHOLD = 0.005
EXTERN_HORIZONTAL_VELOCITY_THRESHOLD = 0.15
HORIZONTAL_THRESHOLD = 0.023

def agent_no_wind(observation):
    action = [0, 0]

    horizontal_vel = horizontal_velocity(observation)
    vertical_vel = vertical_velocity(observation)
    orientation_var = orientation(observation)
    horizontal_pos = horizontal_position(observation)

    # 1. Final case
    # PE, PD -> NIL
    if left_foot_touch(observation) and right_foot_touch(observation):
        return action

    # 2. ABOVE THE EXTERNAL HORIZONTAL SPEED TO THE RIGHT AND CORRECT DEGREE
    # VH > LHE, O < 1.8 * LAE, VV < LV -> GET, MP
    # VH > LHE, O < 1.8 * LAE -> GET
    elif horizontal_vel > EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and orientation_var < 1.8 * EXTERN_ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel > EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and orientation_var < 1.8 * EXTERN_ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 3. ABOVE THE EXTERNAL HORIZONTAL SPEED TO THE RIGHT AND INCORRECT DEGREE
    # VH > LHE, VV < LV -> GDT, MP
    # VH > LHE -> GDT
    elif horizontal_vel > EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel > EXTERN_HORIZONTAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 4. ABOVE THE EXTERNAL HORIZONTAL SPEED TO THE LEFT AND CORRECT DEGREE
    # VH < -LHE, O > -1.8 * LAE, VV < LV -> GDT, MP
    # VH < -LHE, O > -1.8 * LAE -> GDT
    elif horizontal_vel < -EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and orientation_var > -1.8 * EXTERN_ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel < -EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and orientation_var > -1.8 * EXTERN_ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 5. ABOVE THE EXTERNAL HORIZONTAL SPEED TO THE LEFT AND INCORRECT DEGREE
    # VH < -LHE, VV < LV -> GET, MP
    # VH < -LHE -> GET
    elif horizontal_vel < -EXTERN_HORIZONTAL_VELOCITY_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel < -EXTERN_HORIZONTAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 6. OUT OF BOUNDS THE LEFT AND THE RIGHT DEGREE
    # H < -LH, O > -LAE, VV < LV -> GDT, MP
    # H < -LH, O > -LAE -> GDT
    elif horizontal_pos < -HORIZONTAL_THRESHOLD and orientation_var > -EXTERN_ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_pos < -HORIZONTAL_THRESHOLD and orientation_var > -EXTERN_ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 7. OUT OF BOUNDS THE LEFT AND THE INCORRECT DEGREE
    # H < -LH, VV < LV -> GET, MP
    # H < -LH -> GET
    elif horizontal_pos < -HORIZONTAL_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_pos < -HORIZONTAL_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 8. OUT OF BOUNDS THE RIGHT AND THE CORRECT DEGREE
    # H > LH, O < LAE, VV < LV -> GET, MP
    # H > LH, O < LAE -> GET
    elif horizontal_pos > HORIZONTAL_THRESHOLD and orientation_var < EXTERN_ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_pos > HORIZONTAL_THRESHOLD and orientation_var < EXTERN_ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 9. OUT OF BOUNDS THE RIGHT AND THE INCORRECT DEGREE
    # H > LH, VV < LV -> GDT, MP
    # H > LH -> GDT 
    elif horizontal_pos > HORIZONTAL_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_pos > HORIZONTAL_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 10. ABOVE THE HORIZONTAL SPEED LIMIT TO THE RIGHT PERMITTED INTERNALLY WITH CORRECT GRADE
    # VH > LVH, O < Θ, VV < LV -> GET, MP
    # H > LVH, O < Θ -> GET
    elif horizontal_vel > HORIZONTAL_VELOCITY_THRESHOLD and orientation_var < ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel > HORIZONTAL_VELOCITY_THRESHOLD and orientation_var < ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 11. ABOVE THE HORIZONTAL SPEED LIMIT ON THE RIGHT PERMITTED INTERNALLY WITH INCORRECT GRADE
    # VH > LVH, VV < LV -> GDT, MP
    # VH > LVH -> GDT
    elif horizontal_vel > HORIZONTAL_VELOCITY_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel > HORIZONTAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 12. ABOVE THE HORIZONTAL SPEED LIMIT ON THE LEFT PERMITTED INTERNALLY WITH CORRECT GRADE
    # VH < -LVH, O > -Θ, VV < LV -> GDT, MP
    # VH < -LVH, O > -Θ -> GDT
    elif horizontal_vel < -HORIZONTAL_VELOCITY_THRESHOLD and orientation_var > -ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel < -HORIZONTAL_VELOCITY_THRESHOLD and orientation_var > -ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 13.ABOVE THE HORIZONTAL SPEED LIMIT ON THE LEFT PERMITTED INTERNALLY WITH INCORRECT DEGREE
    # VH < -LVH, VV < LV -> GET, MP
    # VH < -LVH -> GET
    elif horizontal_vel < -HORIZONTAL_VELOCITY_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif horizontal_vel < -HORIZONTAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 14. STRONG CORRECTION TO THE RIGHT ON THE DESCENT AT THE CORRECT POINT
    # O > 4 * Θ, VV < LV -> GDT, MP 
    # O > 4 * Θ -> GDT
    elif orientation_var > 4 * ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif orientation_var > 4 * ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)

    # 15. STRONG CORRECTION TO THE LEFT ON THE DESCENT AT THE CORRECT POINT
    # O < -4 * Θ, VV < LV -> GET, MP
    # O < -4 * Θ -> GET
    elif orientation_var < -4 * ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_full_power(action)
        action = main_engine_parcial_power(action)
    elif orientation_var < -4 * ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)

    # 16. WEAK CORRECTION TO THE RIGHT ON THE DESCENT AT THE CORRECT POINT
    # O < -Θ, VV < LV -> GDP, MP
    # O < -Θ -> GDP
    elif orientation_var < -ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_right_with_partial_power(action)
        action = main_engine_parcial_power(action)
    elif orientation_var < -ANGLE_THRESHOLD:
        action = turn_right_with_partial_power(action)
    
    # 17. WEAK CORRECTION TO THE LEFT ON THE DOWNTREND AT THE CORRECT POINT
    # O > Θ, VV < LV -> GEP, MP
    # O > Θ -> GEP
    elif orientation_var > ANGLE_THRESHOLD and vertical_vel < VERTICAL_VELOCITY_THRESHOLD:
        action = turn_left_with_partial_power(action)
        action = main_engine_parcial_power(action)
    elif orientation_var > ANGLE_THRESHOLD:
        action = turn_left_with_partial_power(action)
    
    if action == [0, 0]:
        action = env.action_space.sample()
    
    return action

# Thresholds defined for the scenario WITH wind

WIND_ANGLE_THRESHOLD = 0.015
WIND_EXTERN_ANGLE_THRESHOLD = 0.062
WIND_VERTICAL_VELOCITY_THRESHOLD = -0.015
WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD = -0.06
WIND_HORIZONTAL_VELOCITY_THRESHOLD = 0.005
WIND_EXTERN_HORIZONTAL_VELOCITY_THRESHOLD = 0.15
WIND_HORIZONTAL_THRESHOLD = 0.072

def agent_wind(observation):
    action = [0, 0]

    # Both feet of the spacecraft touch
    if left_foot_touch(observation) == True and right_foot_touch(observation) == True: return action

    # EXCEEDS THE MAXIMUM SPEED LIMIT ON THE RIGHT
    elif(horizontal_velocity(observation) > 2*WIND_EXTERN_HORIZONTAL_VELOCITY_THRESHOLD):
        # STEERS TO THE LEFT
        if orientation(observation) < 3.1 * WIND_EXTERN_ANGLE_THRESHOLD:
            action = turn_left_with_full_power(action)
        elif orientation(observation) > 3.3 * WIND_EXTERN_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)
        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 6 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 5 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)

    # EXCEEDS THE MAXIMUM SPEED LIMIT ON THE LEFT 
    elif(horizontal_velocity(observation) < -2*WIND_EXTERN_HORIZONTAL_VELOCITY_THRESHOLD): 
        # STEER RIGHT
        if orientation(observation) > -3.1 * WIND_EXTERN_ANGLE_THRESHOLD:
            action = turn_right_with_full_power(action)
        elif orientation(observation) < -3.3 * WIND_EXTERN_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)
        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 6 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 5 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)        

    # OUT OF BOUNDS THE LEFT
    elif(horizontal_position(observation) < -WIND_HORIZONTAL_THRESHOLD):
        # GUIDES THE RIGHT
        if orientation(observation) > -2.7 * WIND_EXTERN_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)
        elif orientation(observation) < -2.8 * WIND_EXTERN_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3*WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)
    
    # OUT OF BOUNDS THE RIGHT
    elif(horizontal_position(observation) > WIND_HORIZONTAL_THRESHOLD):
        # LEFT-WING GUIDANCE
        if orientation(observation) < 2.7 * WIND_EXTERN_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)
        elif orientation(observation) > 2.8 * WIND_EXTERN_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action[0] = main_engine_full_power(action)[0]
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action[0] = main_engine_parcial_power(action)[0]

    # ABOVE THE HORIZONTAL SPEED LIMIT ON THE RIGHT PERMITTED INTERNALLY
    elif(horizontal_velocity(observation) > WIND_HORIZONTAL_VELOCITY_THRESHOLD):
        # LEFT-WING GUIDANCE
        if orientation(observation) < WIND_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)
        elif orientation(observation) > 1.2 * WIND_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)
        
    # ABOVE THE HORIZONTAL SPEED LIMIT ON THE LEFT PERMITTED INTERNALLY
    elif(horizontal_velocity(observation) < -WIND_HORIZONTAL_VELOCITY_THRESHOLD): 
        # GUIDES THE RIGHT
        if orientation(observation) > -WIND_ANGLE_THRESHOLD: action = turn_right_with_full_power(action)
        elif orientation(observation) < -1.2 * WIND_ANGLE_THRESHOLD: action = turn_left_with_full_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3 * WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)

    # STRONGLY GUIDES THE RIGHT INTERNALLY
    elif orientation(observation) > 2.5 * WIND_ANGLE_THRESHOLD:
        action = turn_right_with_full_power(action)
        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 5 * WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 4*WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)

    # STRONGLY GUIDES THE LEFT INTERNALLY
    elif orientation(observation) < -2.5 * WIND_ANGLE_THRESHOLD:
        action = turn_left_with_full_power(action)
        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 5 * WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
            
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 4 * WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)
    
    # PARTIAL LEFT INTERNAL GUIDANCE
    elif orientation(observation) > WIND_ANGLE_THRESHOLD:
        action = turn_left_with_partial_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_full_power(action)
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3*WIND_VERTICAL_VELOCITY_THRESHOLD:
            action = main_engine_parcial_power(action)
    
    # PARTIAL RIGHT INTERNAL GUIDE
    elif orientation(observation) < -WIND_ANGLE_THRESHOLD:
        action = turn_right_with_partial_power(action)

        # TOTAL VERTICAL SPEED
        if vertical_velocity(observation) < 4 * WIND_VERTICAL_VELOCITY_THRESHOLD:
            action[0] = main_engine_full_power(action)[0]
        # PARTIAL VERTICAL SPEED
        elif vertical_velocity(observation) < 3*WIND_VERTICAL_VELOCITY_THRESHOLD:
            action[0] = main_engine_parcial_power(action)[0]

    # Ensures that there is a defined action
    if action == [0, 0]:
        action = env.action_space.sample()

    return action

success = 0.0
steps = 0.0

for i in range(EPISODES):
    if(not ENABLE_WIND): st, su = simulate(steps=1000000, policy=agent_no_wind)
    else: st, su = simulate(steps=1000000, policy=agent_wind)

    if su:
        steps += st
    success += su
    
    if su>0:
        print('Average number of successful landings:', steps/success*100)
    print(': Success rate:', success/(i+1)*100)
