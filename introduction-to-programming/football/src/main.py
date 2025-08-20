import os
from game.game_setup import *
from game.game_state import *
from game.ball_moves import *

def main():
    estado_jogo = init_state()
    
    os.makedirs('../data/game-record', exist_ok=True)
    os.makedirs('../data/game-results', exist_ok=True)
    os.makedirs('../data/game-titles', exist_ok=True)

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