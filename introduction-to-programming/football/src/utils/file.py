import os
from config import *

def finish_game(match_state):
    if(os.path.isfile(GAME_HIST_PATH)):
        file = open(GAME_HIST_PATH, 'r+')
        file_lines = file.readlines()
        if(len(file_lines) == 0):
            file.write("Game Number,Red Player,Blue Player\n")
            file.write(f"1,{match_state['red_player_points']},{match_state['blue_player_points']}\n")
        else: 
            file.write(f"{len(file_lines)},{match_state['red_player_points']},{match_state['blue_player_points']}\n")
    else:
        file = open(GAME_HIST_PATH, 'w')
        file.write("Game Number,Red Player,Blue Player\n")
        file.write(f"1,{match_state['red_player_points']},{match_state['blue_player_points']}\n")
    file.close()

    match_state['window'].bye() 


def save_data(match_state):
    red_points = match_state['red_player_points']
    blue_points = match_state['blue_player_points']
    file_name = f"replay_goal_jv_{red_points}ja{blue_points}.txt"
    with open(f"../data/game-record/{file_name}", 'w') as file:
        file.write(f"{match_state['var']['ball']}\n")
        file.write(f"{match_state['var']['red_player']}\n")
        file.write(f"{match_state['var']['blue_player']}\n")
        file.close()

    if(os.path.isfile(GAME_TITLES_PATH)):
        if(red_points >= 1 or blue_points >= 1):
            file = open(GAME_TITLES_PATH, 'a+') 
        file.write(f"{file_name}\n")
    else:
        file = open(GAME_TITLES_PATH, 'w')
        file.write(f"{file_name}\n")
    file.close()