from config import *

# Load high score from file into state
def load_high_score(state):
    with open(HIGH_SCORES_FILE_PATH, "a") as statehs:
        statehs.close()
    with open(HIGH_SCORES_FILE_PATH, "r") as statehs:
        empty = statehs.read(1)
        if not empty:
            state["high_score"] = 0
        else:
            state["high_score"] = int(statehs.readlines()[-1])
        statehs.close()

# Write high score to file if beaten
def write_high_score_to_file(state):
    with open(HIGH_SCORES_FILE_PATH, "a+") as statehs:
        print("NEW HIGHSCORE!!!")
        statehs.write("\n")
        statehs.write(str(state["high_score"]))
        statehs.close()
