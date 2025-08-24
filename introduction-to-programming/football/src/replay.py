import main
import os
from config import *
from game.game_setup import *

def le_replay(nome_ficheiro):
    replay_coordinates = open(f"../data/game-record/{nome_ficheiro}", 'r')
    ball = replay_coordinates.readline()
    red_player = replay_coordinates.readline()
    blue_player = replay_coordinates.readline()
    
    replay_data ={}
    replay_data["ball"] = file_lines(ball)
    replay_data["red_player"] = file_lines(red_player)
    replay_data["blue_player"] = file_lines(blue_player)

    return replay_data

def file_lines(s):
    temp_character = s.split(';')
    formatted_list = [item.split(',') for item in temp_character]
    file_lines = []
    for i in range(0, len(formatted_list)-1):
        coordinates = (float(formatted_list[i][0]), float(formatted_list[i][1]))
        file_lines.append(coordinates)
    return file_lines 

def main():
    print("Available Replays: ")
    if(os.path.isfile(GAME_TITLES_PATH)):
        file = open(GAME_TITLES_PATH, 'r')
        file_lines = file.readlines()
        file_list = [lines.rstrip('\n') for lines in file_lines]
        for i in range (len(file_list)):
            print(i+1, "->", file_list[i])
        x = int(input("Select a replay: "))

    match_state = init_state()
    setup(match_state, False)
   
    replay = le_replay(file_list[x-1])
    for i in range(len(replay['ball'])):
        match_state['window'].update()
        match_state['red_player']['player'].setpos(replay['red_player'][i])
        match_state['blue_player']['player'].setpos(replay['blue_player'][i])
        match_state['ball']['ball'].setpos(replay['ball'][i])
    match_state['window'].exitonclick()

if __name__ == '__main__':
    main()