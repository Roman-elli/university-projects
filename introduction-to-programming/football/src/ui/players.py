import turtle as t
from config import *

def draw_player(x_pos_inicial, y_pos_inicial, cor):
    player = t.Turtle()
    player.shapesize(stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE)
    player.shape("circle")
    player.color(cor)
    player.penup()
    player.goto(x_pos_inicial, y_pos_inicial)
    player.speed(MOVE_PIXELS)
    player_dictionary = {'player': player,'x_coordinate': player.xcor(), 'y_coordinate': player.ycor(), 'previous_position': None}

    return player_dictionary
