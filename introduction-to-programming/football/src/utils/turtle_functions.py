import turtle as t
from config import *

def guarda_movimento(dic):
    dic['direcao_x'] = dic['jogador'].xcor()
    dic['direcao_y'] = dic['jogador'].ycor()

def vai_para(x,y, desenha):
    desenha.penup()
    desenha.goto(x,y)
    desenha.pendown()
