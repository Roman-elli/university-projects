import turtle as t
import functools
import random
import os
import random
import pygame
import time
from src.config import *

def guarda_movimento(dic):
    dic['direcao_x'] = dic['jogador'].xcor()
    dic['direcao_y'] = dic['jogador'].ycor()

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

def vai_para(x,y, desenha):
    desenha.penup()
    desenha.goto(x,y)
    desenha.pendown()

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

def desenha_linhas_campo():
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

def cria_jogador(x_pos_inicial, y_pos_inicial, cor):
    jogador = t.Turtle()
    jogador.shapesize(stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE)
    jogador.shape("circle")
    jogador.color(cor)
    jogador.penup()
    jogador.goto(x_pos_inicial, y_pos_inicial)
    jogador.speed(MOVE_PIXELS)
    dic_jogador = {'jogador': jogador,'direcao_x': jogador.xcor(), 'direcao_y': jogador.ycor(), 'posicao_anterior': None}

    return dic_jogador

def init_state():
    estado_jogo = {}
    estado_jogo['bola'] = None
    estado_jogo['jogador_vermelho'] = None
    estado_jogo['jogador_azul'] = None
    estado_jogo['var'] = {
        'bola' : "",
        'jogador_vermelho' : "",
        'jogador_azul' : "",
    }
    estado_jogo['pontuacao_jogador_vermelho'] = 0
    estado_jogo['pontuacao_jogador_azul'] = 0
    estado_jogo['lista_jogos'] = {}
    return estado_jogo

def cria_janela():
    window=t.Screen()
    window.title("FootBall Game")
    window.bgcolor("green")
    window.setup(width = WINDOW_WIDTH,height = WINDOW_HEIGHT)
    window.tracer(0)
    return window

def cria_quadro_resultados():
    quadro=t.Turtle()
    quadro.speed(0)
    quadro.color("Blue")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(0,260)
    quadro.write("Player A: 0\t\tPlayer B: 0 ", align="center", font=('Monaco',24,"normal"))
    return quadro

def terminar_jogo(estado_jogo):
    if(os.path.isfile(GAME_HIST_PATH)):
        file = open(GAME_HIST_PATH, 'r+')
        lista = file.readlines()
        if(len(lista) == 0):
            file.write("NJogo,JogadorVermelho,JogadorAzul\n")
            file.write(f"1,{estado_jogo['pontuacao_jogador_vermelho']},{estado_jogo['pontuacao_jogador_azul']}\n")
        else: 
            file.write(f"{len(lista)},{estado_jogo['pontuacao_jogador_vermelho']},{estado_jogo['pontuacao_jogador_azul']}\n")
    else:
        file = open(GAME_HIST_PATH, 'w')
        file.write("NJogo,JogadorVermelho,JogadorAzul\n")
        file.write(f"1,{estado_jogo['pontuacao_jogador_vermelho']},{estado_jogo['pontuacao_jogador_azul']}\n")
    file.close()

    print("Adeus")
    estado_jogo['janela'].bye()  

def setup(estado_jogo, jogar):
    janela = cria_janela()
    janela.listen()
    if jogar:
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_vermelho') ,'w')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_vermelho') ,'s')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_vermelho') ,'a')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_vermelho') ,'d')
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_azul') ,'Up')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_azul') ,'Down')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_azul') ,'Left')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_azul') ,'Right')
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo) ,'Escape')
        quadro = cria_quadro_resultados()
        estado_jogo['quadro'] = quadro
    desenha_linhas_campo()
    bola = criar_bola()
    jogador_vermelho = cria_jogador(-((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0, "red")
    jogador_azul = cria_jogador(((WINDOW_HEIGHT / 2) + GOAL_SMALL_SIDE), 0, "blue")
    estado_jogo['janela'] = janela
    estado_jogo['bola'] = bola
    estado_jogo['jogador_vermelho'] = jogador_vermelho
    estado_jogo['jogador_azul'] = jogador_azul

def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write("Player A: {}\t\tPlayer B: {} ".format(estado_jogo['pontuacao_jogador_vermelho'], estado_jogo['pontuacao_jogador_azul']),align="center",font=('Monaco',24,"normal"))

def movimenta_bola(estado_jogo):
    ball = estado_jogo['bola']
    ball['bola'].forward(1)
    ball['direcao_x'] = ball['bola'].xcor()
    ball['direcao_y'] = ball['bola'].ycor()

def verifica_colisoes_ambiente(estado_jogo):
    ball = estado_jogo['bola']
    coordenada = ball['bola'].heading()
    if ball['direcao_x'] < -(WINDOW_WIDTH/2) or ball['direcao_x'] > (WINDOW_WIDTH/2):
        ball['bola'].setheading(180-coordenada)

    if ball['direcao_y'] < -(WINDOW_HEIGHT/2) or ball['direcao_y'] > (WINDOW_HEIGHT/2):
        ball['bola'].setheading(-coordenada)

def faz_ficheiro(estado_jogo):
    pointv = estado_jogo['pontuacao_jogador_vermelho']
    pointa = estado_jogo['pontuacao_jogador_azul']
    nome_arquivo = f"replay_goal_jv_{pointv}ja{pointa}.txt"
    with open(f"data/game-record/{nome_arquivo}", 'w') as file:
        file.write(f"{estado_jogo['var']['bola']}\n")
        file.write(f"{estado_jogo['var']['jogador_vermelho']}\n")
        file.write(f"{estado_jogo['var']['jogador_azul']}\n")
        file.close()
    
    if(os.path.isfile(GAME_TITLES_PATH)):
        if((pointv == 0 and pointa == 1) or (pointv == 1 and pointa == 0)):
            file = open(GAME_TITLES_PATH, 'w')
        else:
            file = open(GAME_TITLES_PATH, 'a') 
        file.write(f"{nome_arquivo}\n")
    else:
        file = open(GAME_TITLES_PATH, 'w')
        file.write(f"{nome_arquivo}\n")
    file.close()

def posicao(estado_jogo, x_pos_inicial, y_pos_inicial):
    vermelho = estado_jogo['jogador_vermelho']['jogador']
    azul = estado_jogo['jogador_azul']['jogador']
    vermelho.goto(-(x_pos_inicial), y_pos_inicial)
    azul.goto(x_pos_inicial, y_pos_inicial)
    
def troca(estado_jogo):
    pygame.init()
    arquivo_palmas = GAME_SOUND_PATH
    som = pygame.mixer.Sound(arquivo_palmas)

    som.play()
    time.sleep(som.get_length())
    pygame.quit()

    window = estado_jogo['janela']
    bola = estado_jogo['bola']['bola']
    x = random.randint(0, 4)

    if(x == 0):
        window.bgcolor("black")
        bola.color("white")
    if(x == 1):
        window.bgcolor("gold")
        bola.color("black")
    if(x == 2):
        window.bgcolor("gray")
        bola.color("green")
    if(x == 3):
        window.bgcolor("green")
        bola.color("black")
    if(x == 4):
        window.bgcolor("purple")
        bola.color("gold") 

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

def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)

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

def main():
    estado_jogo = init_state()
    
    os.makedirs('data/game-record', exist_ok=True)
    os.makedirs('data/game-results', exist_ok=True)
    os.makedirs('data/game-titles', exist_ok=True)

    setup(estado_jogo, True)
    while True:
        guarda_posicoes_para_var(estado_jogo)
        estado_jogo['janela'].update()
        if estado_jogo['bola'] is not None:
            movimenta_bola(estado_jogo)
        verifica_colisoes_ambiente(estado_jogo)
        verifica_golos(estado_jogo)
        if estado_jogo['jogador_vermelho'] is not None:
            verifica_toque_jogador_azul(estado_jogo)
        if estado_jogo['jogador_azul'] is not None:
            verifica_toque_jogador_vermelho(estado_jogo)

if __name__ == '__main__':
    main()