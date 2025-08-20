import turtle as t
from config import *
from utils.turtle_functions import *

def jogador_cima(estado_jogo, jogador):
    meche = estado_jogo[jogador]
    if(meche['direcao_y'] < (WINDOW_HEIGHT/2) - MOVE_PIXELS):
        meche['jogador'].setheading(90)
        meche['jogador'].fd(MOVE_PIXELS)
    guarda_movimento(meche)

def jogador_baixo(estado_jogo, jogador):
    meche = estado_jogo[jogador]
    if(meche['direcao_y'] > -(WINDOW_HEIGHT/2) + MOVE_PIXELS):
        meche['jogador'].setheading(-90)
        meche['jogador'].fd(MOVE_PIXELS)
    guarda_movimento(meche)
    
def jogador_direita(estado_jogo, jogador):
    meche = estado_jogo[jogador]
    if(jogador == 'jogador_azul' and meche['direcao_x'] < (WINDOW_WIDTH/2)):
        meche['jogador'].setheading(0)
        meche['jogador'].fd(MOVE_PIXELS)
    if(jogador == 'jogador_vermelho' and meche['direcao_x'] < 0):
        meche['jogador'].setheading(0)
        meche['jogador'].fd(MOVE_PIXELS)
    guarda_movimento(meche)

def jogador_esquerda(estado_jogo, jogador):
    meche = estado_jogo[jogador]
    if(jogador == 'jogador_azul' and meche['direcao_x'] > 0):
        meche['jogador'].setheading(180)
        meche['jogador'].fd(MOVE_PIXELS)
    if(jogador == 'jogador_vermelho' and meche['direcao_x'] > -(WINDOW_WIDTH/2)):
        meche['jogador'].setheading(180)
        meche['jogador'].fd(MOVE_PIXELS)
    guarda_movimento(meche)

def guarda_posicoes_para_var(estado_jogo):
    bola = estado_jogo['bola']
    posicao_bola = "{:.5f},{:.5f};".format(bola['direcao_x'], bola['direcao_y'])
    estado_jogo['var']['bola'] += posicao_bola

    jogadorv = estado_jogo['jogador_vermelho']
    posicaov = "{:.5f},{:.5f};".format(jogadorv['direcao_x'], jogadorv['direcao_y'])
    estado_jogo['var']['jogador_vermelho'] += posicaov
    
    jogadora = estado_jogo['jogador_azul']
    posicaoa = "{:.5f},{:.5f};".format(jogadora['direcao_x'],jogadora['direcao_y'])
    estado_jogo['var']['jogador_azul'] += posicaoa