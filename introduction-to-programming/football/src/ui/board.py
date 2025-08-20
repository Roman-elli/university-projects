import turtle as t
import time
import pygame
import random

from config import *
from utils.turtle_functions import *

def cria_janela():
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

def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write("Player A: {}\t\tPlayer B: {} ".format(estado_jogo['pontuacao_jogador_vermelho'], estado_jogo['pontuacao_jogador_azul']),align="center",font=('Monaco',24,"normal"))

def troca(estado_jogo):
    pygame.init()
    som = pygame.mixer.Sound(GAME_SOUND_PATH)

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

