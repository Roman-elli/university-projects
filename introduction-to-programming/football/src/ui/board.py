import turtle as t
import time
import pygame
import random

from config import *
from utils.turtle_functions import *

def draw_window():
    window=t.Screen()
    window.title("FootBall Game")
    window.bgcolor("green")
    window.setup(width = WINDOW_WIDTH,height = WINDOW_HEIGHT)
    window.tracer(0)
    return window

def draw_goalpost(draw):
    for i in range (3):
        if(i == 1):
            draw.forward(GOAL_LARGE_SIDE)
        else:
            draw.forward(GOAL_SMALL_SIDE)
        draw.left(90)

def board_lines(draw):
    turtle_go_to(-(WINDOW_WIDTH/2), -(WINDOW_HEIGHT/2), draw)
    for i in range (2):
        draw.forward(WINDOW_HEIGHT)
        draw.right(90)
        draw.forward(WINDOW_WIDTH )
        draw.right(90) 

def draw_board_lines():
    draw = t.Turtle()
    draw.color("White")
    draw.pensize(DEFAULT_TURTLE_SCALE + 2)  
    t.hideturtle()

    turtle_go_to(0, -CENTER_RADIUS, draw)
    draw.circle(CENTER_RADIUS)

    turtle_go_to(0, -(WINDOW_HEIGHT/2), draw)
    draw.setheading(90)
    draw.forward(WINDOW_HEIGHT)

    turtle_go_to(-(WINDOW_WIDTH/2), -GOAL_POSITION, draw)
    draw.setheading(0)
    draw_goalpost(draw)

    turtle_go_to((WINDOW_WIDTH/2), GOAL_POSITION, draw)
    draw.setheading(180)
    draw_goalpost(draw)

    board_lines(draw)

def update_board(match_state):
    match_state['score_board'].clear()
    match_state['score_board'].write("Player A: {}\t\tPlayer B: {} ".format(match_state['red_player_points'], match_state['blue_player_points']),align="center",font=('Monaco',24,"normal"))

def pick_aleatory_board(match_state):
    pygame.init()
    sound_file = pygame.mixer.Sound(GAME_SOUND_PATH)

    sound_file.play()
    time.sleep(sound_file.get_length())
    pygame.quit()

    window = match_state['window']
    ball = match_state['ball']['ball']
    x = random.randint(0, 4)

    if(x == 0):
        window.bgcolor("black")
        ball.color("white")
    if(x == 1):
        window.bgcolor("gold")
        ball.color("black")
    if(x == 2):
        window.bgcolor("gray")
        ball.color("green")
    if(x == 3):
        window.bgcolor("green")
        ball.color("black")
    if(x == 4):
        window.bgcolor("purple")
        ball.color("gold")

