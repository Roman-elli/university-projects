import functools

from config import *
from ui.board import *
from ui.players import *
from ui.ball import *
from ui.score import *
from game.player_moves import *
from utils.file import *

def init_state():
    match_state = {}
    match_state['ball'] = None
    match_state['red_player'] = None
    match_state['blue_player'] = None
    match_state['var'] = {
        'ball' : "",
        'red_player' : "",
        'blue_player' : "",
    }
    match_state['red_player_points'] = 0
    match_state['blue_player_points'] = 0
    match_state['game_list'] = {}
    return match_state


def setup(match_state, playable):
    window = draw_window()
    window.listen()
    if playable:
        window.onkeypress(functools.partial(move_up, match_state, 'red_player') ,'w')
        window.onkeypress(functools.partial(move_down, match_state, 'red_player') ,'s')
        window.onkeypress(functools.partial(move_left, match_state, 'red_player') ,'a')
        window.onkeypress(functools.partial(move_right, match_state, 'red_player') ,'d')
        window.onkeypress(functools.partial(move_up, match_state, 'blue_player') ,'Up')
        window.onkeypress(functools.partial(move_down, match_state, 'blue_player') ,'Down')
        window.onkeypress(functools.partial(move_left, match_state, 'blue_player') ,'Left')
        window.onkeypress(functools.partial(move_right, match_state, 'blue_player') ,'Right')
        window.onkeypress(functools.partial(finish_game, match_state) ,'Escape')
        match_state['score_board'] = create_score()
    draw_board_lines()
    ball = draw_ball()
    red_player = draw_player(-((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0, "red")
    blue_player = draw_player(((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0, "blue")
    match_state['window'] = window
    match_state['ball'] = ball
    match_state['red_player'] = red_player
    match_state['blue_player'] = blue_player
