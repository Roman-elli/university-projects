import os
from config import *

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


def faz_ficheiro(estado_jogo):
    pointv = estado_jogo['pontuacao_jogador_vermelho']
    pointa = estado_jogo['pontuacao_jogador_azul']
    nome_arquivo = f"replay_goal_jv_{pointv}ja{pointa}.txt"
    with open(f"../data/game-record/{nome_arquivo}", 'w') as file:
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