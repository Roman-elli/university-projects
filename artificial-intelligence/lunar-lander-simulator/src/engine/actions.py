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
