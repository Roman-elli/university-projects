from config import *
from ui.board import *
from ui.ball import *
from utils.file import *

def posicao(estado_jogo, x_pos_inicial, y_pos_inicial):
    vermelho = estado_jogo['jogador_vermelho']['jogador']
    azul = estado_jogo['jogador_azul']['jogador']
    vermelho.goto(-(x_pos_inicial), y_pos_inicial)
    azul.goto(x_pos_inicial, y_pos_inicial)

def verifica_colisoes_ambiente(estado_jogo):
    ball = estado_jogo['bola']
    coordenada = ball['bola'].heading()
    if ball['direcao_x'] < -(WINDOW_WIDTH/2) or ball['direcao_x'] > (WINDOW_WIDTH/2):
        ball['bola'].setheading(180-coordenada)

    if ball['direcao_y'] < -(WINDOW_HEIGHT/2) or ball['direcao_y'] > (WINDOW_HEIGHT/2):
        ball['bola'].setheading(-coordenada) 

def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)

def verifica_golo_jogador_vermelho(estado_jogo):
    ball = estado_jogo['bola']
    
    if (ball['direcao_x'] >= WINDOW_WIDTH/2 and (ball['direcao_y'] >= -GOAL_POSITION and ball['direcao_y'] <= GOAL_POSITION)):
        estado_jogo['pontuacao_jogador_vermelho'] += 1
        update_board(estado_jogo)
        centra_bola(ball['bola'])
        faz_ficheiro(estado_jogo)
        troca(estado_jogo)
        posicao(estado_jogo, ((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0)
        estado_jogo['var'] = {
        'bola' : "",
        'jogador_vermelho' : "",
        'jogador_azul' : "",
        }

def verifica_golo_jogador_azul(estado_jogo):
    ball = estado_jogo['bola']
    
    if (ball['direcao_x'] <= -WINDOW_WIDTH/2 and (ball['direcao_y'] >= -GOAL_POSITION and ball['direcao_y'] <= GOAL_POSITION)):
        estado_jogo['pontuacao_jogador_azul'] += 1
        update_board(estado_jogo)
        centra_bola(ball['bola'])
        faz_ficheiro(estado_jogo)
        troca(estado_jogo)
        posicao(estado_jogo, ((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0)
        estado_jogo['var'] = {
        'bola' : "",
        'jogador_vermelho' : "",
        'jogador_azul' : "",
        }

def verifica_toque_jogador_azul(estado_jogo):
    ball = estado_jogo['bola']['bola']
    jogador_azul = estado_jogo['jogador_azul']['jogador']
    
    if ball.distance(jogador_azul) < BALL_RADIUS + PLAYER_RADIUS:
        novo_cabeceamento = 180 + ball.towards(jogador_azul)
        ball.setheading(novo_cabeceamento)

def verifica_toque_jogador_vermelho(estado_jogo):
    ball = estado_jogo['bola']['bola']
    jogador_vermelho = estado_jogo['jogador_vermelho']['jogador']
    
    if ball.distance(jogador_vermelho) < BALL_RADIUS + PLAYER_RADIUS:
        novo_cabeceamento = 180 + ball.towards(jogador_vermelho)
        ball.setheading(novo_cabeceamento)