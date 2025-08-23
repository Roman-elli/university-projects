import turtle as t
from config import *
import random

def centra_bola(ball):
    ball.setpos(BALL_START_POS)
    x = random.randrange(360)
    ball.setheading(x)

def draw_ball():
    ball = t.Turtle()
    ball.penup()
    ball.shapesize(1)
    ball.shape("circle")
    ball.color("black")
    centra_bola(ball)
    ball.speed(MOVE_PIXELS*1.2)
    dic_bola = {'ball': ball,'direcao_x': ball.xcor(), 'direcao_y': ball.ycor(), 'posicao_anterior': None}

    return dic_bola