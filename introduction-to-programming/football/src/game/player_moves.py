import turtle as t
from config import *
from utils.turtle_functions import *

def move_up(match_state, player):
    player_dictionary = match_state[player]
    if(player_dictionary['y_coordinate'] < (WINDOW_HEIGHT/2) - MOVE_PIXELS):
        player_dictionary['player'].setheading(90)
        player_dictionary['player'].fd(MOVE_PIXELS)
    save_movement(player_dictionary)

def move_down(match_state, player):
    player_dictionary = match_state[player]
    if(player_dictionary['y_coordinate'] > -(WINDOW_HEIGHT/2) + MOVE_PIXELS):
        player_dictionary['player'].setheading(-90)
        player_dictionary['player'].fd(MOVE_PIXELS)
    save_movement(player_dictionary)
    
def move_right(match_state, player):
    player_dictionary = match_state[player]
    if(player == 'blue_player' and player_dictionary['x_coordinate'] < (WINDOW_WIDTH/2)):
        player_dictionary['player'].setheading(0)
        player_dictionary['player'].fd(MOVE_PIXELS)
    if(player == 'red_player' and player_dictionary['x_coordinate'] < 0):
        player_dictionary['player'].setheading(0)
        player_dictionary['player'].fd(MOVE_PIXELS)
    save_movement(player_dictionary)

def move_left(match_state, player):
    player_dictionary = match_state[player]
    if(player == 'blue_player' and player_dictionary['x_coordinate'] > 0):
        player_dictionary['player'].setheading(180)
        player_dictionary['player'].fd(MOVE_PIXELS)
    if(player == 'red_player' and player_dictionary['x_coordinate'] > -(WINDOW_WIDTH/2)):
        player_dictionary['player'].setheading(180)
        player_dictionary['player'].fd(MOVE_PIXELS)
    save_movement(player_dictionary)

def save_replay(match_state):
    ball = match_state['ball']

    match_state['var']['ball'] += "{:.5f},{:.5f};".format(ball['x_coordinate'], ball['y_coordinate'])

    red_player = match_state['red_player']
    match_state['var']['red_player'] += "{:.5f},{:.5f};".format(red_player['x_coordinate'], red_player['y_coordinate'])
    
    blue_player = match_state['blue_player']
    match_state['var']['blue_player'] += "{:.5f},{:.5f};".format(blue_player['x_coordinate'],blue_player['y_coordinate'])