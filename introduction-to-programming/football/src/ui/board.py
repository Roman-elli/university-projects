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

def baliza(desenha):
    for i in range (3):
        if(i == 1):
            desenha.forward(GOAL_LARGE_SIDE)
        else:
            desenha.forward(GOAL_SMALL_SIDE)
        desenha.left(90)

def linhas(desenha):
    vai_para(-(WINDOW_WIDTH/2), -(WINDOW_HEIGHT/2), desenha)
    for i in range (2):
        desenha.forward(WINDOW_HEIGHT)
        desenha.right(90)
        desenha.forward(WINDOW_WIDTH )
        desenha.right(90) 

def draw_board_lines():
    desenha = t.Turtle()
    desenha.color("White")
    desenha.pensize(DEFAULT_TURTLE_SCALE + 2)  
    t.hideturtle()

    vai_para(0, -CENTER_RADIUS, desenha)
    desenha.circle(CENTER_RADIUS)

    vai_para(0, -(WINDOW_HEIGHT/2), desenha)
    desenha.setheading(90)
    desenha.forward(WINDOW_HEIGHT)

    vai_para(-(WINDOW_WIDTH/2), -GOAL_POSITION, desenha)
    desenha.setheading(0)
    baliza(desenha)

    vai_para((WINDOW_WIDTH/2), GOAL_POSITION, desenha)
    desenha.setheading(180)
    baliza(desenha)

    linhas(desenha)

def update_board(match_state):
    match_state['score_board'].clear()
    match_state['score_board'].write("Player A: {}\t\tPlayer B: {} ".format(match_state['red_player_points'], match_state['blue_player_points']),align="center",font=('Monaco',24,"normal"))

def troca(match_state):
    pygame.init()
    som = pygame.mixer.Sound(GAME_SOUND_PATH)

    som.play()
    time.sleep(som.get_length())
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

