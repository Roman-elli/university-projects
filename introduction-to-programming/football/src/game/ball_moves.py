import turtle as t

def movimenta_bola(estado_jogo):
    ball = estado_jogo['bola']
    ball['bola'].forward(1)
    ball['direcao_x'] = ball['bola'].xcor()
    ball['direcao_y'] = ball['bola'].ycor()
