import turtle as turtle
from config import *
import functools
from game.player import *
from random import randint
from ui.board import *
from ui.food import *

# Initialize game state
def init_state():
    state = {'score_board': None, 'new_high_score': False, 'high_score': 0, 'score': 0, 'food': None, 'window': None, "player": ""}
    snake = {'head': None, 'current_direction': None}
    state['snake'] = snake
    return state

# Setup window, snake, score and food
def setup(state):
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    window.onkey(functools.partial(go_up, state), 'w')
    window.onkey(functools.partial(go_down, state), 's')
    window.onkey(functools.partial(go_left, state), 'a')
    window.onkey(functools.partial(go_right, state), 'd')
    window.tracer(0)

    background(state)
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].showturtle()
    snake['head'].pu()
    snake['head'].color('grey')
    snake["snakebody"] = []
    snake["coord"] = []
    create_score_board(state)
    create_food(state)
