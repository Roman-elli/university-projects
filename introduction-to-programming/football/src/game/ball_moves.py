import turtle as t

def ball_move(match_state):
    ball = match_state['ball']
    ball['ball'].forward(1)
    ball['direcao_x'] = ball['ball'].xcor()
    ball['direcao_y'] = ball['ball'].ycor()
