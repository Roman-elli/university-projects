import os
from config import *

def finish_game(match_state):
    if(os.path.isfile(GAME_HIST_PATH)):
        file = open(GAME_HIST_PATH, 'r+')
        lista = file.readlines()
        if(len(lista) == 0):
            file.write("NJogo,JogadorVermelho,JogadorAzul\n")
            file.write(f"1,{match_state['red_player_points']},{match_state['blue_player_points']}\n")
        else: 
            file.write(f"{len(lista)},{match_state['red_player_points']},{match_state['blue_player_points']}\n")
    else:
        file = open(GAME_HIST_PATH, 'w')
        file.write("NJogo,JogadorVermelho,JogadorAzul\n")
        file.write(f"1,{match_state['red_player_points']},{match_state['blue_player_points']}\n")
    file.close()

    print("Adeus")
    match_state['window'].bye() 


def faz_ficheiro(match_state):
    pointv = match_state['red_player_points']
    pointa = match_state['blue_player_points']
    nome_arquivo = f"replay_goal_jv_{pointv}ja{pointa}.txt"
    with open(f"../data/game-record/{nome_arquivo}", 'w') as file:
        file.write(f"{match_state['var']['ball']}\n")
        file.write(f"{match_state['var']['red_player']}\n")
        file.write(f"{match_state['var']['blue_player']}\n")
        file.close()

    if(os.path.isfile(GAME_TITLES_PATH)):
        if((pointv == 0 and pointa == 1) or (pointv == 1 and pointa == 0)):
            file = open(GAME_TITLES_PATH, 'w')
        else:
            file = open(GAME_TITLES_PATH, 'a') 
        file.write(f"{nome_arquivo}\n")
    else:
        file = open(GAME_TITLES_PATH, 'w')
        file.write(f"{nome_arquivo}\n")
    file.close()