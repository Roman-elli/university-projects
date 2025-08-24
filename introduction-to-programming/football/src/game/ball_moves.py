import turtle as t

def ball_move(match_state):
    ball = match_state['ball']
    ball['ball'].forward(1)
    ball['x_coordinate'] = ball['ball'].xcor()
    ball['y_coordinate'] = ball['ball'].ycor()
