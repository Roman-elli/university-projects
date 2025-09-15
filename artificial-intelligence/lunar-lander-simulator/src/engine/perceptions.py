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
