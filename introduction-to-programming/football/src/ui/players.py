import turtle as t
from config import *

def draw_player(x_pos_inicial, y_pos_inicial, cor):
    jogador = t.Turtle()
    jogador.shapesize(stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE)
    jogador.shape("circle")
    jogador.color(cor)
    jogador.penup()
    jogador.goto(x_pos_inicial, y_pos_inicial)
    jogador.speed(MOVE_PIXELS)
    dic_jogador = {'jogador': jogador,'direcao_x': jogador.xcor(), 'direcao_y': jogador.ycor(), 'posicao_anterior': None}

    return dic_jogador
