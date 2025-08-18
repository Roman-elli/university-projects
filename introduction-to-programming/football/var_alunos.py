import foosball_alunos
import os

def le_replay(nome_ficheiro):
    coordenadas = open(nome_ficheiro, 'r')
    bola = coordenadas.readline()
    jogador_vermelho = coordenadas.readline()
    jogador_azul = coordenadas.readline()
    
    dici ={}
    dici["bola"] = lista(bola)
    dici["jogador_vermelho"] = lista(jogador_vermelho)
    dici["jogador_azul"] = lista(jogador_azul)

    return dici

#Função que faz o split da string lida do ficheiro, para criar uma lista de tuplos 
def lista(s):
    ponto_virgula = s.split(';')
    virgula = [item.split(',') for item in ponto_virgula]
    lista = []
    for i in range(0, len(virgula)-1):
        tuplo = (float(virgula[i][0]), float(virgula[i][1]))
        lista.append(tuplo)
    return lista 

#Função que faz o menu para escolher o replay desejado
def main():
    print("Replays disponiveis: ")
    if(os.path.isfile('nome_menu.txt')):
        file = open('nome_menu.txt', 'r')
        lista = file.readlines()
        linhas = [linha.rstrip('\n') for linha in lista]
        for i in range (len(linhas)):
            print(i+1, "->", linhas[i])
        x = int(input("Digite o replay que deseja ver: "))

    estado_jogo = foosball_alunos.init_state()
    foosball_alunos.setup(estado_jogo, False)
   
    replay = le_replay(linhas[x-1])
    for i in range(len(replay['bola'])):
        estado_jogo['janela'].update()
        estado_jogo['jogador_vermelho']['jogador'].setpos(replay['jogador_vermelho'][i])
        estado_jogo['jogador_azul']['jogador'].setpos(replay['jogador_azul'][i])
        estado_jogo['bola']['bola'].setpos(replay['bola'][i])
    estado_jogo['janela'].exitonclick()

if __name__ == '__main__':
    main()