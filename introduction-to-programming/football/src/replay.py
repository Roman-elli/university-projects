import main
import os
from config import *
from game.game_setup import *

def le_replay(nome_ficheiro):
    coordenadas = open(f"../data/game-record/{nome_ficheiro}", 'r')
    ball = coordenadas.readline()
    red_player = coordenadas.readline()
    blue_player = coordenadas.readline()
    
    dici ={}
    dici["ball"] = lista(ball)
    dici["red_player"] = lista(red_player)
    dici["blue_player"] = lista(blue_player)

    return dici

def lista(s):
    ponto_virgula = s.split(';')
    virgula = [item.split(',') for item in ponto_virgula]
    lista = []
    for i in range(0, len(virgula)-1):
        tuplo = (float(virgula[i][0]), float(virgula[i][1]))
        lista.append(tuplo)
    return lista 

def main():
    print("Replays disponiveis: ")
    if(os.path.isfile(GAME_TITLES_PATH)):
        file = open(GAME_TITLES_PATH, 'r')
        lista = file.readlines()
        linhas = [linha.rstrip('\n') for linha in lista]
        for i in range (len(linhas)):
            print(i+1, "->", linhas[i])
        x = int(input("Digite o replay que deseja ver: "))

    match_state = init_state()
    setup(match_state, False)
   
    replay = le_replay(linhas[x-1])
    for i in range(len(replay['ball'])):
        match_state['window'].update()
        match_state['red_player']['jogador'].setpos(replay['red_player'][i])
        match_state['blue_player']['jogador'].setpos(replay['blue_player'][i])
        match_state['ball']['ball'].setpos(replay['ball'][i])
    match_state['window'].exitonclick()

if __name__ == '__main__':
    main()