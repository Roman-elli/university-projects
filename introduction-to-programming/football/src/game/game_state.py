from config import *
from ui.board import *
from ui.ball import *
from utils.file import *

def posicao(match_state, x_pos_inicial, y_pos_inicial):
    vermelho = match_state['red_player']['jogador']
    azul = match_state['blue_player']['jogador']
    vermelho.goto(-(x_pos_inicial), y_pos_inicial)
    azul.goto(x_pos_inicial, y_pos_inicial)

def check_board_collisions(match_state):
    ball = match_state['ball']
    coordenada = ball['ball'].heading()
    if ball['direcao_x'] < -(WINDOW_WIDTH/2) or ball['direcao_x'] > (WINDOW_WIDTH/2):
        ball['ball'].setheading(180-coordenada)

    if ball['direcao_y'] < -(WINDOW_HEIGHT/2) or ball['direcao_y'] > (WINDOW_HEIGHT/2):
        ball['ball'].setheading(-coordenada) 

def check_goal(match_state):
    verifica_golo_jogador_vermelho(match_state)
    verifica_golo_jogador_azul(match_state)

def verifica_golo_jogador_vermelho(match_state):
    ball = match_state['ball']
    
    if (ball['direcao_x'] >= WINDOW_WIDTH/2 and (ball['direcao_y'] >= -GOAL_POSITION and ball['direcao_y'] <= GOAL_POSITION)):
        match_state['red_player_points'] += 1
        update_board(match_state)
        centra_bola(ball['ball'])
        faz_ficheiro(match_state)
        troca(match_state)
        posicao(match_state, ((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0)
        match_state['var'] = {
        'ball' : "",
        'red_player' : "",
        'blue_player' : "",
        }

def verifica_golo_jogador_azul(match_state):
    ball = match_state['ball']
    
    if (ball['direcao_x'] <= -WINDOW_WIDTH/2 and (ball['direcao_y'] >= -GOAL_POSITION and ball['direcao_y'] <= GOAL_POSITION)):
        match_state['blue_player_points'] += 1
        update_board(match_state)
        centra_bola(ball['ball'])
        faz_ficheiro(match_state)
        troca(match_state)
        posicao(match_state, ((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0)
        match_state['var'] = {
        'ball' : "",
        'red_player' : "",
        'blue_player' : "",
        }

def verifica_toque_jogador_azul(match_state):
    ball = match_state['ball']['ball']
    blue_player = match_state['blue_player']['jogador']
    
    if ball.distance(blue_player) < BALL_RADIUS + PLAYER_RADIUS:
        novo_cabeceamento = 180 + ball.towards(blue_player)
        ball.setheading(novo_cabeceamento)

def verifica_toque_jogador_vermelho(match_state):
    ball = match_state['ball']['ball']
    red_player = match_state['red_player']['jogador']
    
    if ball.distance(red_player) < BALL_RADIUS + PLAYER_RADIUS:
        novo_cabeceamento = 180 + ball.towards(red_player)
        ball.setheading(novo_cabeceamento)