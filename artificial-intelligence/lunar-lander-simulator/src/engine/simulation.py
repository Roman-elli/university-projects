import config as cfg

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
    observ, _ = cfg.env.reset(seed=seed)
    for step in range(steps):
        action = policy(observ)

        observ, _, term, trunc, _ = cfg.env.step(action)

        if term or trunc:
            break

    success = check_successful_landing(observ)
    return step, success
