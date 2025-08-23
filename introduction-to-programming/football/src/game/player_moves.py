import turtle as t
from config import *
from utils.turtle_functions import *

def move_up(match_state, jogador):
    meche = match_state[jogador]
    if(meche['direcao_y'] < (WINDOW_HEIGHT/2) - MOVE_PIXELS):
        meche['jogador'].setheading(90)
        meche['jogador'].fd(MOVE_PIXELS)
    guarda_movimento(meche)

def move_down(match_state, jogador):
    meche = match_state[jogador]
    if(meche['direcao_y'] > -(WINDOW_HEIGHT/2) + MOVE_PIXELS):
        meche['jogador'].setheading(-90)
        meche['jogador'].fd(MOVE_PIXELS)
    guarda_movimento(meche)
    
def move_right(match_state, jogador):
    meche = match_state[jogador]
    if(jogador == 'blue_player' and meche['direcao_x'] < (WINDOW_WIDTH/2)):
        meche['jogador'].setheading(0)
        meche['jogador'].fd(MOVE_PIXELS)
    if(jogador == 'red_player' and meche['direcao_x'] < 0):
        meche['jogador'].setheading(0)
        meche['jogador'].fd(MOVE_PIXELS)
    guarda_movimento(meche)

def move_left(match_state, jogador):
    meche = match_state[jogador]
    if(jogador == 'blue_player' and meche['direcao_x'] > 0):
        meche['jogador'].setheading(180)
        meche['jogador'].fd(MOVE_PIXELS)
    if(jogador == 'red_player' and meche['direcao_x'] > -(WINDOW_WIDTH/2)):
        meche['jogador'].setheading(180)
        meche['jogador'].fd(MOVE_PIXELS)
    guarda_movimento(meche)

def save_replay(match_state):
    ball = match_state['ball']
    posicao_bola = "{:.5f},{:.5f};".format(ball['direcao_x'], ball['direcao_y'])
    match_state['var']['ball'] += posicao_bola

    jogadorv = match_state['red_player']
    posicaov = "{:.5f},{:.5f};".format(jogadorv['direcao_x'], jogadorv['direcao_y'])
    match_state['var']['red_player'] += posicaov
    
    jogadora = match_state['blue_player']
    posicaoa = "{:.5f},{:.5f};".format(jogadora['direcao_x'],jogadora['direcao_y'])
    match_state['var']['blue_player'] += posicaoa