import gymnasium as gym

# =============================
# Lunar setup
# =============================
ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = None # testing scenario, put 'human' to watch all episodes
EPISODES = 1000

env = gym.make("LunarLander-v3", render_mode =RENDER_MODE, 
continuous=True, gravity=GRAVITY, 
enable_wind=ENABLE_WIND, wind_power=WIND_POWER, 
turbulence_power=TURBULENCE_POWER)

# =============================
# No wind Lunar constants
# =============================
ANGLE_THRESHOLD = 0.005
EXTERN_ANGLE_THRESHOLD = 0.053
VERTICAL_VELOCITY_THRESHOLD = -0.07
HORIZONTAL_VELOCITY_THRESHOLD = 0.005
EXTERN_HORIZONTAL_VELOCITY_THRESHOLD = 0.15
HORIZONTAL_THRESHOLD = 0.023

# =============================
# Wind Lunar constants
# =============================
WIND_ANGLE_THRESHOLD = 0.015
WIND_EXTERN_ANGLE_THRESHOLD = 0.062
WIND_VERTICAL_VELOCITY_THRESHOLD = -0.015
WIND_EXTERN_VERTICAL_VELOCITY_THRESHOLD = -0.06
WIND_HORIZONTAL_VELOCITY_THRESHOLD = 0.005
WIND_EXTERN_HORIZONTAL_VELOCITY_THRESHOLD = 0.15
WIND_HORIZONTAL_THRESHOLD = 0.072