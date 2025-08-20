import turtle as t
from config import *
import random

def centra_bola(bola):
    bola.setpos(BALL_START_POS)
    x = random.randrange(360)
    bola.setheading(x)

def criar_bola():
    bola = t.Turtle()
    bola.penup()
    bola.shapesize(1)
    bola.shape("circle")
    bola.color("black")
    centra_bola(bola)
    bola.speed(MOVE_PIXELS*1.2)
    dic_bola = {'bola': bola,'direcao_x': bola.xcor(), 'direcao_y': bola.ycor(), 'posicao_anterior': None}

    return dic_bola