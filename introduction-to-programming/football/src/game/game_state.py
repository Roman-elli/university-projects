from config import *
from ui.board import *
from ui.ball import *
from utils.file import *

def update_position(match_state, x_pos_inicial, y_pos_inicial):
    red_player = match_state['red_player']['player']
    blue_player = match_state['blue_player']['player']
    red_player.goto(-(x_pos_inicial), y_pos_inicial)
    blue_player.goto(x_pos_inicial, y_pos_inicial)

def check_board_collisions(match_state):
    ball = match_state['ball']
    head_direction = ball['ball'].heading()
    if ball['x_coordinate'] < -(WINDOW_WIDTH/2) or ball['x_coordinate'] > (WINDOW_WIDTH/2):
        ball['ball'].setheading(180-head_direction)

    if ball['y_coordinate'] < -(WINDOW_HEIGHT/2) or ball['y_coordinate'] > (WINDOW_HEIGHT/2):
        ball['ball'].setheading(-head_direction) 

def check_goal(match_state):
    ball = match_state['ball']
    
    if (ball['x_coordinate'] >= WINDOW_WIDTH/2 and (ball['y_coordinate'] >= -GOAL_POSITION and ball['y_coordinate'] <= GOAL_POSITION)):
        match_state['red_player_points'] += 1
        update_board(match_state)
        reset_ball_position(ball['ball'])
        save_data(match_state)
        pick_aleatory_board(match_state)
        update_position(match_state, ((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0)
        match_state['var'] = {
        'ball' : "",
        'red_player' : "",
        'blue_player' : "",
        }
    
    elif (ball['x_coordinate'] <= -WINDOW_WIDTH/2 and (ball['y_coordinate'] >= -GOAL_POSITION and ball['y_coordinate'] <= GOAL_POSITION)):
        match_state['blue_player_points'] += 1
        update_board(match_state)
        reset_ball_position(ball['ball'])
        save_data(match_state)
        pick_aleatory_board(match_state)
        update_position(match_state, ((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0)
        match_state['var'] = {
        'ball' : "",
        'red_player' : "",
        'blue_player' : "",
        }

def check_blue_collisions(match_state):
    ball = match_state['ball']['ball']
    blue_player = match_state['blue_player']['player']
    
    if ball.distance(blue_player) < BALL_RADIUS + PLAYER_RADIUS:
        ball.setheading(180 + ball.towards(blue_player))

def check_red_collisions(match_state):
    ball = match_state['ball']['ball']
    red_player = match_state['red_player']['player']
    
    if ball.distance(red_player) < BALL_RADIUS + PLAYER_RADIUS:
        ball.setheading(180 + ball.towards(red_player))